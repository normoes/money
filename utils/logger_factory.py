

def get_logger(name):
    import logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def get_child_logger(parent_logger, name):
    if not parent_logger:
        raise ValueError('cannot get child logger without parent logger')
    logger = parent_logger.getChild(name)
    return logger


def get_file_handler(file_name):
    from logging import Formatter
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler(file_name, maxBytes=1000000, backupCount=2)
    formatter = Formatter('--------------------------------------------------------------------------------\n %(asctime)s, %(msecs)d %(name)s %(levelname)s [%(pathname)s:%(lineno)d]  - %(message)s\n--------------------------------------------------------------------------------')
    handler.setFormatter(formatter)
    return handler


def get_console_handler():
    from logging import StreamHandler
    from logging import Formatter
    handler = StreamHandler()
    formatter = Formatter('--------------------------------------------------------------------------------\n %(asctime)s, %(msecs)d %(name)s %(levelname)s [%(pathname)s:%(lineno)d]  - %(message)s\n--------------------------------------------------------------------------------')
    handler.setFormatter(formatter)
    return handler


def get_file_logger(name):
    logger = get_logger(name=name)
    logger.addHandler(get_file_handler(file_name=name + '.log'))
    return logger


def get_console_logger(name):
    logger = get_logger(name=name)
    logger.addHandler(get_console_handler())
    return logger


def get_file_and_console_logger(name):
    logger = get_file_logger(name=name)
    logger.addHandler(get_console_handler())
    return logger
