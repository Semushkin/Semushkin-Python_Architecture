from templator import render
from patterns.petterns import DataBase, Log


base = DataBase()
log = Log('test')


class PageControllerMain:
    def __call__(self, request):
        return render('index.html', object_list=[base.read_base()])


class PageControllerAbout:
    def __call__(self, request):
        return render('about.html', object_list=[{'content': 'About us'}])


class PageControllerContacts:
    def __call__(self, request):
        return render('contacts.html', object_list=[{'content': 'Contacts'}])


class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'GET':
            return render('create_category.html', object_list=[{'content': 'CreateCategory'}])
        elif request['method'] == 'POST':
            log.write('Создана категория')
            base.add_category(request['data']['name'])
            return render('index.html', object_list=[base.read_base()])


class CategoryDetails:
    def __call__(self, request):
        if request['method'] == 'GET':
            category_id = int(request['data']['id'])
            courses = base.courses_by_category_id(category_id)
            name = base.name_category_by_id(category_id)
            return render('category_details.html',
                          object_list=[courses],
                          id=category_id,
                          name=name)


class CopyCategory:
    def __call__(self, request):
        category_id = int(request['data']['id'])
        if request['method'] == 'GET':
            base.copy_category(category_id)
            return render('index.html', object_list=[base.read_base()])


class CreateCourse:
    def __call__(self, request):
        method = request['method']
        category_id = request['data']['id']
        if method == 'GET':
            return render('create_course.html', object_list=[{'content': 'CreateCourse'}], id=category_id)
        elif method == 'POST':
            base.add_course(request['data']['name'], int(category_id))
            courses = base.courses_by_category_id(int(category_id))
            log.write('Создан курс')
            return render('category_details.html', object_list=[courses], id=category_id)


class CopyCourse:
    def __call__(self, request):
        course_id = int(request['data']['id'])
        if request['method'] == 'GET':
            base.copy_course(course_id)
            return render('index.html', object_list=[base.read_base()])


class CreateStudent:
    def __call__(self, request):
        method = request['method']
        if method == 'GET':
            return render('create_student.html', object_list=[{'content': 'CreateStudent'}])
        elif method == 'POST':
            base.add_student(request['data']['name'])
            return render('index.html', object_list=[base.read_base()])


class PageController404:
    def __call__(self, request):
        return '404 Page not found!!!'
