import shaungui

window = shaungui.Window("Shaun's Window", 1500, 750)

canvas = shaungui.Canvas(window, 500, 500)
canvas.place(0, 0)

canvas.create_rectangle(1, 1, 100, 100, [255, 0, 0, 255], id="rectangle")

def update():
    canvas.move("rectangle", 10, 0)
    window.after(update, 1)

window.after(update, 1)

shaungui.start()