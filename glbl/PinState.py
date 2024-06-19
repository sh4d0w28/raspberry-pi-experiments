from enums.PinKey import PinKey

class PinState:

    def all(self):
        return self.curState

    def get(self, pin: PinKey):
        return self.curState[pin]
    
    def set(self, pin: PinKey, state: int):
        self.curState[pin] = state
        print('set ', self.curState)

    ############# PRIVATE SECTION ################

    _instance = None
    _curState = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PinState, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            self.curState = {
                PinKey.K1:1, 
                PinKey.K2:1, 
                PinKey.K3:1, 
                PinKey.UP:1, 
                PinKey.DOWN:1, 
                PinKey.LEFT:1, 
                PinKey.RIGHT:1, 
                PinKey.PRESS:1
            }
            self.initialized = True
    