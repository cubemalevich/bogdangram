import os
import re
from routes import routes
from mimes import get_mime
from views import View


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
    for key in routes.keys():
        print('url', url, 'key', key)
        if re.match(key, url) is not None:
            view = routes[key](url)
    resp = view.response()
    # Возвращаем HTTP-ответ с сгенерированной страницей
    status = resp.status#'200 OK'
    #file_name = route(environ['REQUEST_URI'])
    response_headers = resp.headers
    start_response(status, response_headers)
    return [bytes(resp.data, "utf-8")]
   
 