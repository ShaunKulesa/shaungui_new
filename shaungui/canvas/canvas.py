from OpenGL import GL
from array import array
from .rectangle_drawer import RectangleDrawer

class Canvas:
    def __init__(self, parent, width, height, background_colour=[0, 0, 0, 255], border_colour=[255, 255, 255, 255], border_width=1) -> None:
        self.parent = parent
        self.x = None
        self.y = None

        self.width = width
        self.height = height

        self.ids = {}
        self.counter = 0
        self.tags = {}

        self.rectangle_drawer = RectangleDrawer(self.width, self.height)

        # background
        self.create_rectangle(0, 0, self.width, self.height, [item / 255 for item in background_colour], id="canvas_background")

        # border
        self.create_rectangle(0, 0, self.width, border_width, [item / 255 for item in border_colour], id="bottom_border")
        self.create_rectangle(0, 0, border_width, self.height, [item / 255 for item in border_colour], id="left_border")
        self.create_rectangle(self.width - border_width, 0, border_width, self.height, [item / 255 for item in border_colour], id="right_border")
        self.create_rectangle(0, self.height - border_width, self.width, border_width, [item / 255 for item in border_colour], id="top_border")

    def create_rectangle(self, x, y, width, height, colour, id=None, tags=[]) -> str:
        # works
        self.rectangle_drawer.rectangle_points.extend([x, y, width, height, colour[0], colour[1], colour[2], colour[3]])
        self.rectangle_drawer.rectangle_buffer_needs_updating = True
        
        if id is None:
            id = f'canvas_object{self.counter}'
            self.counter += 1

        for tag in tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag].append(id)
       
        self.ids[id] = ["rectangle", x, y, width, height, [colour[0], colour[1], colour[2], colour[3]], []]
        
        return id
    
    def place(self, x, y) -> None:
        # works
        self.x = x
        self.y = y

        self.parent.widgets.append(self)
    
    def move_to(self, id, x, y) -> None:
        # works
        if id not in self.ids:
            return "Id not found"

        index = self.get_index(id)

        if self.ids[id][0] == "rectangle":
            self.ids[id][1] = x
            self.ids[id][2] = y

            self.rectangle_drawer.rectangle_points[(index * 8) - 8] = x
            self.rectangle_drawer.rectangle_points[(index * 8) - 7] = y
            self.rectangle_drawer.rectangle_buffer_needs_updating = True
    
    def move(self, id, x, y) -> None:
        # works
        if id not in self.ids:
            return "Id not found"

        index = self.get_index(id)

        if self.ids[id][0] == "rectangle":
            self.ids[id][1] += x
            self.ids[id][2] += y

            self.rectangle_drawer.rectangle_points[(index * 8) - 8] += x
            self.rectangle_drawer.rectangle_points[(index * 8) - 7] += y
            self.rectangle_drawer.rectangle_buffer_needs_updating = True
    
    def get_coords(self, id) -> tuple[float, float]:
        # works
        if id not in self.ids:
            return "Id not found"

        if self.ids[id][0] == "rectangle":
            return (
            self.ids[id][1],
            self.ids[id][2]
            )
    
    def get_size(self, id) -> tuple[float, float]:
        # works
        if id not in self.ids:
            return "Id not found"

        if self.ids[id][0] == "rectangle":
            return (
            self.ids[id][3],
            self.ids[id][4]
            )

    def get_colour(self, id) -> tuple[float, float, float, float]:
        # works
        if id not in self.ids:
            return "Id not found"

        if self.ids[id][0] == "rectangle":
            return (self.ids[5])
    
    def set_colour(self, id, colour):
        if id not in self.ids:
            return "Id not found"
        
        index = self.get_index(id)

        if self.ids[id][0] == "rectangle":
            self.ids[5] = colour
            self.rectangle_drawer.rectangle_points[(index * 8) - 4 : (index * 8)] = array('f', colour)
            self.rectangle_drawer.rectangle_buffer_needs_updating = True
    
    def tag_collision(self, tag, target_id=None, target_tags=[]) -> list:
        if target_id:
            target = self.ids[target_id]
            x, y = self.get_coords(target_id)
            width, height = self.get_size(target_id)

    def id_collision(self, id, target_id=None, target_tag=None) -> list:
        if id not in self.ids:
            return "id not found"
            
        collisions = []
        x, y = self.get_coords(id)
        width, height = self.get_size(id)
        
        if target_id:
            if target_id not in self.ids:
                return "target id not found"
                
            if self.ids[id][0] == "rectangle" and self.ids[target_id][0] == "rectangle":
                target_x, target_y = self.get_coords(target_id)
                target_width, target_height = self.get_size(target_id)

                if x < target_x + target_width and x + width > target_x and y < target_y + target_height and y + height > target_y:
                    collisions.append(target_id)

        if target_tag:
            if target_tag not in self.tags:
                return "target tag not found"

            for object in self.tags[target_tag]:
                if self.ids[object][0] == "rectangle" and self.ids[id][0] == "rectangle":
                    target_x, target_y = self.get_coords(id)
                    target_width, target_height = self.get_size(id)

                    if x < target_x + target_width and x + width > target_x and y < target_y + target_height and y + height > target_y:
                        collisions.append(object)
        
        return collisions
        
    def add_tag(self, id, tag):
        if tag not in self.tags:
            self.tags[tag] = []
        self.tags[tag].append(id)
    
    def remove_tag(self, id, tag):
        if tag not in self.tags:
            return "Tag not found"
        
        if id in self.tags[tag]:
            self.tags[tag].remove(id)
        else:
            return "Id does not have this tag"
    
    def delete_tag(self, tag):
        if tag not in self.tags:
            return "Tag not found"
        
        self.tags.pop(tag)
    
    def delete_id(self, id):
        if id not in self.ids:
            return "Id not found"
        
        self.ids.pop(id)
        
        for tag in self.tags:
            for id in tag:
                if id == id:
                    self.tags[tag].remove(id)
                    break
    
    def get_index(self, id):
        # Gets the index of the id's points in the points array

        index = 1

        for key in self.ids.keys():
            if key == id:
                return index
            index += 1

    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        self.rectangle_drawer.draw_rectangles()
    



