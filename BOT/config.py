import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('shop.db', check_same_thread=False)
cursor = conn.cursor()

def insert_db(name: str, Email: str, problem: str, phone: int):
	cursor.execute('INSERT INTO help (name, Email, problem, phone) VALUES (?, ?, ?, ?)', (name, Email, problem, phone))
	conn.commit()

url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

