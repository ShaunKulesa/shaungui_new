import time

import shaungui
import glfw

window = shaungui.Window("Shaun's Window", 1500, 750)

canvas = shaungui.Canvas(window, 500, 500)
canvas.place(0, 0)

canvas.create_rectangle(1, 1, 100, 100, [255, 0, 0, 255], id="rectangle")

dt = 0
last_delta = 0


def update():
    dt = window.delta_time

    # Close window when ESCAPE key was pressed at any moment
    if window.input.key_pressed('ESCAPE'):
        window.close()

    # Move canvas when key is pressed (WASD)
    if window.input.key_pressed('W'):
        canvas.move("rectangle", 0, 100 * dt)
    elif window.input.key_pressed('S'):
        canvas.move("rectangle", 0, -100 * dt)

    if window.input.key_pressed('A'):
        canvas.move("rectangle", -100 * dt, 0)
    elif window.input.key_pressed('D'):
        canvas.move("rectangle", 100 * dt, 0)

    # Update at same rate as renderer
    window.after(update, 0)

# Update at same rate as renderer
window.after(update, 0)

def escape():
    window.close()

def right():
    canvas.move("rectangle", 100 * window.delta_time, 0)

def left():
    canvas.move("rectangle", -100 * window.delta_time, 0)

def up():
    canvas.move("rectangle", 0, 100 * window.delta_time)

def down():
    canvas.move("rectangle", 0, -100 * window.delta_time)

window.key_bind("ESCAPE", escape)
window.key_bind("D", right)
window.key_bind("A", left)
window.key_bind("W", up)
window.key_bind("S", down)

shaungui.start()