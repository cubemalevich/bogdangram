import os
from routes import route
from mimes import get_mime

class View:
    @staticmethod
    def read_template_file(filename):
        """
        Читает содержимое файла из папки templates.
        """
        template_dir = 'templates'
        file_path = os.path.join(template_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"File '{filename}' not found."

    @staticmethod
    def render_page(content):
        """
        Генерирует HTML-страницу с заданным контентом.
        """
        template_filename = 'index.html'
        template_content = View.read_template_file(template_filename)
        if "Здесь будут отображаться сообщения" in template_content:
            template_content = template_content.replace("Здесь будут отображаться сообщения", content)
        return template_content

def load(file_name):
    f = open(file_name, encoding='utf-8')
    data = f.read()
    f.close()
    return data

def send_message():
    
    pass

def app(environ, start_response):
    """
    (dict, callable( status: str,
                     headers: list[(header_name: str, header_value: str)]))
                  -> body: iterable of strings_
    """
    if environ['REQUEST_METHOD'] == 'POST':
        # Обработка POST-запроса (отправка сообщения)
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        message = request_body.decode('utf-8').split('=')[1]  # Получаем сообщение из тела запроса
        send_message(message)  # Сохраняем сообщение
        status = '200 OK'
        response_body = "Message sent successfully!"
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]

    # Генерация основного контента страницы
    content = "Здесь будут отображаться сообщения"  # Вы можете добавить динамический контент сюда

    # Генерация HTML-страницы с использованием класса View
    page_content = View.render_page(content)
    
    # Возвращаем HTTP-ответ с сгенерированной страницей
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [page_content.encode('utf-8')]
    # return [bytes(load(f"bogdangram\\" + file_name), "utf-8")]
