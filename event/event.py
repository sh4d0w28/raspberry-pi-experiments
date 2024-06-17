import RPi.GPIO as GPIO
from functools import wraps
import time
from gdep.LCD144_pins import *

curState = {
    PIN_KEY.K1:1, 
    PIN_KEY.K2:1, 
    PIN_KEY.K3:1, 
    PIN_KEY.UP:1, 
    PIN_KEY.DOWN:1, 
    PIN_KEY.LEFT:1, 
    PIN_KEY.RIGHT:1, 
    PIN_KEY.PRESS:1
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
    wantStop = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Event, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            
            self.listeners = []
            self.wantStop = False

            self.initialized = True

    def reset(self):
        self.listeners = []         

    def register_listener(self, listener):
        self.listeners.append(listener)

    def please_stop(self):
        self.wantStop = True

    @rate_limit(calls_per_second=50)
    def notify(self, pin, state):
        for listener in self.listeners:
            listener(pin, state)

def eventLoop():
    event = Event()
    while not event.wantStop:
        for pin in curState:
            if GPIO.input(pin) != curState[pin]:
                curState[pin] = GPIO.input(pin)
                event.notify(pin, curState[pin])