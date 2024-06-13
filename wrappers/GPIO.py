from wrappers.pins import *

states = {
    KEY_UP_PIN: 1,
    KEY_DOWN_PIN: 1,
    KEY_LEFT_PIN: 1,
    KEY_RIGHT_PIN: 1,
    KEY_PRESS_PIN: 1,
    KEY1_PIN: 1,
    KEY2_PIN: 1,
    KEY3_PIN: 1
}

def input(pin):
    return states[pin]
