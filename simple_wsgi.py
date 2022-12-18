'''
В этой самостоятельной работе тренируем умения:

    Разделять get и post запрос внутри wsgi-фреймворка
    Получать и декодировать параметры post запроса

Смысл:

Чтобы уметь обрабатывать разные типы web-запросов
Последовательность действий:
0. Добавить в свой wsgi-фреймворк возможность обработки post-запроса
1. Добавить в свой wsgi-фреймворк возможность получения данных из post запроса
2. Дополнительно можно добавить возможность получения данных из get запроса
3. В проект добавить страницу контактов на которой пользователь может отправить нам сообщение (пользователь вводит тему сообщения, его текст, свой email)
4. После отправки реализовать сохранение сообщения в файл, либо вывести сообщение в терминал (базу данных пока не используем)


'''
from quopri import decodestring

from jinja2 import Template
from pprint import pprint


class Application:
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, environ, start_response):
        site = self.front_controller(environ['PATH_INFO'], environ)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [site.encode('utf-8')]

    def front_controller(self, path, env):
        method = env['REQUEST_METHOD']
        query = env["QUERY_STRING"]
        if method == 'GET':
            if query:
                print(f'Получен GET запрос, c данными {self.parse_query_data(query)}')
            else:
                print('Получен GET запрос, без данных')
        elif method == 'POST':
            if env.get('CONTENT_LENGTH'):
                message = self.post_request(env)
                print(f'Получено сообщение (POST запрос) от {message["name"]}, c адресом {message["email"]}\n'
                      f'Cообщение: {message["message"]}')
        if path in self.urls:
            content = self.urls[path]
        else:
            content = page_controller_404()
        return content

    @staticmethod
    def parse_query_data(data):
        result = {}
        params = data.split('&')
        for param in params:
            key, value = param.split('=')
            result[key] = value
        return result

    def post_request(self, env):
        data = env['wsgi.input'].read(int(env.get('CONTENT_LENGTH')))
        data = data.decode(encoding='utf-8')
        data = self.parse_query_data(data)
        data = self.decode_value(data)
        return data

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            new_data[k] = decodestring(val).decode('UTF-8')
        return new_data


def page_controller_main():
    return render('templates/index.html', object_list=[{'content': 'Main Page'}])


def page_controller_about():
    return render('templates/about.html', object_list=[{'content': 'About us'}])


def page_controller_contacts():
    return render('templates/contacts.html', object_list=[{'content': 'Contacts'}])


def page_controller_404():
    return '404 Page not found!!!'


def render(template_name, **kwargs):
    with open(template_name, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)


URLS = {
    '/': page_controller_main(),
    '/about': page_controller_about(),
    '/contacts': page_controller_contacts(),
}

application = Application(URLS)
