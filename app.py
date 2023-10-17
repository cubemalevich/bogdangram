import os
from routes import route
from mimes import get_mime

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
    status = '200 OK'
    file_name = route(environ['REQUEST_URI'])
    response_headers = [('Content-type', get_mime(file_name))]
    start_response(status, response_headers)
    
    return [bytes(load(f"bogdangram\\" + file_name), "utf-8")]
