import os
import re
from routes import routes
from mimes import get_mime
from views import View
import sqlite3

# Создание подключения к базе данных SQLite
conn = sqlite3.connect('messages.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы для хранения учетных данных пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Создание таблицы для хранения сообщений
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_text TEXT NOT NULL
    )
''')

# Закрытие соединения с базой данных
conn.close()

def load(file_name):
    f = open(file_name, encoding='utf-8')
    data = f.read()
    f.close()
    return data

def app(environ, start_response):
    """
    (dict, callable( status: str,
                     headers: list[(header_name: str, header_value: str)]))
                  -> body: iterable of strings_
    """
    url = environ['REQUEST_URI']
    view = None
    
    for key in routes.keys():
        if re.match(key, url) is not None:
            view = routes[key](url)
            break
    
    if view is None:
        view = NotFoundView(url)
    
    # Изменение вызова метода response(), передаем только один аргумент
    resp = view.response(environ)  # Передаем environ в метод response()
    # Возвращаем HTTP-ответ с сгенерированной страницей
    status = resp.status    #'200 OK'
    #file_name = route(environ['REQUEST_URI'])
    response_headers = resp.headers
    start_response(status, response_headers)
    return [bytes(resp.data, "utf-8")]

   
 