import tkinter as tk
import threading

from wrappers.pins import *
from wrappers.GPIO import states
from PIL import Image

def key1pin_prsd(e): states[KEY1_PIN] = 1
def key1pin_rlsd(e): states[KEY1_PIN] = 0
def key2pin_prsd(e): states[KEY2_PIN] = 1
def key2pin_rlsd(e): states[KEY2_PIN] = 0
def key3pin_prsd(e): states[KEY3_PIN] = 1
def key3pin_rlsd(e): states[KEY3_PIN] = 0
def keydownpin_prsd(e): states[KEY_DOWN_PIN] = 1
def keydownpin_rlsd(e): states[KEY_DOWN_PIN] = 0
def keyuppin_prsd(e): states[KEY_UP_PIN] = 1
def keyuppin_rlsd(e): states[KEY_UP_PIN] = 0
def keyleftpin_prsd(e): states[KEY_LEFT_PIN] = 1
def keyleftpin_rlsd(e): states[KEY_LEFT_PIN] = 0
def keyrightpin_prsd(e): states[KEY_RIGHT_PIN] = 1
def keyrightpin_rlsd(e): states[KEY_RIGHT_PIN] = 0
def keypresspin_prsd(e): states[KEY_PRESS_PIN] = 1
def keypresspin_rlsd(e): states[KEY_PRESS_PIN] = 0

class LCD_LCD144:

    canvas: tk.Canvas
    image = Image.new('RGB', (128, 128))

    class draw:

        cnvs: tk.Canvas

        def __init__(self, cnvs) -> None: cnvs = cnvs

        def rectangle(self, coords, outline, fill):
            self.cnvs.create_rectangle(coords[0], coords[1], coords[2], coords[3], outline="blue", width=1, fill="lightblue")
            print(coords,outline,fill)
        
        def text(coords, text, fill):
            print(coords, text, fill)

    class disp:

        def LCD_ShowImage(image, x, y):
            print(image, x, y)

    def init(self):
        draw

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

        self.canvas = tk.Canvas(root, width=128, height=128, bg="white")
        self.canvas.place(x=85, y=1)

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

        # Run the Tkinter event loop
        root.mainloop()

    def __init__(self):
        thread1 = threading.Thread(target=self.init)
        thread1.start()