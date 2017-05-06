def dbConnectAndClose(f):
    def new_f(*args,**kwarg):
        # arrgs[0] represents self, which is the first parameter
        result = None
        print args
        print kwarg
        if args:
            try:
                print 'database name', args[0].database.name
                args[0].database.connect()
                print 'database connected'
                print 'call function', f
                result = f(*args,**kwarg)
            except Exception as e:
                print 'Exception occurred'
                args[0].database.rollback()
                raise e
            finally:
                print 'done calling function', f
                args[0].database.close()
                print 'database closed'
        else:
            pass
        return result
    return new_f
