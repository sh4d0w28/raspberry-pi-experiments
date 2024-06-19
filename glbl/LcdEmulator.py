import threading
import tkinter as tk
from PIL import Image

from glbl.PinState import PinState
from enums.PinKey import PinKey


class LcdEmulator:

    def start(self):
        self._root.mainloop()

    def text(self, xy, text, fill=(255,255,255,128), font=None):
        tfill = 'white'
        if fill == (255,0,0,128):
            tfill = 'red'
        self._canvas.create_text(xy[0], xy[1], text=text, fill=tfill, font = "Helvetica 7",anchor='nw')
    
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._canvas.create_rectangle(xy[0], xy[1], xy[2], xy[3], outline, width, fill)

    def update(self):
        pass

    def clear(self):
        self._canvas.create_rectangle(0,0,128,128,outline='black', fill='black')

    ############# PRIVATE SECTION ################

    _instance = None
    _root: tk.Tk
    _canvas: tk.Canvas
    _lcd: Image 
    _thread: threading.Thread

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LcdEmulator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            self._lcd = Image.new('RGB', (128, 128))
            self._init()
            self._thread = threading.Thread(target=self._run_root_loop)
            self.initialized = True

    def _run_root_loop(self):
        self._root.mainloop()

    def _init(self):
        self._root = tk.Tk()
        self._root.geometry("300x135")
        self._root.title("WS144")

        buttonKey1 = tk.Button(self._root, text="KEY1_PIN")
        buttonKey2 = tk.Button(self._root, text="KEY2_PIN")
        buttonKey3 = tk.Button(self._root, text="KEY3_PIN")

        buttonKeyDown = tk.Button(self._root, text="V")
        buttonKeyLeft = tk.Button(self._root, text="<")
        buttonKeyPress = tk.Button(self._root, text="*")
        buttonKeyRight = tk.Button(self._root, text=">")
        buttonKeyUp = tk.Button(self._root, text="^")

        buttonKey1.place(width=60, height=20, x=220, y=30)
        buttonKey2.place(width=60, height=20, x=220, y=55)
        buttonKey3.place(width=60, height=20, x=220, y=80)

        buttonKeyUp.place(width=20, height=20, x=35, y=30)
        buttonKeyPress.place(width=20, height=20, x=35, y=55)
        buttonKeyDown.place(width=20, height=20, x=35, y=80)
        buttonKeyLeft.place(width=20, height=20, x=10, y=55)
        buttonKeyRight.place(width=20, height=20, x=60, y=55)

        self._canvas = tk.Canvas(self._root, width=128, height=128, bg="white")
        self._canvas.place(x=85, y=1)

        buttonKey1.bind("<ButtonPress-1>", self._key1pin_prsd)
        buttonKey1.bind("<ButtonRelease-1>", self._key1pin_rlsd)

        buttonKey2.bind("<ButtonPress-1>", self._key2pin_prsd)
        buttonKey2.bind("<ButtonRelease-1>", self._key2pin_rlsd)

        buttonKey3.bind("<ButtonPress-1>", self._key3pin_prsd)
        buttonKey3.bind("<ButtonRelease-1>", self._key3pin_rlsd)

        buttonKeyDown.bind("<ButtonPress-1>", self._keydownpin_prsd)
        buttonKeyDown.bind("<ButtonRelease-1>", self._keydownpin_rlsd)

        buttonKeyLeft.bind("<ButtonPress-1>", self._keyleftpin_prsd)
        buttonKeyLeft.bind("<ButtonRelease-1>", self._keyleftpin_rlsd)

        buttonKeyRight.bind("<ButtonPress-1>", self._keyrightpin_prsd)
        buttonKeyRight.bind("<ButtonRelease-1>", self._keyrightpin_rlsd)

        buttonKeyUp.bind("<ButtonPress-1>", self._keyuppin_prsd)
        buttonKeyUp.bind("<ButtonRelease-1>", self._keyuppin_rlsd)

        buttonKeyPress.bind("<ButtonPress-1>", self._keypresspin_prsd)
        buttonKeyPress.bind("<ButtonRelease-1>", self._keypresspin_rlsd)


    def _key1pin_prsd(self, e): PinState().set(PinKey.K1, 0)
    def _key1pin_rlsd(self, e): PinState().set(PinKey.K1, 1)
    
    def _key2pin_prsd(self, e): PinState().set(PinKey.K2, 0)
    def _key2pin_rlsd(self, e): PinState().set(PinKey.K2, 1)

    def _key3pin_prsd(self, e): PinState().set(PinKey.K3, 0)
    def _key3pin_rlsd(self, e): PinState().set(PinKey.K3, 1)
    
    def _keydownpin_prsd(self, e): PinState().set(PinKey.DOWN, 0)
    def _keydownpin_rlsd(self, e): PinState().set(PinKey.DOWN, 1)

    def _keyuppin_prsd(self, e): PinState().set(PinKey.UP, 0)
    def _keyuppin_rlsd(self, e): PinState().set(PinKey.UP, 1)

    def _keyleftpin_prsd(self, e): PinState().set(PinKey.LEFT, 0)
    def _keyleftpin_rlsd(self, e): PinState().set(PinKey.LEFT, 1)

    def _keyrightpin_prsd(self, e): PinState().set(PinKey.RIGHT, 0)
    def _keyrightpin_rlsd(self, e): PinState().set(PinKey.RIGHT, 1)

    def _keypresspin_prsd(self, e): PinState().set(PinKey.PRESS, 0)
    def _keypresspin_rlsd(self, e): PinState().set(PinKey.PRESS, 1)