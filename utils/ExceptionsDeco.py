import logging

logger = logging.getLogger(__name__)


def printException(f):
    def new_f(*args, **kwarg):
        try:
            return f(*args, **kwarg)
        except Exception:
            logger.exception('Exception')
    return new_f
