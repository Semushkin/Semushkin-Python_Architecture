from templator import render
from patterns.creational_petterns import DataBase, Log, MapperRegistry
from patterns.structur_patterns import debug
from patterns.behavioral_patterns import SMSNotify, MailNotify
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork


base = DataBase()
log = Log('test')
sms_notify = SMSNotify()
mail_notify = MailNotify()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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
            category = base.add_category(request['data']['name'])
            category.mark_new()
            UnitOfWork.get_current().commit()
            return render('index.html', object_list=[base.read_base()])


class CategoryDetails:
    @debug
    def __call__(self, request):
        if request['method'] == 'GET':
            category_id = int(request['data']['id'])
            courses = base.courses_by_category_id(category_id)
            category = base.category_by_id(category_id)
            return render('category_details.html',
                          object_list=[courses],
                          id=category_id,
                          name=category.name)


# class CopyCategory:
#     @debug
#     def __call__(self, request):
#         category_id = int(request['data']['id'])
#         if request['method'] == 'GET':
#             base.copy_category(category_id)
#             return render('index.html', object_list=[base.read_base()])


class EditCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            category = base.category_by_id(request['data']['id'])
            category.name = request['data']['name']
            category.mark_dirty()
            UnitOfWork.get_current().commit()
            return render('index.html', object_list=[base.read_base()])
        else:
            category = base.category_by_id(request['data']['id'])
            return render('edit_category.html', object_list=[category])


class CreateCourse:
    @debug
    def __call__(self, request):
        method = request['method']
        category_id = request['data']['id']
        if method == 'GET':
            return render('create_course.html', object_list=[{'content': 'CreateCourse'}], id=category_id)
        elif method == 'POST':
            course = base.add_course(int(category_id), request['data']['name'])
            course.mark_new()
            UnitOfWork.get_current().commit()
            course.observers.append(sms_notify)
            course.observers.append(mail_notify)
            courses = base.courses_by_category_id(int(category_id))
            log.write('Создан курс')
            return render('category_details.html', object_list=[courses], id=category_id)


# class CopyCourse:
#     @debug
#     def __call__(self, request):
#         course_id = int(request['data']['id'])
#         if request['method'] == 'GET':
#             base.copy_course(course_id)
#             return render('index.html', object_list=[base.read_base()])


class EditCourse:
    def __call__(self, request):
        if request['method'] == 'POST':
            course = base.course_by_id(request['data']['id'])
            course.name = request['data']['name']
            course.mark_dirty()
            UnitOfWork.get_current().commit()
            return render('index.html', object_list=[base.read_base()])
        else:
            course = base.course_by_id(request['data']['id'])
            return render('edit_course.html', object_list=[course])


class DeleteCourse:
    def __call__(self, request):
        course = base.course_by_id(request['data']['id'])
        course.mark_removed()
        UnitOfWork.get_current().commit()
        return render('index.html', object_list=[base.read_base()])


class CreateStudent:
    @debug
    def __call__(self, request):
        if request['method'] == 'GET':
            return render('create_student.html', object_list=[{'content': 'CreateCategory'}])
        elif request['method'] == 'POST':
            student = base.add_student(request['data']['name'])
            student.mark_new()
            UnitOfWork.get_current().commit()
            return render('index.html', object_list=[base.read_base()])


class StudentDetails:

    def __call__(self, request):
        base_lst = base.read_base()
        student_id = request['data']['student_id']
        student = base.select_student_by_id(student_id)
        # courses = base.courses_by_student(student_id)
        action = request['data']['status']
        if action == 'new':
            courses_students = base.add_course_student(request['data']['new_course'], student_id)
            courses_students.mark_new()
            UnitOfWork.get_current().commit()
            courses = base.courses_by_student(student_id)
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student.name)
        elif action == 'delete':
            # courses_students = base.add_course_student(request['data']['delete_course'], student_id)
            courses_students = base.courses_students_by_course_id_and_student_id(request['data']['delete_course'], student_id)
            courses_students.mark_removed()
            UnitOfWork.get_current().commit()
            courses = base.courses_by_student(student_id)
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student.name)
        elif action == 'select':
            courses = base.courses_by_student(student_id)
            return render('student_details.html',
                          object_list=[courses],
                          student_id=student.id,
                          name=student.name)


class PageController404:
    @debug
    def __call__(self, request):
        return '404 Page not found!!!'
