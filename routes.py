from views import *

routes = {
    '/static/': View,
    '/$': IndexView,
    '/get_message': GetMessageView,
    '/send_message': SendMessageView
}

def route(url):
    """
    Преобразовывает URL в путь к файлу в соответствии с определенными маршрутами.
    """
    for key in routes.keys():
        if url.startswith(key):
            return routes[key] + url[len(key):]
        return url