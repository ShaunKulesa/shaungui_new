import shaungui

window = shaungui.Window("Shaun's Window", 640, 480)

chart = shaungui.PercentageChart(window, 15, 500, 500, unfilled_colour=[255, 255, 255, 255], line_colour=[0, 0, 0, 255], line_spacing=2, outline_width=2)
chart.place(100, 100)

# quad = shaungui.Quad(window, 100, 100, [0, 255, 0, 255])
# quad.place(150, 150)

# window2 = shaungui.Window("George's Window", 640, 480)
# chart2 = shaungui.PercentageChart(window2, 15, 100, 100, unfilled_colour=[200, 200, 200, 255], line_colour=[0, 0, 0, 255], line_spacing=2, outline_width=2)
# chart2.place(100, 100)

shaungui.start()