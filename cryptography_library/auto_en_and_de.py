import functools
from full_functions import DES_encrypt, DES_decrypt


def en(key):
    """

    :param key:
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (key, func.__name__))
            if key == '':
                return func(*args, **kw)
            socket = args[0]
            data = args[1]
            return func(socket, DES_encrypt(data, key=key, file=True).encode("utf-8"))

        return wrapper

    return decorator


def de(key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if key == '':
                return func(*args, **kw)
            return DES_decrypt(func(*args, **kw).decode('utf-8'), key=key, file=True)

        return wrapper

    return decorator
