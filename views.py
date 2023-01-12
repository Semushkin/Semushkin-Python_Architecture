from templator import render
from patterns.creational_petterns import DataBase, Log
from patterns.structur_patterns import debug
from patterns.behavioral_patterns import SMSNotify, MailNotify


base = DataBase()
log = Log('test')
sms_notify = SMSNotify()
mail_notify = MailNotify()


class PageControllerMain:
    @debug
    def __call__(self, request):
        return render('index.html', object_list=[base.read_base()])


class PageControllerAbout:
    @debug
    def __call__(self, request):
        return render('about.html', object_list=[{'content': 'About us'}])


class PageControllerContacts:
    @debug
    def __call__(self, request):
        return render('contacts.html', object_list=[{'content': 'Contacts'}])


class CreateCategory:
    @debug
    def __call__(self, request):
        if request['method'] == 'GET':
            return render('create_category.html', object_list=[{'content': 'CreateCategory'}])
        elif request['method'] == 'POST':
            log.write('Создана категория')
            base.add_category(request['data']['name'])
            return render('index.html', object_list=[base.read_base()])


class CategoryDetails:
    @debug
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
    @debug
    def __call__(self, request):
        category_id = int(request['data']['id'])
        if request['method'] == 'GET':
            base.copy_category(category_id)
            return render('index.html', object_list=[base.read_base()])


class CreateCourse:
    @debug
    def __call__(self, request):
        method = request['method']
        category_id = request['data']['id']
        if method == 'GET':
            return render('create_course.html', object_list=[{'content': 'CreateCourse'}], id=category_id)
        elif method == 'POST':
            course = base.add_course(request['data']['name'], int(category_id))
            course.observers.append(sms_notify)
            course.observers.append(mail_notify)
            courses = base.courses_by_category_id(int(category_id))
            log.write('Создан курс')
            return render('category_details.html', object_list=[courses], id=category_id)


class CopyCourse:
    @debug
    def __call__(self, request):
        course_id = int(request['data']['id'])
        if request['method'] == 'GET':
            base.copy_course(course_id)
            return render('index.html', object_list=[base.read_base()])


class EditCourse:
    def __call__(self, request):
        data = {}
        method = request['method']
        data['course_id'] = request['data']['id']
        if method == 'GET':
            data = {
                'course_id': request['data']['id'],
                'name': base.name_course_by_id(int(request['data']['id']))
            }
            return render('edit_course.html', object_list=[data])
        elif method == 'POST':
            base.edit_course(request['data']['id'], request['data']['name'])
            return render('index.html', object_list=[base.read_base()])


class CreateStudent:
    @debug
    def __call__(self, request):
        method = request['method']
        if method == 'GET':
            return render('create_student.html', object_list=[{'content': 'CreateStudent'}])
        elif method == 'POST':
            base.add_student(request['data']['name'])
            return render('index.html', object_list=[base.read_base()])


class StudentDetails:

    def __call__(self, request):
        student = base.select_student_by_id(request['data']['student_id'])
        student_name = base.student_name_by_id(request['data']['student_id'])
        action = request['data']['status']
        if action == 'new':
            student.add_course(request['data']['new_course'])
            courses = base.courses_for_students(request['data']['student_id'])
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student_name)
        elif action == 'delete':
            student.leave_course(request['data']['delete_course'])
            courses = base.courses_for_students(request['data']['student_id'])
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student_name)
        elif action == 'select':
            courses = base.courses_for_students(request['data']['student_id'])
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student_name)


class PageController404:
    @debug
    def __call__(self, request):
        return '404 Page not found!!!'
