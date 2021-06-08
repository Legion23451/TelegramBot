import telebot
from telebot import types
import config
import requests
import sqlite3

conn = sqlite3.connect('shop.db', check_same_thread=False)
cursor = conn.cursor()

ab = open('config.txt', 'r')
bc = open('1.txt', 'r')
cd = open('2.txt', 'r')
de = open('3.txt', 'r')

TOKEN = ab.read()

user_admin_code = bc.read()
delete_item_code = cd.read()
delete_qestion_code = de.read()

bot = telebot.TeleBot(TOKEN)

response = requests.get(config.url).json()

def insert_db(name: str, Email: str, problem: str, phone: int):
	cursor.execute('INSERT INTO help (name, Email, problem, phone) VALUES (?, ?, ?, ?)', (name, Email, problem, phone))
	conn.commit()

@bot.message_handler(commands=['start'])
def send_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Помощь', '/Телефон')
    keyboard.row('/Адрес', '/Сайт')
    keyboard.row('/Валюта', '/Товары')
    keyboard.row('/Анкета_об_ошибке')
    bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name} .Я бот помощник интернет магазина flask shop. Для работы с мной используйте команды /', reply_markup=keyboard)

@bot.message_handler(commands=['Адрес'])
def send_addres(message):
    bot.send_message(message.chat.id, 'Адрес: г. Москва, ул. Льва Толстого, 16,')
    bot.send_photo(message.chat.id, 'https://www.google.com/maps/vt/data=zX0dR23DdbyWHNSb2pVHtR154RqHYvAAVeABVOjbqCaMAsZ2HNdPcEIdEiEOUjtp5KnH6EpkisaFdSIyMPW9j_QyRiXvQtJl1V5-KjiiyZKcN902jy7Zgf81n_tFEerYsLr-AKN2jFGwv4-QO8PYKiJq2-o63CrCfMqYRCF_J4PrnJ7njUEwHwgRDuTXkLnO1z7sB3kxr3xaNKIqEg1hAZu9Vv78hp89lBBGfJ8-DpXkCpGs6ox4B2dXcOelBKClxqHO6QioHYg5V_0i_4NudYkGlp1zo0EBTGmEc4awWfPSr6e39ePS2ZiX')

@bot.message_handler(commands=['Помощь'])
def send_help(message):
    bot.send_message(message.chat.id, 'Для связи с специалистом используйте наш аддрес электронной почты flejm198765@gmail.com, или заполните анкету о проблеме ')

@bot.message_handler(commands=['Телефон'])
def send_phone(message):
    bot.send_message(message.chat.id, 'Телефон: +7(495)776-3030 ')

@bot.message_handler(commands=['Сайт'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='http://127.0.0.1:5000/')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейдите на наш сайт.", reply_markup = markup)  

@bot.message_handler(commands=['Анкета_об_ошибке'])     
def get_nick(message):
    bot.send_message(message.from_user.id, "Введите Имя")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global user_name
    user_name = message.text
    bot.send_message(message.from_user.id, "Введите email")
    bot.register_next_step_handler(message, get_lastname)

def get_lastname(message):
    global user_email
    user_email = message.text
    bot.send_message(message.from_user.id, "Опишите вашу проблему.")
    bot.register_next_step_handler(message, get_phone)
    
def get_phone(message):
    global user_eror
    user_eror = message.text
    bot.send_message(message.from_user.id, "Введите телефон")
    bot.register_next_step_handler(message, get_eror)

def get_eror(message):
    user_phone = message.text
    bot.send_message(message.chat.id, "Ваша заявка принята.")
    insert_db(name = user_name, Email = user_email, problem = user_eror, phone = user_phone)
    conn.commit()

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

@bot.message_handler(commands=['Удаление_товара'])
def get_delete(message):
    bot.send_message(message.chat.id, 'Введите код доступа')
    bot.register_next_step_handler(message, get_code_tov)

def get_code_tov(message):
    code = message.text
    if code == delete_item_code:
        bot.send_message(message.chat.id, 'Введите артикул товара')
        bot.register_next_step_handler(message, get_art_tov)
    else:
        bot.send_message(message.chat.id, 'Код не верный')

def get_art_tov(message):
    art = message.text
    cursor.execute("SELECT iditem FROM item where iditem = ?", (art,))
    log = cursor.fetchall()
    if log is None:
        bot.send_message(message.chat.id, 'Нечего удалять')
    else:
        cursor.execute("DELETE FROM item WHERE iditem = ?", (art,))
        conn.commit()
        bot.send_message(message.chat.id, 'Удалено.')

@bot.message_handler(commands=['Заявления'])
def get_text_messages(message):
        cursor.execute("SELECT * FROM help ")
        log = cursor.fetchall()
        print(type(log))
        conn.commit()
        bot.send_message(message.chat.id, 'Активные заявки ')
        text = str(log)
        a = text.strip("[]")
        count = 1
        i = 0
        b = len(a)
        newtext2 = ''
        for i in range(b):
            if a[i] == ',':
                if count % 5 == 0:        
                    newtext2 +='\n\n'
                    count += 1
                else:
                    count += 1
            else:
                newtext2 +=a[i]
        bot.send_message(message.chat.id, newtext2)

@bot.message_handler(commands=['Удаление_заявления'])
def get_delete(message):
    bot.send_message(message.chat.id, 'Введите код доступа')
    bot.register_next_step_handler(message, get_code)

def get_code(message):
    code = message.text
    if code == delete_qestion_code:
        bot.send_message(message.chat.id, 'Введите номер заявления')
        bot.register_next_step_handler(message, get_art)
    else:
        bot.send_message(message.chat.id, 'Код не верный')

def get_art(message):
    eror = message.text
    cursor.execute("SELECT id FROM help where id = ?", (eror,))
    log = cursor.fetchall()
    if log is None:
        bot.send_message(message.chat.id, 'Нечего удалять')
    else:
        cursor.execute("DELETE FROM help WHERE id = ?", (eror,))
        conn.commit()
        bot.send_message(message.chat.id, 'Заявление удалено.')

@bot.message_handler(commands=['admin'])
def get_root(message):
    bot.send_message(message.chat.id, 'Введите код доступа')
    bot.register_next_step_handler(message, get_root_code)

def get_root_code(message):
    code_admin = message.text
    if code_admin == user_admin_code:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('/Заявления')
        keyboard.row('/Удаление_товара')
        keyboard.row('/Удаление_заявления')
        bot.send_message(message.chat.id, 'Добро пожаловать в root', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Код не верный')

@bot.message_handler(commands=['Валюта'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('USD')
    itembtn2 = types.KeyboardButton('EUR')
    itembtn3 = types.KeyboardButton('RUR')
    itembtn4 = types.KeyboardButton('BTC')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, "Узнать курс ПриватБанка ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)

def process_coin_step(message):
    try:
       markup = types.ReplyKeyboardRemove(selective=False)

       for coin in response:
           if (message.text == coin['ccy']):
              bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']), reply_markup=markup)

    except Exception as e:
       bot.reply_to(message, 'Ошибка')

def printCoin(buy, sale):
    '''Вывод курса пользователю'''
    return "Курс покупки: " + str(buy) + " Курс продажи: " + str(sale)

bot.polling(none_stop=True, interval=0)