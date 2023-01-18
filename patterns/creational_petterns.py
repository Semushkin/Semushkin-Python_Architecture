from tabulate import tabulate
from copy import deepcopy
from patterns.behavioral_patterns import Subject
from patterns.architectural_system_pattern_unit_of_work import DomainObject
import DB_Errors
from sqlite3 import connect

connection = connect('DataBase.sqlite')


# Прототип
class PrototypeCategoryCourse:

    def clone(self):
        return deepcopy(self)


class Category(PrototypeCategoryCourse, DomainObject):

    def __init__(self, name):
        self.id = 0
        self.name = name
        self.courses_count = 0


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'categories'

    def insert(self, category):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (category.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCategoryInsertException(e.args)

    def update(self, category):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (category.name, category.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCategoryUpdateException(e.args)

    def delete(self, category):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (category.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCategoryDeleteException(e.args)

    def select_all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def select_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            id, name = result
            category = Category(name)
            category.id = id
            return category
        else:
            raise DB_Errors.DBCategorySelectException(f'Category with id={id} not found')


class CourseOffline:
    def __init__(self, course, address):
        self.course = course
        self.address = address


class CourseOnline:
    pass


class Course(PrototypeCategoryCourse, Subject, DomainObject):
    course_type = {
        'Online': CourseOnline,
        'Ofline': CourseOffline
    }

    def __init__(self, category_id, name):
        self.id = 0
        self.name = name
        self.category_id = category_id
        super().__init__()

    def change_course(self, new_name):
        self.name = new_name
        self.notify()


class CourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'courses'

    def insert(self, course):
        statement = f'INSERT INTO {self.table_name} (category_id, name) VALUES (?, ?)'
        self.cursor.execute(statement, (course.category_id, course.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCoursesInsertException(e.args)

    def update(self, course):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (course.name, course.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCoursesUpdateException(e.args)

    def delete(self, course):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCategoryDeleteException(e.args)

    def select_all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, category_id, name = item
            category = Course(category_id, name)
            category.id = id
            result.append(category)
        return result

    def select_by_id(self, course_id):
        statement = f"SELECT id, category_id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (course_id,))
        result = self.cursor.fetchone()
        if result:
            id, category_id, name = result
            course = Course(category_id, name)
            course.id = id
            return course
        else:
            raise DB_Errors.DBCoursesSelectException(f'Course with id={course_id} not found')

    def select_course_by_category_id(self, category_id):
        statement = f'SELECT id, category_id, name FROM {self.table_name} WHERE category_id=?'
        self.cursor.execute(statement, (category_id,))
        result = []
        for item in self.cursor.fetchall():
            id, category_id, name = item
            course = Course(category_id, name)
            course.id = id
            result.append(course)
        return result

    def count_course_by_category_id(self, category_id):
        statement = f'SELECT id, category_id, name FROM {self.table_name} WHERE category_id=?'
        self.cursor.execute(statement, (category_id,))
        result = len(self.cursor.fetchall())
        return result


class CourseStudent(DomainObject):

    def __init__(self, course_id, student_id):
        self.id = 0
        self.course_id = course_id
        self.student_id = student_id


class CourseStudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'courses_students'

    def insert(self, courses_students):
        statement = f'INSERT INTO {self.table_name} (course_id, student_id) VALUES (?, ?)'
        self.cursor.execute(statement, (courses_students.course_id, courses_students.student_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCoursesInsertException(e.args)

    def update(self, courses_students):
        statement = f"UPDATE {self.table_name} SET course_id=? WHERE student_id=?"

        self.cursor.execute(statement, (courses_students.course_id, courses_students.student_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCoursesUpdateException(e.args)

    def delete(self, courses_students):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (courses_students.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBCategoryDeleteException(e.args)

    def select_all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, course_id, student_id = item
            courses_students = CourseStudent(course_id, student_id)
            courses_students.id = id
            result.append(courses_students)
        return result

    def select_by_id(self, courses_students_id):
        statement = f"SELECT id, course_id, student_id FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (courses_students_id,))
        result = self.cursor.fetchone()
        if result:
            id, course_id, student_id = result
            courses_students = CourseStudent(course_id, student_id)
            courses_students.id = id
            return courses_students
        else:
            raise DB_Errors.DBCategorySelectException(f'CoursesStudents with id={courses_students_id} not found')

    def select_by_student_id(self, student_id):
        statement = f'SELECT id, course_id, student_id FROM {self.table_name} WHERE student_id=?'
        self.cursor.execute(statement, (student_id,))
        result = []
        for item in self.cursor.fetchall():
            id, course_id, student_id = item
            courses_students = CourseStudent(course_id, student_id)
            courses_students.id = id
            result.append(courses_students)
        return result

    def courses_students_by_course_id_and_student_id(self, course_id, student_id):
        statement = f"SELECT id, course_id, student_id FROM {self.table_name} WHERE course_id=? AND student_id =?"
        self.cursor.execute(statement, (course_id, student_id))
        result = self.cursor.fetchone()
        if result:
            id, course_id, student_id = result
            courses_students = CourseStudent(course_id, student_id)
            courses_students.id = id
            return courses_students
        else:
            raise DB_Errors.DBCategorySelectException(f'CoursesStudents with course_id={course_id} and student_id={student_id} not found')


class Student(DomainObject):

    def __init__(self, name):
        self.id = 0
        self.name = name
        super().__init__()


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'students'

    def insert(self, student):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (student.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBStudentsInsertException(e.args)

    def update(self, student):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (student.name, student.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBStudentsUpdateException(e.args)

    def delete(self, student):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (student.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DB_Errors.DBStudentsDeleteException(e.args)

    def select_all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def select_by_id(self, student_id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (student_id,))
        result = self.cursor.fetchone()
        if result:
            id, name = result
            student = Student(name)
            student.id = id
            return student
        else:
            raise DB_Errors.DBStudentsSelectException(f'Student with id={student_id} not found')


class MapperRegistry:
    mappers = {
        'categories': CategoryMapper,
        'courses': CourseMapper,
        'students': StudentMapper,
        'courses_students': CourseStudentMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)
        elif isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, CourseStudent):
            return CourseStudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DataBase:

    @staticmethod
    def read_base():
        mapper_category = MapperRegistry.get_current_mapper('categories')
        mapper_course = MapperRegistry.get_current_mapper('courses')
        mapper_student = MapperRegistry.get_current_mapper('students')
        categories = mapper_category.select_all()
        for category in categories:
            count_courses = mapper_course.count_course_by_category_id(category.id)
            category.courses_count = count_courses
        courses = mapper_course.select_all()
        for course in courses:
            course.category_id = mapper_category.select_by_id(course.category_id).name

        data = {
            'categories': categories,
            'courses': courses,
            'students': mapper_student.select_all()
        }
        return data

    @staticmethod
    def add_category(name):
        category = Category(name)
        return category

    @staticmethod
    def category_by_id(category_id):
        mapper_category = MapperRegistry.get_current_mapper('categories')
        return mapper_category.select_by_id(category_id)

    @staticmethod
    def add_course(name, category_id):
        course = Course(name, category_id)
        return course

    @staticmethod
    def course_by_id(courses_id):
        mapper_course = MapperRegistry.get_current_mapper('courses')
        return mapper_course.select_by_id(courses_id)

    @staticmethod
    def courses_by_category_id(category_id):
        mapper_course = MapperRegistry.get_current_mapper('courses')
        return mapper_course.select_course_by_category_id(category_id)

    @staticmethod
    def add_course_student(course_id, student_id):
        courses_students = CourseStudent(course_id, student_id)
        return courses_students

    @staticmethod
    def courses_students_by_course_id_and_student_id(course_id, student_id):
        mapper_course_students = MapperRegistry.get_current_mapper('courses_students')
        return mapper_course_students.courses_students_by_course_id_and_student_id(course_id, student_id)

    @staticmethod
    def courses_by_student(student_id):
        mapper_course_students = MapperRegistry.get_current_mapper('courses_students')
        mapper_course = MapperRegistry.get_current_mapper('courses')
        courses_students = mapper_course_students.select_by_student_id(student_id)
        courses = mapper_course.select_all()
        selected = []
        not_selected = []
        for course in courses:
            exist = False
            for item in courses_students:
                if item.course_id == course.id:
                    selected.append(course)
                    exist = True
            if not exist:
                not_selected.append(course)
        result = {
            'selected': selected,
            'not_selected': not_selected
        }
        return result

    @staticmethod
    def add_student(name):
        student = Student(name)
        return student

    @staticmethod
    def select_student_by_id(student_id):
        mapper_student = MapperRegistry.get_current_mapper('students')
        return mapper_student.select_by_id(student_id)


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
    pass
