from simple_wsgi import page_controller_main, page_controller_contacts, page_controller_about

URLS = {
    '/': page_controller_main(),
    '/about': page_controller_about(),
    '/contacts': page_controller_contacts(),
}