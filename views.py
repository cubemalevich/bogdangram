from collections import namedtuple
import sqlite3
import json
import time
import uuid

from urllib.parse import parse_qs
from mimes import get_mime
from webob import Request
from webob.exc import HTTPFound


Response = namedtuple("Response", "status headers data")

class View:
    path = ''

    def __init__(self, url) -> None:
        self.url = url

    def response(self, environ, start_response):
        file_name = self.path + self.url
        headers = [('Content-type', get_mime(file_name))]
        try:
            data = self.read_file(file_name[1:])
            status = '200 OK'
        except FileNotFoundError:
            data = ''
            status = '404 Not found'
        start_response(status, headers)
        return [data.encode('utf-8')]

    def read_file(self, file_name):
        print(file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()

class TemplateView(View):
    template = ''

    def __init__(self, url) -> None:
        super().__init__(url)
        self.url = '/' + self.template

    def response(self, environ, start_response):
        file_name = self.path + self.url
        headers = [('Content-type', get_mime(file_name))]
        try:
            data = self.read_file(file_name[1:])
            status = '200 OK'
        except FileNotFoundError:
            data = ''
            status = '404 Not found'
        start_response(status, headers)
        return [data.encode('utf-8')]

    def read_file(self, file_name):
        print(file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()


class GetMessageView(View):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.last_timestamp = 0

    def response(self, environ, start_response):
        headers = [('Content-type', 'application/json')]
        status = '200 OK'

        query_params = parse_qs(environ.get('QUERY_STRING', ''))
        message_id = int(query_params.get('message_id', [0])[0])

        messages, timestamp = self.get_new_messages_from_db(message_id)
        data = json.dumps({'messages': messages, 'timestamp': timestamp})

        self.last_timestamp = timestamp

        start_response(status, headers)
        return [data.encode('utf-8')]

    def get_new_messages_from_db(self, message_id):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('SELECT message_text, timestamp FROM messages WHERE message_id > ?', (message_id,))
        messages = cursor.fetchall()
        conn.close()

        if messages:
            timestamp = max(msg[1] for msg in messages)
        else:
            timestamp = self.last_timestamp

        return [message[0] for message in messages], timestamp
    

class GetUserIdView(View):

    # Функция для получения user_id из базы данных по имени пользователя
    def fetch_user_id_from_database(self, username):
        connection = sqlite3.connect('messages.db')
        cursor = connection.cursor()

        # Используем параметризованный запрос для предотвращения SQL-инъекций
        cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
        
        user_id = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_id[0] if user_id else None

    def response(self, environ, start_response):
        headers = [
            ('Content-type', 'application/json'),
            ('Access-Control-Allow-Origin', 'http://localhost:8000'),  
            ('Access-Control-Allow-Credentials', 'true'), 
            ]

        request = Request(environ)

        user_id_cookie = request.cookies.get('user_id')

        if user_id_cookie:
            user_id = user_id_cookie
        else:
            user_id = None

        print("Response from /get_user_id:", {"user_id": user_id})

        if user_id is None:
            print("User ID is None. Cannot fetch messages.")
            status = '200 OK'
            data = json.dumps({'user_id': None})
            start_response(status, headers)
            return [data.encode('utf-8')]
        else:
            print(f"Fetching messages for user_id: {user_id}")

            fetched_user_id = self.fetch_user_id_from_database(user_id)

            if fetched_user_id is not None:
                user_id = fetched_user_id

            print("Fetched user_id:", user_id)

            status = '200 OK'
            data = json.dumps({'user_id': str(user_id)})  
            start_response(status, headers + [('Set-Cookie', f'user_id={user_id}; Path=/')])
            return [data.encode('utf-8')]
        
class SendMessageView(View):
    def response(self, environ, start_response):
        message, user_id = self.get_message_and_user_from_request(environ)

        if message and user_id:
            timestamp = int(time.time())
            #nickname = self.get_nickname_from_database(user_id)
            full_message = "{message}"
            self.save_message_to_db(full_message, user_id, timestamp)

            status = '200 OK'
            headers = [('Content-type', 'application/json')]
            data = json.dumps({'message': 'Сообщение успешно получено и сохранено'})
        else:
            status = '400 Bad Request'
            headers = [('Content-type', 'application/json')]
            data = json.dumps({'error': 'Неверное сообщение или пользователь'})

        start_response(status, headers)
        return [data.encode('utf-8')]
    
    def save_message_to_db(self, message, user_id, timestamp):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (user_id, sender, message_text, timestamp) VALUES (?, ?, ?, ?)',
                    (user_id, self.get_nickname_from_database(user_id), message, timestamp))
        conn.commit()
        conn.close()


    def get_message_and_user_from_request(self, environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')

            parsed_body = json.loads(request_body)

            message = parsed_body.get('message', '')
            user_id = parsed_body.get('user_id', '')

            if not message or not user_id:
                raise ValueError("Invalid message or user_id")

            return message, user_id
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None, None
        except Exception as e:
            print(f"Error while extracting message and user_id: {e}")
            return None, None

        

    def get_nickname_from_database(self, user_id):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE user_id=?', (user_id,))
        nickname = cursor.fetchone()
        conn.close()

        if nickname:
            print(f"Nickname found in the database: {nickname[0]}")
            return nickname[0]
        else:
            print(f"Nickname not found in the database for user_id: {user_id}")
            return 'Guest' #Гостевой пользователь


class IndexView(TemplateView):
    template = 'templates/index.html'

class NotFoundView(TemplateView):
    pass

class RegisterView(TemplateView):
    template = 'templates/register.html'

    def response(self, environ, start_response):
        request = Request(environ)
        if request.method == 'POST':
            post_data = request.POST
            username = post_data.get('username', '')
            password = post_data.get('password', '')

            if username and password:
                success = self.register_user(username, password)
                if success:
                    status = '200 OK'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'message': 'User registered successfully'})
                else:
                    status = '400 Bad Request'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'error': 'Username already exists'})
            else:
                status = '400 Bad Request'
                headers = [('Content-type', 'application/json')]
                data = json.dumps({'error': 'Invalid username or password'})

            start_response(status, headers)
            return [data.encode('utf-8')]

        return super().response(environ, start_response)

    def register_user(self, username, password):
        print(f"Received username reg_us: {username}, password: {password}")
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()

        # Генерируем уникальный идентификатор пользователя
        user_id = uuid.uuid4().hex

        # Проверяем, есть ли уже пользователь с таким именем
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return False  # Пользователь с таким именем уже существует

        # Если пользователь не найден, регистрируем нового
        cursor.execute('INSERT INTO users (username, password, user_id) VALUES (?, ?, ?)', (username, password, user_id))
        cursor.execute('INSERT INTO messages (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()
        return True  # Пользователь успешно зарегистрирован

    def get_post_data(self, request, key):
        try:
            data = request.POST.get(key, '')
            print(f"Received data for {key}: {data}")  # Добавим отладочное сообщение
            return data
        except Exception as e:
            print(f"Error while extracting {key}: {e}")
            return None

class LoginView(TemplateView):
    template = 'templates/login.html'

    def response(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'POST':
            request = Request(environ)
            post_data = parse_qs(request.body.decode('utf-8'))
            username = post_data.get('username', [''])[0]
            password = post_data.get('password', [''])[0]

            if username and password:
                user_id = self.authenticate_user(username, password)
                if user_id:
                    # Вместо редиректа возвращаем JSON с информацией о редиректе
                    status = '200 OK'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'redirect': '/', 'user_id': str(user_id[0])})  
                    start_response(status, headers)
                    return [data.encode('utf-8')]
                else:
                    status = '401 Unauthorized'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'error': 'Invalid username or password'})
                    start_response(status, headers)
                    return [data.encode('utf-8')]
            else:
                status = '400 Bad Request'
                headers = [('Content-type', 'application/json')]
                data = json.dumps({'error': 'Invalid username or password'})
                start_response(status, headers)
                return [data.encode('utf-8')]
        else:
            return super().response(environ, start_response)

    def authenticate_user(self, username, password):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()

        print(f"Received username: {username}, password: {password}")
        
        # Проверяем, существует ли пользователь с таким именем и паролем
        cursor.execute('SELECT user_id FROM users WHERE username=? AND password=?', (username, password))
        user_id = cursor.fetchone()

        conn.close()

        # Если пользователь существует, возвращаем его ID, иначе None
        print("Authenticated user_id:", user_id)  

        return user_id


    def get_post_data(self, request):
        try:
            data = request.POST
            return data
        except Exception as e:
            print(f"Error while extracting POST data: {e}")
            return None