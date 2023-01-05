from views import PageControllerMain, PageControllerContacts, \
    PageControllerAbout, CreateCategory, CategoryDetails, \
    CreateCourse, CopyCategory, CreateStudent, CopyCourse

URLS = {
    '/': PageControllerMain(),
    '/about': PageControllerAbout(),
    '/contacts': PageControllerContacts(),
    '/create_category': CreateCategory(),
    '/category_details': CategoryDetails(),
    '/create_course': CreateCourse(),
    '/copy_category': CopyCategory(),
    '/create_student': CreateStudent(),
    '/copy_course': CopyCourse()
}
