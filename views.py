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
