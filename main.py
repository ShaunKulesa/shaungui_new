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
    global last_delta, dt

    # Calculate delta time (time since last frame was rendered)
    dt = time.perf_counter() - last_delta

    # Keep track of start of current frame render
    last_delta = time.perf_counter()

    # Close window when ESCAPE key was pressed at any moment
    for key, pressed in window.input.key_events():
        if key == glfw.KEY_ESCAPE and pressed:
            glfw.set_window_should_close(window.glfw_window, True)

    # Move canvas when key is pressed (WASD)
    if window.input.key_pressed(glfw.KEY_W):
        canvas.move("rectangle", 0, 100 * dt)
    elif window.input.key_pressed(glfw.KEY_S):
        canvas.move("rectangle", 0, -100 * dt)

    if window.input.key_pressed(glfw.KEY_A):
        canvas.move("rectangle", -100 * dt, 0)
    elif window.input.key_pressed(glfw.KEY_D):
        canvas.move("rectangle", 100 * dt, 0)

    # Update at same rate as renderer
    window.after(update, 0)


# Update at same rate as renderer
window.after(update, 0)

shaungui.start()