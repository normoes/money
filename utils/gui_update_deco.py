def gui_show_entries(f):
    def new_f(*args, **kwarg):
        # arrgs[0] represents self, which is the first parameter
        result = None
        print 'args:', args
        print 'kwargs:', kwarg
        if args:
            f(*args, **kwarg)
            args[0].show_entries()
        else:
            print 'no self (class) given'
        return result
    return new_f


def gui_populate_categories(f):
    def new_f(*args, **kwarg):
        # arrgs[0] represents self, which is the first parameter
        result = None
        print 'args:', args
        print 'kwargs:', kwarg
        if args:
            f(*args, **kwarg)
            args[0].populate_categories()
        else:
            print 'no self (class) given'
        return result
    return new_f
