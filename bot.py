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

@bot.message_handler(commands=['start'])
def send_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Помощь', '/Телефон')
    keyboard.row('/Аддрес', '/Сайт')
    keyboard.row('/Анкета')
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

@bot.message_handler(commands=['reg'])
def get_reg(message):
    bot.send_message(message.from_user.id,'Введите Login')
    bot.register_next_step_handler(message, get_login)

def get_login(message):
    global login_user
    login_user = message.text
    cursor.execute("SELECT login FROM user where login = ?", (login_user,))
    log = cursor.fetchone()
    logo = log[0]
    if logo == login_user:   
        bot.send_message(message.from_user.id, "Login уже используется, введите новый")
        bot.register_next_step_handler(message, get_reg(message))
    else:
        bot.send_message(message.from_user.id,'Введите Пароль')
        bot.register_next_step_handler(message, get_pass)

def get_pass(message):
    global pass_user
    pass_user = message.text
    bot.register_next_step_handler(message, get_insert(message))

def get_insert(message):
    userp = ("")
    userinf = ("") 
    insert_db(id = 19569, login = login_user, password = pass_user, userpic = userp, userinfo = userinf)
    bot.send_message(message.from_user.id,'Вы успешно зарегестрировались в нашей системе')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'как':
        bot.send_message(message.from_user.id, 'Часто задаваемые вопросы:')
        bot.send_message(message.chat.id, 'Как сделать заказ?')
        bot.send_message(message.chat.id, 'Как зарегестрироваться на сайте?')
        bot.send_message(message.chat.id, 'Как отменить заказ?')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю ваш вопрос.')


bot.polling(none_stop=True)
