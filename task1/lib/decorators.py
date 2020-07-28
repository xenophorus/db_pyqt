import sys
import inspect
import lib.logger
import logging


if 'client.py' in str(sys.argv):
    log = logging.getLogger('client.app')
else:
    log = logging.getLogger('server.app')


def log_dec(f):
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        log.debug(f'Отработала фуккция {f.__name__} с параметрами {args, kwargs}'
                  f'\n\t\tвызванная {inspect.stack()[1][3]}')

    return wrapper
