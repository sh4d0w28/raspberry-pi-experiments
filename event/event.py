from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_PRESS_PIN, KEY_RIGHT_PIN, KEY_UP_PIN
import RPi.GPIO as GPIO
from functools import wraps
import time

curState = {
    KEY1_PIN:1, 
    KEY2_PIN:1, 
    KEY3_PIN:1, 
    KEY_DOWN_PIN:1, 
    KEY_LEFT_PIN:1, 
    KEY_PRESS_PIN:1, 
    KEY_RIGHT_PIN:1, 
    KEY_UP_PIN:1
}

def pinstate(pin):
    return curState[pin]

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

# singleton
class Event:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Event, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            
            self.listeners = []

            self.initialized = True

    def reset(self):
        self.listeners = []         

    def register_listener(self, listener):
        self.listeners.append(listener)

    @rate_limit(calls_per_second=50)
    def notify(self, pin, state):
        for listener in self.listeners:
            listener(pin, state)

def eventLoop():
    event = Event()
    while True:
        for pin in curState:
            if GPIO.input(pin) != curState[pin]:
                curState[pin] = GPIO.input(pin)
                event.notify(pin, curState[pin])