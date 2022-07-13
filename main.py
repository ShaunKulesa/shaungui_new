import shaungui

window = shaungui.Window("Tetris", 500, 600, background_colour=[240, 240, 240, 255])

canvas = shaungui.Canvas(window, 250, 500, border_width=0)
canvas.place(125, 0)

canvas.create_rectangle(0, 0, 25, 25, [255, 0, 0, 255], id="rectangle1")
canvas.create_rectangle(25, 0, 25, 25, [255, 0, 0, 255], id="rectangle2")
canvas.create_rectangle(50, 0, 25, 25, [255, 0, 0, 255], id="rectangle3")
canvas.create_rectangle(75, 0, 25, 25, [255, 0, 0, 255], id="rectangle4")

def update():
    if window.input.key_pressed('A'):
        canvas.move("rectangle1", -25, 0)
        canvas.move("rectangle2", -25, 0)
        canvas.move("rectangle3", -25, 0)
        canvas.move("rectangle4", -25, 0)

    elif window.input.key_pressed('D'):
        canvas.move("rectangle1", 25, 0)
        canvas.move("rectangle2", 25, 0)
        canvas.move("rectangle3", 25, 0)
        canvas.move("rectangle4", 25, 0)

    window.after(update, 0.1)

window.after(update, 0.1)

shaungui.start()