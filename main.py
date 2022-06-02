import shaungui
from time import perf_counter

window = shaungui.Window("Shaun's Window", 1920, 1080)

# for i in range(100000):
#     quad1 = shaungui.Quad(window, 100, 100, [255, 0, 0, 255], rotation = 45)
#     quad1.place((i * 150) + 0, 100)

# start = perf_counter()

# for x in range(5):
#     for y in range(1000):
#         quad1 = shaungui.Quad(window, 1100, 200, [255, 0, 0, 255])
#         quad1.place((x * 200), (y * 200))

# print(perf_counter() - start)

# start = perf_counter()

# for column in range(5):
#     for row in range(200000):
#         quad1 = shaungui.Quad(window, 300, 100, [255, 0, 0, 255])
#         quad1.grid(column, row, column_padding = 1, row_padding = 1)

# for column in range(5):
#     for row in range(200000):
#         quad1 = shaungui.Quad(window, 100, 100, [255, 0, 0, 255])
#         quad1.place(x=(column * 100) + 2, y=(row * 100) + 1)

# print(perf_counter() - start)

# table = shaungui.Table(window, height = 300, width = 1600)
# table.insert_row(400, 100)
# table.place(0, 0)

quad = shaungui.Quad(window, 100, 100, [255, 0, 0, 255])
print(quad.__dir__())


shaungui.start()