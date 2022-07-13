from time import perf_counter
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
        self.create_rectangle(0, 0, self.width, self.height, [item / 255 for item in background_colour], id="canvas_background")

        # border
        self.create_rectangle(0, 0, self.width, border_width, [item / 255 for item in border_colour], id="bottom_border")
        self.create_rectangle(0, 0, border_width, self.height, [item / 255 for item in border_colour], id="left_border")
        self.create_rectangle(self.width - border_width, 0, border_width, self.height, [item / 255 for item in border_colour], id="right_border")
        self.create_rectangle(0, self.height - border_width, self.width, border_width, [item / 255 for item in border_colour], id="top_border")

        self.rectangle_buffer_needs_updating = True

    def create_rectangle(self, x, y, width, height, colour, id=None, tags=[]):
        self.rectangle_drawer.rectangle_points.extend([x, y, width, height, colour[0], colour[1], colour[2], colour[3]])
        self.rectangle_drawer.rectangle_buffer_needs_updating = True
        
        if id is None:
            id = f'canvas_rectangle{self.counter}'
            self.ids[id] = ["rectangle", len(self.rectangle_drawer.rectangle_points) // 8]
            self.counter += 1
            return

        for tag in tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag].append(id)
       
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
                    return self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 8], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 7]
                break
    
    def get_size(self, id) -> list[float]:
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    return self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 6], self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 5]
                break
    
    def get_colour(self, id) -> list[float]:
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    return [
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 4],
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 3],
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 2],
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 1]
                    ]
                break
    
    def set_colour(self, id, colour):
        for shape_id in self.ids:
            if id == shape_id:
                if self.ids[id][0] == "rectangle":
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 4] = colour[0]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 3] = colour[1]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 2] = colour[2]
                    self.rectangle_drawer.rectangle_points[(self.ids[id][1] * 8) - 1] = colour[3]
                    self.rectangle_buffer_needs_updating = True
                break
    
    def tag_collision(self, tag, target_id=None, target_tags=[]) -> list:
        if target_id:
            target = self.ids[target_id]
            x, y = self.get_coords(target_id)
            width, height = self.get_size(target_id)

            # if sel.ids[target_id][0] == "rectangle":
            #     return self.rectangle_drawer.rectangle_collision(x, y, width, height, tag, target_tags
    
    def id_collision(self, id, target_id=None, target_tag=None) -> list:
        collisions = []
        
        if target_id:
            if self.ids[id][0] == "rectangle" and self.ids[target_id][0] == "rectangle":
                x, y = self.get_coords(id)
                width, height = self.get_size(id)
                target_x, target_y = self.get_coords(target_id)
                target_width, target_height = self.get_size(target_id)

                if x < target_x + target_width and x + width > target_x and y < target_y + target_height and y + height > target_y:
                    collisions.append(target_id)

        if target_tag:
            for object in self.tags[target_tag]:
                if self.ids[object][0] == "rectangle" and self.ids[id][0] == "rectangle":
                    x, y, = self.get_coords(object)
                    width, height = self.get_size(object)
                    target_x, target_y = self.get_coords(id)
                    target_width, target_height = self.get_size(id)

                    if x < target_x + target_width and x + width > target_x and y < target_y + target_height and y + height > target_y:
                        collisions.append(object)
        
        return collisions
        
    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        self.rectangle_drawer.draw_rectangles()
    



