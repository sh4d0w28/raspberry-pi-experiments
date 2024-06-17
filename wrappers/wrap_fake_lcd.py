import threading
import tkinter as tk
from PIL import Image
from gdep.LCD144_pins import PIN_KEY

states = []

def key1pin_prsd(e): states[PIN_KEY.K1] = 1
def key1pin_rlsd(e): states[PIN_KEY.K1] = 0
def key2pin_prsd(e): states[PIN_KEY.K2] = 1
def key2pin_rlsd(e): states[PIN_KEY.K2] = 0
def key3pin_prsd(e): states[PIN_KEY.K3] = 1
def key3pin_rlsd(e): states[PIN_KEY.K3] = 0
def keydownpin_prsd(e): states[PIN_KEY.DOWN] = 1
def keydownpin_rlsd(e): states[PIN_KEY.DOWN] = 0
def keyuppin_prsd(e): states[PIN_KEY.UP] = 1
def keyuppin_rlsd(e): states[PIN_KEY.UP] = 0
def keyleftpin_prsd(e): states[PIN_KEY.LEFT] = 1
def keyleftpin_rlsd(e): states[PIN_KEY.LEFT] = 0
def keyrightpin_prsd(e): states[PIN_KEY.RIGHT] = 1
def keyrightpin_rlsd(e): states[PIN_KEY.RIGHT] = 0
def keypresspin_prsd(e): states[PIN_KEY.PRESS] = 1
def keypresspin_rlsd(e): states[PIN_KEY.PRESS] = 0


#singleton
class wrap_fake_LCD:

    _instance = None
    _canvas: tk.Canvas
    _lcd: Image 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(wrap_fake_LCD, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            self._lcd = Image.new('RGB', (128, 128))

            thread1 = threading.Thread(target=self.init)
            thread1.start()

            self.initialized = True

    def init(self):
        root = tk.Tk()
        root.geometry("300x130")
        root.title("WS144")

        buttonKey1 = tk.Button(root, text="KEY1_PIN")
        buttonKey2 = tk.Button(root, text="KEY2_PIN")
        buttonKey3 = tk.Button(root, text="KEY3_PIN")

        buttonKeyDown = tk.Button(root, text="V")
        buttonKeyLeft = tk.Button(root, text="<")
        buttonKeyPress = tk.Button(root, text="*")
        buttonKeyRight = tk.Button(root, text=">")
        buttonKeyUp = tk.Button(root, text="^")

        buttonKey1.place(width=60, height=20, x=220, y=30)
        buttonKey2.place(width=60, height=20, x=220, y=55)
        buttonKey3.place(width=60, height=20, x=220, y=80)

        buttonKeyUp.place(width=20, height=20, x=35, y=30)
        buttonKeyPress.place(width=20, height=20, x=35, y=55)
        buttonKeyDown.place(width=20, height=20, x=35, y=80)
        buttonKeyLeft.place(width=20, height=20, x=10, y=55)
        buttonKeyRight.place(width=20, height=20, x=60, y=55)

        self._canvas = tk.Canvas(root, width=128, height=128, bg="white")
        self._canvas.place(x=85, y=1)

        buttonKey1.bind("<ButtonPress-1>", key1pin_prsd)
        buttonKey1.bind("<ButtonRelease-1>", key1pin_rlsd)

        buttonKey2.bind("<ButtonPress-1>", key2pin_prsd)
        buttonKey2.bind("<ButtonRelease-1>", key2pin_rlsd)

        buttonKey3.bind("<ButtonPress-1>", key3pin_prsd)
        buttonKey3.bind("<ButtonRelease-1>", key3pin_rlsd)

        buttonKeyDown.bind("<ButtonPress-1>", keydownpin_prsd)
        buttonKeyDown.bind("<ButtonRelease-1>", keydownpin_rlsd)

        buttonKeyLeft.bind("<ButtonPress-1>", keyleftpin_prsd)
        buttonKeyLeft.bind("<ButtonRelease-1>", keyleftpin_rlsd)

        buttonKeyRight.bind("<ButtonPress-1>", keyrightpin_prsd)
        buttonKeyRight.bind("<ButtonRelease-1>", keyrightpin_rlsd)

        buttonKeyUp.bind("<ButtonPress-1>", keyuppin_prsd)
        buttonKeyUp.bind("<ButtonRelease-1>", keyuppin_rlsd)

        buttonKeyPress.bind("<ButtonPress-1>", keypresspin_prsd)
        buttonKeyPress.bind("<ButtonRelease-1>", keypresspin_rlsd)
        root.mainloop()

    def text(self, xy, text, fill=(255,255,255,128), font=None):
        self._canvas.create_text(xy[0], xy[1], text, fill, font)
    
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._canvas.create_rectangle(xy[0], xy[1], xy[2], xy[3], outline, width, fill)

    def update(self):
        pass

    def clear(self):
        self._canvas.create_rectangle(0,0,200,200,fill="white")
