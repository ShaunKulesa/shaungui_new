
from shaungui.shader import Shader
from shaungui.quad import Quad, QuadDrawer
import pyrr
from shaungui.grid_system.grid_system import GridSystem
from shaungui.place_system.place_system import PlaceSystem
from OpenGL import GL

from array import array
import ctypes

class ChartDrawer:
    def __init__(self) -> None:
        self.vertex_shader = """
            #version 330

            in vec2 in_position;
            in vec2 in_size;
            in vec4 in_colour;
            
            out vec2 position;
            out vec2 size;
            out vec4 vs_colour;

            void main() {
                position = in_position;
                size = in_size;
                vs_colour = in_colour;
            }
        """

        self.fragment_shader = """
            #version 330 core

            in vec4 gs_colour;
            out vec4 outColour;

            void main()
            {
                outColour = gs_colour;
            }
        """

        self.geometry_shader = """
            #version 330
            layout (points) in;
            layout (triangle_strip, max_vertices = 8) out;

            in vec2 position[];
            in vec2 size[];

            uniform mat4 projection;

            in vec4 vs_colour[];
            out vec4 gs_colour;
        
            void main() {
                gs_colour = vs_colour[0];
                gl_Position = projection * vec4(position[0].x, position[0].y, 0.0, 1.0); // bottom left
                EmitVertex();
                gl_Position = projection * vec4(position[0].x, position[0].y + size[0].y, 0.0, 1.0); // top left
                EmitVertex();
                gl_Position = projection * vec4(position[0].x + size[0].x, position[0].y, 0.0, 1.0); // bottom right
                EmitVertex();
                gl_Position = projection * vec4(position[0].x + size[0].x, position[0].y + size[0].y, 0.0, 1.0); // top right
                EmitVertex();
                EndPrimitive();
            }
        """

        self.shader = Shader(self.vertex_shader, self.fragment_shader, geometry_shader=self.geometry_shader)
        self.shader.compile()
        self.shader.use()

        ortho = pyrr.matrix44.create_orthogonal_projection_matrix(
            0, 500, 0, 500, 0, 1, dtype="float32")

        self.shader.set_UniformMatrix4fv(self.shader.get_uniform("projection"), 1, GL.GL_FALSE, ortho)
        
        self.points = []
        self.points_array = array('f', self.points).tobytes()

        self.buffer_update = False
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        
        self.vbo = GL.glGenBuffers(1)        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.points_array, GL.GL_STATIC_DRAW)

        print(GL.glGetAttribLocation(self.shader.shader, "in_position"))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_position"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_position"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        print(GL.glGetAttribLocation(self.shader.shader, "in_size"))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_size"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_size"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(2 * 4))
        print(GL.glGetAttribLocation(self.shader.shader, "in_colour"))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_colour"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_colour"), 4, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(4 * 4))

    def add_quad(self, width, height, x, y, colour):
        self.points.extend([x, y, width, height, colour[0]/255, colour[1]/255,colour[2]/255, colour[3]/255])
        self.points_array = array('f', self.points).tobytes()
        self.buffer_update = True

    def update(self):
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.points_array, GL.GL_STATIC_DRAW)

    def render(self):
        if self.buffer_update:
            self.update()
            self.buffer_update = False

        self.shader.use()
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, len(self.points) // 8)
        
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

        # self.grid_system = GridSystem(self)
        # self.place_system = PlaceSystem(self)

        # self.background = Quad(self, self.width, self.height, self.line_colour)

        self.window = parent.window
        parent.widgets.append(self)
        
    def render(self):
        GL.glViewport(self.x, self.y, self.width, self.height)

        # if self.background.x == None:
        #     self.background.place(0, 0)
        
        # if len(self.place_system.queue) > 0:
        #     self.place_system.display_queue()
        #     self.quad_drawer.buffers_need_updating = True

        # if len(self.grid_system.queue) > 0:
        #     self.grid_system.display_queue()
        #     self.quad_drawer.buffers_need_updating = True

        # self.quad_drawer.render()

        self.chart_quad.render()

    def place(self, x, y):
        self.x = x
        self.y = y

        self.chart_quad = ChartDrawer()

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

    def png_save(self):
        if len(self.place_system.queue) > 0:
            self.place_system.display_queue()
            self.quad_drawer.buffers_need_updating = True
        
        pixels = self.quad_drawer.read_pixels(0, 0, self.width, self.height)
        image = Image.frombytes("RGBA", (self.width, self.height), pixels).transpose(Image.FLIP_TOP_BOTTOM).save("percentage_chart.png")