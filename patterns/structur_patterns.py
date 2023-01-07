from time import time


def debug(func):
    def wrapper(*args, **kwargs):
        method = str(func)
        view = method[10:method.rfind('.')]
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f'Вызван view "{view}". Время выполнения {(end_time-start_time):2.4f}')
        return result
    return wrapper


if __name__ == '__main__':
    pass
