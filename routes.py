routes = {
    '/static/': 'static/',
    '/': 'templates/' 
}

def route(url):
    """
    Преобразовывает url в путь к файлу
    """
    for key in routes.keys():
        if url.find(key) == 0:
            return url.replace(key, routes[key])
    return url
