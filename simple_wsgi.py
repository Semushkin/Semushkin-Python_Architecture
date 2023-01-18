
'''
В этой самостоятельной работе тренируем умения:

    Выбирать подходящий порождающий шаблон
    Применять порождающие шаблоны в своем коде

Смысл:

Для использования порождающих шаблонов в своем коде
Последовательность действий:
0. На базе нашего wsgi-фреймворка мы начинаем делать обучающий сайт, для того чтобы на нем отработать навыки применения
    шаблонов проектирования
1. Тема (чему мы будем обучать) может быть любая, что вам больше нравиться (например: горным лыжам, йоге,
    администрированию, фридайвингу, продажам, …)
2. Минимальное описание работы сайта следующее:

    На сайте есть курсы по обучению чему либо. Курс относится какой либо категории.
    Например для обучения программированию есть python, java, javascript. И курсы python для новичков, java для профи, …
    Также на сайте есть студенты, которые могут записаться на один или несколько курсов ###
    3. Это минимальный функционал, на котором мы будем отрабатывать шаблоны, можно будет его расширить. ###
    4. В данном домашнем задании требуется добавить следующий функционал:
        Создание категории курсов
        Вывод списка категорий
        Создание курса
        Вывод списка курсов ###
    5. Далее можно сделать всё или одно на выбор, применив при этом один из порождающих паттернов, либо аргументировать почему данные паттерны не были использованы:
    На сайте могут быть курсы разных видов: офлайн (в живую) курсы (для них указывается адрес проведения) и онлайн курсы (вебинары), для них указывается вебинарная система.
    Также известно что в будущем могут добавиться новые виды курсов
    Реализовать простой логгер (не используя сторонние библиотеки). У логгера есть имя. Логгер с одним и тем же именем пишет данные в один и тот же файл, а с другим именем в другой
    Реализовать страницу для копирования уже существующего курса (Для того чтобы снова с нуля не создавать курс, а скопировать существующий и немного отредактировать)


'''
from pprint import pprint
from quopri import decodestring
from views import PageController404


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
        request = {}
        if method == 'GET':

            request['method'] = method
            if query:
                print(f'Получен GET запрос, c данными {self.parse_query_data(query)}')
                request['data'] = self.parse_query_data(query)
            else:
                print('Получен GET запрос, без данных')
        elif method == 'POST':
            request['method'] = method
            if env.get('CONTENT_LENGTH'):
                #message = self.post_request(env)
                request['data'] = self.post_request(env)
                print(f'Получено сообщение (POST запрос), с данными {request["data"]}')
        if path in self.urls:
            content = self.urls[path]
        else:
            content = PageController404()
        return content(request)

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




