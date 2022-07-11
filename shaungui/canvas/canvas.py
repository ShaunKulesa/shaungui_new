from OpenGL import GL
from .rectangle_drawer import RectangleDrawer

class Canvas:
    def __init__(self, parent, width, height, background_colour=[0, 0, 0, 255], border_colour=[255, 255, 255, 255], border_width=1) -> None:
        self.parent = parent
        self.x = None
        self.y = None

        self.width = width
        self.height = height

        self.tags = {}
        self.counter = 0
        self.ids = {}

        self.rectangle_drawer = RectangleDrawer(self.width, self.height)

        # background
        self.create_rectangle(0, 0, self.width, self.height, [item / 255 for item in background_colour])

        # border
        self.create_rectangle(0, 0, self.width, border_width, [item / 255 for item in border_colour], id="bottom_border")
        self.create_rectangle(0, 0, border_width, self.height, [item / 255 for item in border_colour], id="left_border")
        self.create_rectangle(self.width - border_width, 0, border_width, self.height, [item / 255 for item in border_colour], id="right_border")
        self.create_rectangle(0, self.height - border_width, self.width, border_width, [item / 255 for item in border_colour], id="top_border")

        self.rectangle_buffer_needs_updating = True

    def create_rectangle(self, x, y, width, height, colour, id=None, tags=[]):
        self.rectangle_drawer.rectangle_points.extend([x, y, width, height, colour[0], colour[1], colour[2], colour[3]])
        self.rectangle_drawer.rectangle_buffer_needs_updating = True

        for tag in tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag].append(self.counter)

        if id is None:
            self.ids[f'canvas_rectangle{self.counter}'] = ["rectangle", len(self.rectangle_drawer.rectangle_points) // 8]
            self.counter += 1
            return
        
        self.ids[id] = ["rectangle", len(self.rectangle_drawer.rectangle_points) // 8]
    
    def place(self, x, y):
        self.x = x
        self.y = y

        self.parent.widgets.append(self)
    
    def move_to(self, id, x, y):
        if self.ids[id][0] == "rectangle":
            self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 8] = x
            self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 8] = y
            self.rectangle_buffer_needs_updating = True
    
    def move(self, id, x, y):
        if self.ids[id][0] == "rectangle":
            self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 8] += x
            self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 8] += y
            self.rectangle_drawer.rectangle_buffer_needs_updating = True
    
    def get_coords(self, id) -> list[float]:
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    return self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 8], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 8]
                break
    
    def get_size(self, id) -> list[float]:
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    return self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 7], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 7]
                break
    
    def get_colour(self, id) -> list[float]:
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    return self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 6], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 6], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 2) - 6], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 3) - 6]
                break
    
    def set_colour(self, id, colour):
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 6] = colour[0]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 1) - 6] = colour[1]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 2) - 6] = colour[2]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8 + 3) - 6] = colour[3]
                    self.rectangle_buffer_needs_updating = True
                break
    
    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        self.rectangle_drawer.draw_rectangles()
    



