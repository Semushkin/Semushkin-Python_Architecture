from tabulate import tabulate
from copy import deepcopy


# Прототип
class PrototypeCategoryCourse:

    def clone(self):
        return deepcopy(self)


class Category(PrototypeCategoryCourse):
    count = 0

    def __init__(self, name):
        self.name = name
        self.courses_count = 0
        Category.count += 1
        self.id = Category.count


class CourseOffline:
    def __init__(self, course, address):
        self.course = course
        self.address = address


class CourseOnline:
    pass


class Course(PrototypeCategoryCourse):
    count = 0
    course_type = {
        'Online': CourseOnline,
        'Ofline': CourseOffline
    }

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id
        Course.count += 1
        self.id = Course.count


class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1
        self.id = Student.count


class DataBase:
    def __init__(self):
        self.categories = []
        self.courses = []
        self.students = []

    def print_base(self):
        return f'Category count: {len(self.categories)}\n' \
               f'Courses count: {len(self.courses)}\n' \
               f'Students count: {len(self.students)}'

    def read_base(self):
        data = {
            'categories': self.category_list(),
            'courses': self.course_list(),
            'students': self.students
        }
        return data

    def add_category(self, name):
        category = Category(name)
        self.categories.append(category)
        return category

    def copy_category(self, category_id):
        for cat in self.categories:
            if int(cat.id) == category_id:
                cat_copy = cat.clone()
                Category.count += 1
                cat_copy.id = Category.count
                self.categories.append(cat_copy)
                return

    def category_list(self):
        cat_lst = []
        for item in self.categories:
            cat_lst.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'courses': self.count_courses(item.id)
                }
            )
        return cat_lst

    def name_category_by_id(self, category_id):
        for item in self.categories:
            if item.id == category_id:
                return item.name

    def count_courses(self, category_id):
        result = 0
        for item in self.courses:
            if item.category_id == category_id:
                result += 1
        return result

    def add_course(self, name, category_id):
        course = Course(name, category_id)
        self.courses.append(course)
        return course

    def copy_course(self, corse_id):
        for course in self.courses:
            if int(course.id) == corse_id:
                course_copy = course.clone()
                Course.count += 1
                course_copy.id = Course.count
                self.courses.append(course_copy)
                return

    def courses_by_category_id(self, category_id):
        result = []
        if self.courses:
            for item in self.courses:
                if item.category_id == category_id:
                    result.append(item)
        return result

    def course_list(self):
        cour_lst = []
        for item in self.courses:
            cour_lst.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'category': self.name_category_by_id(int(item.category_id))
                }
            )
        return cour_lst

    def add_student(self, name):
        student = Student(name)
        self.students.append(student)
        return student

    def print_categories(self):
        result = {}
        id = []
        name = []
        for item in self.categories:
            id.append(item.id)
            name.append(item.name)
        result['id'] = id
        result['name'] = name
        print(f'List of categories (total count: {Category.count})\n{tabulate(result, headers="keys")}')

    def print_courses(self):
        result = {}
        id = []
        name = []
        category = []
        for item in self.courses:
            id.append(item.id)
            name.append(item.name)
            category.append(item.category_id)
        result['id'] = id
        result['name'] = name
        result['category'] = category
        print(f'List of cuorses (total count: {Course.count})\n{tabulate(result,  headers="keys")}')


#Синглтон
class Singleton(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args):
        name = args[0]
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args)
            return cls.__instance[name]


class Log(metaclass=Singleton):

    def __init__(self, name):
        self.name = name
        self.log_file = []

    def write(self, text):
        print(f'log "{self.name}" write - {text}')
        self.log_file.append(text)

    def read(self):
        return self.log_file

if __name__ == '__main__':
    x = Log('test')
    y = Log('test_2')
    z = Log('test')

    print(x)
    print(y)
    print(z)
    print('----------------------------------')
    x.write('что то происходит')
    x.write('что то происходит 2')
    x.write('что то происходит 3')

    y.write('что то происходит')

    print(x.read())
    print(y.read())
    print(z.read())