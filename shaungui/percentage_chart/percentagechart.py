from shaungui.percentage_chart.chart_drawer import ChartDrawer
from shaungui.grid_system.grid_system import GridSystem
from shaungui.place_system.place_system import PlaceSystem

from OpenGL import GL

class PercentageChart():
    def __init__(self, parent, percentage, width=100, height=100, filled_colour=[255, 0, 0, 255], unfilled_colour=[0, 0, 0, 255], background_colour=[255, 255, 255, 255], outline_colour=[0, 0, 0, 255], line_spacing=1, outline_width=1) -> None:
        self.window = parent
        self.percentage = percentage
        self.width = width
        self.height = height
        self.filled_colour = filled_colour
        self.unfilled_colour = unfilled_colour
        self.background_colour = background_colour
        self.line_spacing = line_spacing
        self.outline_width = outline_width
        self.outline_colour = outline_colour

        self.grid_system = GridSystem(self)
        self.place_system = PlaceSystem(self)

        self.window = parent.window
        parent.widgets.append(self)
        
    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        # if len(self.grid_system.queue) > 0:
        #     self.grid_system.display_queue()
        #     self.quad_drawer.buffers_need_updating = True

        self.chart_quad.render()

    def place(self, x, y):
        self.x = x
        self.y = y

        self.chart_quad = ChartDrawer()

        # background
        self.chart_quad.add_quad(self.width, self.height, 0, 0, self.background_colour)

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

                self.chart_quad.add_quad(quad_width, quad_height, column_spacing, row_spacing, colour)
        
        # left outline
        self.chart_quad.add_quad(self.outline_width, self.height, 0, 0, self.outline_colour)

        # right outline
        self.chart_quad.add_quad(self.outline_width, self.height, self.width - self.outline_width, 0, self.outline_colour)

        # top outline
        self.chart_quad.add_quad(self.width, self.outline_width, 0, 0, self.outline_colour)

        # bottom outline
        self.chart_quad.add_quad(self.width, self.outline_width, 0, self.height - self.outline_width, self.outline_colour)