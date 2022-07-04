import shaungui

window = shaungui.Window("Shaun's Window", 1500, 750)

chart = shaungui.PercentageChart(window, 15, 500, 500, unfilled_colour=[255, 255, 255, 255], line_colour=[0, 0, 0, 0], line_spacing=2, outline_width=2, outline_colour=[255, 0, 255, 255])
chart.place(100, 100)

shaungui.start()
