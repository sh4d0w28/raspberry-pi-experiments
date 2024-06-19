from functools import wraps
import time

def rate_limit(calls_per_second):
    interval = 1.0 / calls_per_second
    
    def decorator(func):
        last_called = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):

            key = str(args[1])
            if key not in last_called:
                last_called[key] = 0.0

            elapsed = time.time() - last_called[key]
            if elapsed < interval:
                return  # Skip the function call
            last_called[key] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator