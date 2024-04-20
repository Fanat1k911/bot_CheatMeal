import time
import math
import functools


# декоратор для подсчета временных затрат для выполнения функции
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {round(end_time - start_time, 3)} секунды")
        return result

    return wrapper
