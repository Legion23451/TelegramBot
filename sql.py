import telebot
from telebot import types
import sqlite3
from sqlite3 import Error
from time import ctime

conn = sqlite3.connect('course prj(flask)/shop.db', check_same_thread=False)
cursor = conn.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        phone INTEGER,
                        error TEXT,
                        reg_date TEXT);''')
    conn.commit()

def db_table_val(user_id: int, username: str, first_name: str, last_name: str, phone: int, error: str, reg_date: str):
	cursor.execute('INSERT INTO USERS (user_id, username, first_name, last_name, phone, error, reg_date) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, username, first_name, last_name, phone, error, reg_date))
	conn.commit()
