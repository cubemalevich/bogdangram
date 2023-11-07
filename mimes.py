mimes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript'
}

def get_mime(file_name):
    """
    Возвращает тип содержимого по имени файла 
    """
    for key in mimes.keys():
        if file_name.find(key) > 0:
            return mimes[key]
    return 'text/plain'