import shaungui

window = shaungui.Window("Shaun's Window", 1500, 750)
# window2 = shaungui.Window("Shaun's Window 2", 1500, 750)


canvas = shaungui.Canvas(window, 500, 500)
canvas.place(0, 0)

canvas.create_rectangle(0, 0, 100, 100, [255, 0, 0, 255], id="rectangle")
canvas.create_rectangle(0, 0, 100, 100, [255, 255, 0, 255], id="rectangle1")
canvas.move_to("rectangle", 400, 400)
canvas.move_to("rectangle1", 300, 300)

shaungui.start()