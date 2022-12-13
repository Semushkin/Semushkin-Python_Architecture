'''
Скрыть
В этой самостоятельной работе тренируем умения:

    Использовать паттерны page controller, front controller
    Использовать шаблонизатор

Смысл:

Понимать и применять паттерны page и front controllers, понимать как устроены и работают wsgi фреймворки. Использовать шаблонизаторы
Последовательность действий:
0. Создать репозиторий для нового проекта (gitlab, github, ...)
1. С помощью uwsgi или gunicorn запустить пример simple_wsgi.py, проверить что он работает (Эти библиотеки работают на linux системах, документацию по ним можно найти в дополнительных материалах)
2. Написать свой wsgi фреймворк использую паттерны page controller и front controller.
Описание работы фреймворка:

    возможность отвечать на get запросы пользователя (код ответа + html страница)
    для разных url - адресов отвечать разными страницами
    page controller - возможность без изменения фреймворка добавить view для обработки нового адреса
    front controller - возможность без изменения фреймворка вносить изменения в обработку всех запросов

3. Реализовать рендеринг страниц с помощью шаблонизатора jinja2. Документацию по этой библиотеке можно найти в дополнительных материалах
4. Добавить любый полезный функционал в фреймворк, например обработку наличия (отсутствия) слеша в конце адреса, ...
5. Добавить для демонстрации 2 любые разные страницы (например главная и about или любые другие)
6. Сдать дз в виде ссылки на репозиторий
7. В readme указать пример как запустить фреймворк с помощью uwsgi и/или gunicorn

'''


from jinja2 import Template
from pprint import pprint


def application(environ, start_response):
    #pprint(environ)
    start_response('200 OK', [('Content-Type', 'text/html')])
    site = front_controller(environ['PATH_INFO'])
    return [site.encode('utf-8')]


def front_controller(path):
    if path in URLS:
        content = URLS[path]
    else:
        content = page_controller_404()
    return content


def page_controller_main():
    return render('index.html', object_list=[{'content': 'Main Page'}])


def page_controller_about():
    return render('index.html', object_list=[{'content': 'About us'}])


def page_controller_contacts():
    return render('index.html', object_list=[{'content': 'Contacts'}])


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