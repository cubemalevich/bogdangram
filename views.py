from collections import namedtuple
import sqlite3
import json
from urllib.parse import parse_qs

from mimes import get_mime

Response = namedtuple("Response", "status headers data") 

class View:
    path = ''

    def __init__(self, url) -> None:
        self.url = url

    def response(self, environ):
        file_name = self.path + self.url
        headers = [('Content-type', get_mime(file_name))]
        try:
            data = self.read_file(file_name[1:])
            status = '200 OK'
        except FileNotFoundError:
            data = ''
            status = '404 Not found'
        return Response(status, headers, data)
    
    def read_file(self, file_name):
        print(file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    
class TemplateView(View):
    template = ''
    def __init__(self, url) -> None:
        super().__init__(url)
        self.url = '/' + self.template

class GetMessageView(View):
    def response(self, environ):
        headers = [('Content-type', 'application/json')]
        status = '200 OK'
        messages = self.get_messages_from_db()
        data = json.dumps({'messages': messages})
        return Response(status, headers, data)

    def get_messages_from_db(self):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('SELECT message_text FROM messages')
        messages = cursor.fetchall()
        conn.close()
        return [message[0] for message in messages]

class SendMessageView(View):
    def response(self, environ):
        message = self.get_message_from_request(environ)
        
        if message:
            self.save_message_to_db(message)

            status = '200 OK'
            headers = [('Content-type', 'application/json')]
            data = json.dumps({'message': 'Message received and saved successfully'})
        else:
            status = '400 Bad Request'
            headers = [('Content-type', 'application/json')]
            data = json.dumps({'error': 'Invalid message'})
        
        return Response(status, headers, data)

    def get_message_from_request(self, environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
            
            parsed_body = parse_qs(request_body)
            
            message = parsed_body.get('message', [''])[0]
            
            return message
        except Exception as e:
            print(f"Error while extracting message: {e}")
            return None

    def save_message_to_db(self, message):
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (message_text) VALUES (?)', (message,))
        conn.commit()
        conn.close()

class IndexView(TemplateView):
    template = 'templates/index.html'
class NotFoundView(TemplateView):
    pass
class RegisterView(TemplateView):
    template = 'templates/register.html'

    def response(self, environ):
        if environ['REQUEST_METHOD'] == 'GET':
            return super().response(environ)
        elif environ['REQUEST_METHOD'] == 'POST':
            username = self.get_post_data(environ, 'username')
            password = self.get_post_data(environ, 'password')

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
                

            return Response(status, headers, data)
        
    def register_user(self, username, password):
        print(f"Received username reg_us: {username}, password: {password}")  
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()

        # Проверяем, есть ли уже пользователь с таким именем
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return False  # Пользователь с таким именем уже существует

        # Если пользователь не найден, регистрируем нового
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True  # Пользователь успешно зарегистрирован

    def get_post_data(self, environ, key):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
            parsed_body = parse_qs(request_body)
            data = parsed_body.get(key, [''])[0]
            print(f"Received data for {key}: {data}")  # Добавим отладочное сообщение
            return data
        except Exception as e:
            print(f"Error while extracting {key}: {e}")
            return None
        
class LoginView(TemplateView):
    template = 'templates/login.html'

    def response(self, environ):
        if environ['REQUEST_METHOD'] == 'GET':
            return super().response(environ)
        elif environ['REQUEST_METHOD'] == 'POST':
            username = self.get_post_data(environ, 'username')
            password = self.get_post_data(environ, 'password')

            if username and password:
                authenticated = self.authenticate_user(username, password) 
                if authenticated:
                    status = '200 OK'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'message': 'User authenticated successfully'})
                else:
                    status = '401 Unauthorized'
                    headers = [('Content-type', 'application/json')]
                    data = json.dumps({'error': 'Invalid username or password'})
            else:
                status = '400 Bad Request'
                headers = [('Content-type', 'application/json')]
                data = json.dumps({'error': 'Invalid username or password'})
                
            return Response(status, headers, data)
        
    def authenticate_user(self, username, password):
        print(f"Received username: {username}, password: {password}")  
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return True  # Возвращаем True, если пользователь найден и пароль совпадает
        else:
            return False  # Возвращаем False в противном случае

    def get_post_data(self, environ, key):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
            parsed_body = parse_qs(request_body)
            return parsed_body.get(key, [''])[0]
        except Exception as e:
            print(f"Error while extracting {key}: {e}")
            return None


