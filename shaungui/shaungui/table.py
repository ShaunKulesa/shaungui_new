from .quad.quad_drawer import QuadDrawer
from .grid_system import GridSystem
from .place_system import PlaceSystem
from .quad.quad import Quad

import pyrr
import glfw
from OpenGL import GL

class Table():
    def __init__(self, parent, height, width):
        self.height = height
        self.width = width
        
        self.x = None
        self.y = None

        self.grid_system = GridSystem(self)
        self.place_system = PlaceSystem(self)
        
        self.window = parent.window
        self.parent = parent.widgets.append(self)

        self.background = Quad(self, width=self.width, height=self.height, colour=[0, 255, 0, 255])


    def place(self, x, y):
        self.x = x
        self.y = y
        
        ortho = pyrr.matrix44.create_orthogonal_projection_matrix(0, self.width, 0, self.height, 0, 1, dtype="float32")
        self.quad_drawer = QuadDrawer(self, ortho)
    
    def insert_row(self, width, height):
        for i in range(4):
            quad = Quad(self, width=width, height=height, colour=[255, 0, 0, 255])
            quad.grid(i, 0, column_padding=1)
    
    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        if self.background.x == None:
            self.background.place(0, 0)
        
        if len(self.place_system.queue) > 0:
            self.place_system.display_queue()
            self.quad_drawer.buffers_need_updating = True

        if len(self.grid_system.queue) > 0:
            self.grid_system.display_queue()
            self.quad_drawer.buffers_need_updating = True

        self.quad_drawer.render()
        # print(self.quad_drawer.vertices.tolist())




