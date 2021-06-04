import telebot
from time import ctime
from telebot import types
from sql import *

f = open('config.txt')
TOKEN = f.readline()
bot = telebot.TeleBot('1792282194:AAHS45Vu6zVNPvDA2WMItgCiFLr1E8tNypw')

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

@bot.message_handler(commands=['Анкета'])
def chek_user(message):
    teg_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM USERS WHERE user_id = {teg_id}")
    data = cursor.fetchone()
    if data is None:
        bot.register_next_step_handler(message, get_nick)
    else:
        bot.send_message(message.from_user.id, "Вы уже зарегестрировали свою анкету.")
        
def get_nick(message):
    bot.send_message(message.from_user.id, "Введите Имя")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    regFirst_name = message.text
    bot.send_message(message.from_user.id, "Введите фамилию")
    bot.register_next_step_handler(message, get_lastname)
    return regFirst_name

def get_lastname(message):
    lasTname = message.text
    bot.send_message(message.from_user.id, "Введите телефон без 8")
    bot.register_next_step_handler(message, get_phone)
    return lasTname

def get_phone(message):
    phonenumber = message.text
    bot.send_message(message.from_user.id, "Опишите вашу проблему.")
    bot.register_next_step_handler(message, get_eror)
    return phonenumber

def get_eror(message):
    error_text = message.text
    bot.send_message(message.chat.id, "Ваша заявка принята.")
    us_id = message.chat.id
    us_nick = message.from_user.first_name
    db_table_val(user_id=us_id, username=us_nick, first_name=get_name, last_name=get_lastname, phone=get_phone, error=error_text, reg_date=ctime())  

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
