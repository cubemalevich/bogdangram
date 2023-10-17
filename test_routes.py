import unittest
import routes
import mimes

class TestRoutes(unittest.TestCase):
    def route(self, url, file):
        self.assertEqual(routes.route(url), file)

    def test_root(self):
        """
        Тест корня сайта
        """
        self.route('/index.html', 'templates/index.html')

    def test_static(self):
        """
        Тест static файлов
        """
        self.route('/static/app.js', 'static/app.js')

class TestMimes(unittest.TestCase):
    def mime(self, file, content):
        self.assertEqual(mimes.get_mime(file), content)

    def test_html(self):
        """
        Тест корня сайта
        """
        self.mime('/index.html', 'text/html')

    def test_css(self):
        """
        Тест static файлов
        """
        self.mime('/static/style.css', 'text/css')
    