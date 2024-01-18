from views import *

routes = {
    '/static/': View,
    '/$': IndexView,
    '/get_user_id': GetUserIdView,
    '/get_messages': GetMessageView,
    '/send_message': SendMessageView,
    '/register': RegisterView,
    '/login': LoginView   
}

def route(url):
    """
    Преобразовывает URL в путь к файлу в соответствии с определенными маршрутами.
    """
    for key in routes.keys():
        if url.startswith(key):
            return routes[key] + url[len(key):]
        return url