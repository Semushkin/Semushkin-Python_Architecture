class DBCategoryInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'Create Category Error: {message}')


class DBCategoryUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update Category Error: {message}')


class DBCategoryDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete Category Error: {message}')


class DBCategorySelectException(Exception):
    def __init__(self, message):
        super().__init__(f'Select Category Error: {message}')


class DBCoursesInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'Create Courses Error: {message}')


class DBCoursesUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update Courses Error: {message}')


class DBCoursesDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete Courses Error: {message}')


class DBCoursesSelectException(Exception):
    def __init__(self, message):
        super().__init__(f'Select Courses Error: {message}')


class DBStudentsInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'Create Students Error: {message}')


class DBStudentsUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update Students Error: {message}')


class DBStudentsDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete Students Error: {message}')


class DBStudentsSelectException(Exception):
    def __init__(self, message):
        super().__init__(f'Select Students Error: {message}')

###################################################################
class DBCoursesStudentsInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'Create CoursesStudents Error: {message}')


class DBCoursesStudentsUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update CoursesStudents Error: {message}')


class DBCoursesStudentsDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete CoursesStudents Error: {message}')


class DBCoursesStudentsSelectException(Exception):
    def __init__(self, message):
        super().__init__(f'Select CoursesStudents Error: {message}')