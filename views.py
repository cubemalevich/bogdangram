from collections import namedtuple
import json

from mimes import get_mime

Response = namedtuple("Response", "status headers data") # Именнованный кортеж, 

class View:
    path = ''

    def __init__(self, url) -> None:
        self.url = url

    def response(self):
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
        """
        Читает содержимое файла из папки templates.
        """
        #try:
        print(file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
        #except FileNotFoundError:
        #    return f"File '{file_name}' not found."
    
class TemplateView(View):
    template = ''
    def __init__(self, url) -> None:
        super().__init__(url)
        self.url = '/' + self.template

class GetMessageView(View):
    def response(self):
        headers = [('Content-type', 'application/json')]
        status = '200 OK'
        data = json.dumps({'messages':['test', 'test2']}) #Начальные сообщения  
        return Response(status, headers, data)
    
class IndexView(TemplateView):
    template = 'templates/index.html'