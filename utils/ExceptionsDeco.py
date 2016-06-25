def printException(f):
    def new_f(*args,**kwarg):
        try:
            return f(*args,**kwarg)
        except Exception as e:
            print '--> Exception', e         
    return new_f
    
    
    
    
