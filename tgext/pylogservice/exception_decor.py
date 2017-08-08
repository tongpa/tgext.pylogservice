def exception(logger,extraLog=None):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
    print logger
    def decorator(func):
        print "call decorator"
        def wrapper(*args, **kwargs):
            print "call exception decor"
            print args
            print kwargs
            try:
                print "-----: normal"
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                #logger.exception(err)
                print "-----: except"
                logger.exception(err,extra=extraLog)
            # re-raise the exception
            raise
        return wrapper
    return decorator