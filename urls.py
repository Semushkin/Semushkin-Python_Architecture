from views import PageControllerMain, PageControllerContacts, \
    PageControllerAbout, CreateCategory, CategoryDetails, \
    CreateCourse, CreateStudent, \
    EditCourse, StudentDetails, DeleteCourse, EditCategory

URLS = {
    '/': PageControllerMain(),
    '/about': PageControllerAbout(),
    '/contacts': PageControllerContacts(),
    '/create_category': CreateCategory(),
    '/category_details': CategoryDetails(),
    '/edit_category': EditCategory(),
    '/create_course': CreateCourse(),
    # '/copy_category': CopyCategory(),
    '/create_student': CreateStudent(),
    # '/copy_course': CopyCourse(),
    '/edit_course': EditCourse(),
    '/course_delete': DeleteCourse(),
    '/student_details': StudentDetails(),
}
