import telebot
from time import ctime
from telebot import types
from telebot.apihelper import get_chat_member
from sql import *
conn = sqlite3.connect('shop.db', check_same_thread=False)
cursor = conn.cursor()
f = open('config.txt', 'r')
TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
admin = "777"
@bot.message_handler(commands=['start'])
def send_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Помощь', '/Телефон')
    keyboard.row('/Аддрес', '/Сайт')
    keyboard.row('/Регистрация', '/Товары')
    keyboard.row('/Удаление')
    bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name} .Я бот помощник интернет магазина flask shop. Для работы с мной используйте команды /', reply_markup=keyboard)

@bot.message_handler(commands=['Аддрес'])
def send_addres(message):
    bot.send_message(message.chat.id, 'Адрес: г. Москва, ул. Льва Толстого, 16,')
    bot.send_photo(message.chat.id, 'https://www.google.com/maps/vt/data=zX0dR23DdbyWHNSb2pVHtR154RqHYvAAVeABVOjbqCaMAsZ2HNdPcEIdEiEOUjtp5KnH6EpkisaFdSIyMPW9j_QyRiXvQtJl1V5-KjiiyZKcN902jy7Zgf81n_tFEerYsLr-AKN2jFGwv4-QO8PYKiJq2-o63CrCfMqYRCF_J4PrnJ7njUEwHwgRDuTXkLnO1z7sB3kxr3xaNKIqEg1hAZu9Vv78hp89lBBGfJ8-DpXkCpGs6ox4B2dXcOelBKClxqHO6QioHYg5V_0i_4NudYkGlp1zo0EBTGmEc4awWfPSr6e39ePS2ZiX')

@bot.message_handler(commands=['Помощь'])
def send_help(message):
    bot.send_message(message.chat.id, 'Для связи с специалистом используйте наш аддрес электронной почты flejm198765@gmail.com ')

@bot.message_handler(commands=['Телефон'])
def send_phone(message):
    bot.send_message(message.chat.id, 'Телефон: +7(495)776-3030 ')

@bot.message_handler(commands=['Сайт'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='http://127.0.0.1:5000/')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейдите на наш сайт.", reply_markup = markup)  

@bot.message_handler(commands=['Регистрация'])
def get_reg(message):
    bot.send_message(message.chat.id,'Введите Login')
    bot.register_next_step_handler(message, get_login)

def get_login(message):
    global login_user
    login_user = message.text
    cursor.execute("SELECT login FROM user where login = ?", (login_user,))
    log = cursor.fetchone()
    conn.commit()
    if log is None:   
        bot.send_message(message.chat.id,'Введите Пароль')
        bot.register_next_step_handler(message, get_pass)
    else:
        bot.send_message(message.chat.id, "Login уже используется \n Для регистрации введите /Регистрация ")

def get_pass(message):
    global pass_user
    pass_user = message.text
    bot.register_next_step_handler(message, get_insert(message))

def get_insert(message):
    userp = ("")
    userinf = ("") 
    id_user = None
    insert_db(id = id_user, login = login_user, password = pass_user, userpic = userp, userinfo = userinf)
    conn.commit()
    cursor.close()
    bot.send_message(message.from_user.id,'Вы успешно зарегестрировались в нашей системе')

@bot.message_handler(commands=['Товары'])
def get_text_messages(message):
        cursor.execute("SELECT title, price FROM item ")
        log = cursor.fetchall()
        conn.commit()
        bot.send_message(message.chat.id, 'Товары в наличии ')
        text = str(log)
        a = text.strip("[]")
        count = 1
        i = 0
        b = len(a)
        newtext = ''
        for i in range(b):
            if a[i] == ',':
                if count % 2 == 0:        
                    newtext +='\n'
                    count += 1
                else:
                    count += 1
            else:
                if a[i] == '(' or a[i] == ')':
                    if a[i] == ')':
                        newtext += ' руб'
                else:
                    newtext +=a[i]
        bot.send_message(message.chat.id, newtext)

@bot.message_handler(commands=['Удаление'])
def get_delete(message):
    bot.send_message(message.chat.id, 'Введите код доступа')
    bot.register_next_step_handler(message, get_code)

def get_code(message):
    code = message.text
    if code == admin:
        bot.send_message(message.chat.id, 'Введите артикул товара')
        bot.register_next_step_handler(message, get_art)
    else:
        bot.send_message(message.chat.id, 'Код не верный')

def get_art(message):
    art = message.text
    cursor.execute("SELECT iditem FROM item where iditem = ?", (art))
    log = cursor.fetchall()
    if log is None:
        bot.send_message(message.chat.id, 'Нечего удалять')
    else:
        cursor.execute("DELETE FROM item WHERE iditem = ?", (art))
        conn.commit()
        bot.send_message(message.chat.id, 'Удалено.')

bot.polling(none_stop=True, interval=0)
