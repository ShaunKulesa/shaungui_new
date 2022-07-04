import shaungui

window = shaungui.Window("Shaun's Window", 1500, 750)

# for x in range(1000):
#     chart = shaungui.PercentageChart(window, 15, 500, 500, unfilled_colour=[255, 255, 255, 255], background_colour=[0, 255, 0, 255], line_spacing=2, outline_width=2, outline_colour=[255, 0, 255, 255])
#     chart.place(x * 100, 100)

for x in range(105000):
    quad = shaungui.Quad(window, 100, 100, [255, 0, 0, 255])
    quad.place(x * 100, 100)

shaungui.start()

#78.5
#127.5