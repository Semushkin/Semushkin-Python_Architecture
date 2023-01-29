

from abc import ABCMeta, abstractmethod


class Observe(metaclass=ABCMeta):
    @abstractmethod
    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for observe in self.observers:
            observe.update(self)


class SMSNotify(Observe):
    def update(self, subject):
        print(f'Рассылка SMS: Изменено наименование курса "{subject.name}"')


class MailNotify(Observe):
    def update(self, subject):
        print(f'Рассылка по e-mail: Изменено наименование курса "{subject.name}"')
