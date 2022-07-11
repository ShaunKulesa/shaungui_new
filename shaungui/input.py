import copy

import glfw.GLFW
import glfw

keys = {
"A": glfw.KEY_A,
"B": glfw.KEY_B,
"C": glfw.KEY_C,
"D": glfw.KEY_D,
"E": glfw.KEY_E,
"F": glfw.KEY_F,
"G": glfw.KEY_G,
"H": glfw.KEY_H,
"I": glfw.KEY_I,
"J": glfw.KEY_J,
"K": glfw.KEY_K,
"L": glfw.KEY_L,
"M": glfw.KEY_M,
"N": glfw.KEY_N,
"O": glfw.KEY_O,
"P": glfw.KEY_P,
"Q": glfw.KEY_Q,
"R": glfw.KEY_R,
"S": glfw.KEY_S,
"T": glfw.KEY_T,
"U": glfw.KEY_U,
"V": glfw.KEY_V,
"W": glfw.KEY_W,
"X": glfw.KEY_X,
"Y": glfw.KEY_Y,
"Z": glfw.KEY_Z,

"0": glfw.KEY_0,
"1": glfw.KEY_1,
"2": glfw.KEY_2,
"3": glfw.KEY_3,
"4": glfw.KEY_4,
"5": glfw.KEY_5,
"6": glfw.KEY_6,
"7": glfw.KEY_7,
"8": glfw.KEY_8,
"9": glfw.KEY_9,

"KEY_PAD_0": glfw.KEY_KP_0,
"KEY_PAD_1": glfw.KEY_KP_1,
"KEY_PAD_2": glfw.KEY_KP_2,
"KEY_PAD_3": glfw.KEY_KP_3,
"KEY_PAD_4": glfw.KEY_KP_4,
"KEY_PAD_5": glfw.KEY_KP_5,
"KEY_PAD_6": glfw.KEY_KP_6,
"KEY_PAD_7": glfw.KEY_KP_7,
"KEY_PAD_8": glfw.KEY_KP_8,
"KEY_PAD_9": glfw.KEY_KP_9,

"UP_ARROW": glfw.KEY_UP,
"DOWN_ARROW": glfw.KEY_DOWN,
"LEFT_ARROW": glfw.KEY_LEFT,
"RIGHT_ARROW": glfw.KEY_RIGHT,

"SPACE": glfw.KEY_SPACE,
"ENTER": glfw.KEY_ENTER,
"ESCAPE": glfw.KEY_ESCAPE,
"BACKSPACE": glfw.KEY_BACKSPACE,
"TAB": glfw.KEY_TAB,
}

class Input:
    def __init__(self, window):
        self.window = window

        self.keys_pressed = {}

        self._key_events = []

        glfw.set_key_callback(self.window, self._key_callback)

    def key_events(self):
        key_events = copy.copy(self._key_events)
        self._key_events.clear()
        return key_events

    def key_pressed(self, key: int):
        if key not in self.keys_pressed:
            return False

        # Return the state of the key (pressed or released)
        return self.keys_pressed[key]

    def _key_callback(self, window, key: int, scan_code: int, action: int, mods: int):
        for key_str, key_code in keys.items():
            if key_code == key:
                key = key_str
                
        # Set the state of the key (pressed or released)
        if action == glfw.GLFW.GLFW_PRESS:
            self.keys_pressed[key] = True
            self._key_events.append((key, True))
            
        elif action == glfw.GLFW.GLFW_RELEASE:
            self.keys_pressed[key] = False
            self._key_events.append((key, False))