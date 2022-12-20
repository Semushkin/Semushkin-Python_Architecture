from wsgiref.simple_server import make_server
from simple_wsgi import Application
from urls import URLS

application = Application(URLS)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()