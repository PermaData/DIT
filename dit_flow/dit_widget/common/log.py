def begin(file, function):
    with open(file, 'w') as log:
        pass

def value(file, strings):
    pass

def finish(file, function):
    pass
    
def decorator(function):
    def decorated(*args, **kwargs):
        begin(args[-1], function)
        function(*args, **kwargs)
        end(args[-1], function)
