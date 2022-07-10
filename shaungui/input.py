import copy

import glfw.GLFW


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
        # Set the state of the key (pressed or released)
        if action == glfw.GLFW.GLFW_PRESS:
            self.keys_pressed[key] = True
            self._key_events.append((key, True))
        elif action == glfw.GLFW.GLFW_RELEASE:
            self.keys_pressed[key] = False
            self._key_events.append((key, False))