def dbConnectAndClose(f):
    def new_f(*args,**kwarg):
        # arrgs[0] represents self, which is the first parameter
        result = None
        try:
            print 'database name', args[0].db.name
            args[0].db.connect()
            print 'database connected'
            print 'call function', f
            result = f(*args,**kwarg)
        except Exception as e:
            print 'Exception occurred'
            args[0].db.rollback()
            raise e
        finally:
            print 'done calling function', f
            args[0].db.close()
            print 'database closed'
        return result
    return new_f