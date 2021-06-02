import telebot
from telebot import types
import sqlite3
from sqlite3 import Error


bot = telebot.TeleBot('1792282194:AAHS45Vu6zVNPvDA2WMItgCiFLr1E8tNypw')

conn = sqlite3.connect('course prj(flask)/shop.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, username: str, first_name: str, last_name: str):
	cursor.execute('INSERT INTO USERS (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)', (user_id, username, first_name, last_name))
	conn.commit()

@bot.message_handler(commands=['db'])

def get_nick(message):
    bot.send_message(message.from_user.id, "Введите Имя")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global regFirst_name
    regFirst_name = message.text
    global lasTname
    bot.send_message(message.from_user.id, "Введите фамилию")
    bot.register_next_step_handler(message, get_lastname)
    
def get_lastname(message):
    lasTname = message.text
    bot.send_message(message.from_user.id, "Ваше имя и фамилия добавлены.")
    us_id = message.from_user.id
    us_nick = message.from_user.first_name
    db_table_val(user_id=us_id, username=us_nick, first_name=regFirst_name, last_name=lasTname)
     
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Помощь', '/Телефон')
    keyboard.row('/Аддрес', '/Сайт')
    bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name} .Я бот помощник интернет магазина flask shop. Для работы с мной используйте команды /', reply_markup=keyboard)

@bot.message_handler(commands=['Аддрес'])
def send_message(message):
    bot.send_message(message.chat.id, 'Адрес: г. Москва, ул. Льва Толстого, 16,')
    bot.send_photo(message.chat.id, 'https://www.google.com/maps/vt/data=zX0dR23DdbyWHNSb2pVHtR154RqHYvAAVeABVOjbqCaMAsZ2HNdPcEIdEiEOUjtp5KnH6EpkisaFdSIyMPW9j_QyRiXvQtJl1V5-KjiiyZKcN902jy7Zgf81n_tFEerYsLr-AKN2jFGwv4-QO8PYKiJq2-o63CrCfMqYRCF_J4PrnJ7njUEwHwgRDuTXkLnO1z7sB3kxr3xaNKIqEg1hAZu9Vv78hp89lBBGfJ8-DpXkCpGs6ox4B2dXcOelBKClxqHO6QioHYg5V_0i_4NudYkGlp1zo0EBTGmEc4awWfPSr6e39ePS2ZiX')

@bot.message_handler(commands=['Помощь'])
def send_message(message):
    bot.send_message(message.chat.id, 'Для связи с специалистом используйте наш аддрес электронной почты flejm198765@gmail.com ')

@bot.message_handler(commands=['Телефон'])
def send_message(message):
    bot.send_message(message.chat.id, 'Телефон: +7(495)776-3030 ')

@bot.message_handler(commands = ['Сайт'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='http://127.0.0.1:5000/')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейдите на наш сайт.", reply_markup = markup)

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
