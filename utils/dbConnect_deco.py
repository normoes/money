import logging

logger = logging.getLogger(__name__)


def dbConnectAndClose(f):
    def new_f(*args, **kwarg):
        # arrgs[0] represents self, which is the first parameter
        result = None
        if args:
            if not args[0].database:
                raise ValueError('database object missing')
            logger.debug('database name: {}'.format(args[0].database_name))
            try:
                args[0].database.connect()
                logger.debug('database connected')
                # print 'call function', f
                result = f(*args, **kwarg)
            except Exception:  # TODO group exception types
                logger.exception('Exception')
                args[0].database.rollback()
            finally:
                args[0].database.close()
                logger.debug('database closed')
        else:
            logger.warn('no self (class) given')
        return result
    return new_f
