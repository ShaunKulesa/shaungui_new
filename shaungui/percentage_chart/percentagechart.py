
from shaungui.quad import Quad, QuadDrawer
import pyrr
from shaungui.grid_system.grid_system import GridSystem
from shaungui.place_system.place_system import PlaceSystem
from OpenGL import GL
from PIL import Image

#use individual renderer and geomertry shader to draw the chart

class PercentageChart():
    def __init__(self, parent, percentage, width=100, height=100, filled_colour=[255, 0, 0, 255], unfilled_colour=[0, 0, 0, 255], line_colour=[255, 255, 255, 255], outline_colour=[0, 0, 0, 255], line_spacing=1, outline_width=1) -> None:
        self.window = parent
        self.percentage = percentage
        self.width = width
        self.height = height
        self.filled_colour = filled_colour
        self.unfilled_colour = unfilled_colour
        self.line_colour = line_colour
        self.line_spacing = line_spacing
        self.outline_width = outline_width
        self.outline_colour = outline_colour

        self.grid_system = GridSystem(self)
        self.place_system = PlaceSystem(self)

        self.background = Quad(self, self.width, self.height, self.line_colour)

        self.window = parent.window
        parent.widgets.append(self)
        
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

    def place(self, x, y):
        self.x = x
        self.y = y
        
        ortho = pyrr.matrix44.create_orthogonal_projection_matrix(0, self.width, 0, self.height, 0, 1, dtype="float32")
        self.quad_drawer = QuadDrawer(self, ortho)

        self.background.place(0, 0)

        quad_width = ((self.width - (self.line_spacing * (10 - 1))) - (self.outline_width * 2)) / 10
        quad_height = ((self.height - (self.line_spacing * (10 - 1))) - (self.outline_width * 2)) / 10
        

        for row in range(10):
            for column in range(10):

                if (row * 10) + column + 1 <= self.percentage:
                    colour = self.filled_colour
                else:
                    colour = self.unfilled_colour

                column_spacing = (quad_width + self.line_spacing) * column
                column_spacing += self.outline_width

                row_spacing = (self.height - ((quad_height + self.line_spacing) * row)) - quad_height
                row_spacing -= self.outline_width

                quad = Quad(self, quad_width, quad_height, colour)
                quad.place(column_spacing, row_spacing)
        
        left_outline = Quad(self, self.outline_width, self.height, self.outline_colour)
        left_outline.place(0, 0)

        right_outline = Quad(self, self.outline_width, self.height, self.outline_colour)
        right_outline.place(self.width - self.outline_width, 0)

        top_outline = Quad(self, self.width  - (self.outline_width * 2), self.outline_width, self.outline_colour)
        top_outline.place(0 + self.outline_width, 0)

        bottom_outline = Quad(self, self.width  - (self.outline_width * 2), self.outline_width, self.outline_colour)
        bottom_outline.place(0 + self.outline_width, self.height - self.outline_width)
                
    def png_save(self):
        if len(self.place_system.queue) > 0:
            self.place_system.display_queue()
            self.quad_drawer.buffers_need_updating = True
        
        pixels = self.quad_drawer.read_pixels(0, 0, self.width, self.height)
        image = Image.frombytes("RGBA", (self.width, self.height), pixels).transpose(Image.FLIP_TOP_BOTTOM).save("percentage_chart.png")