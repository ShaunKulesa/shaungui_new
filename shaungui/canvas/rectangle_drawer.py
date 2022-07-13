from OpenGL import GL
from shaungui.shader import Shader
from array import array
import ctypes
import pyrr

class RectangleDrawer:
    def __init__(self, width, height):
        rectangle_vertex_shader = """
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

        rectangle_geometry_shader = """
            #version 330
            layout (points) in;
            layout (triangle_strip, max_vertices = 4) out;

            in vec2 position[];
            in vec2 size[];

            uniform mat4 projection;

            in vec4 vs_colour[];
            out vec4 gs_colour;

            void main() {
                // main shape
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

        rectangle_fragment_shader = """
            #version 330 core

            in vec4 gs_colour;
            out vec4 outColour;

            void main()
            {
                outColour = gs_colour;
            }
        """

        self.rectangle_buffer_needs_updating = False
        self.rectangle_points = array('f', [])

        self.rectangle_shader = Shader(rectangle_vertex_shader, rectangle_fragment_shader, geometry_shader=rectangle_geometry_shader)
        self.rectangle_shader.compile()
        self.rectangle_shader.use()

        ortho = pyrr.matrix44.create_orthogonal_projection_matrix(
            0, width, 0, height, 0, 1, dtype="float32")

        self.rectangle_shader.set_UniformMatrix4fv(self.rectangle_shader.get_uniform("projection"), 1, GL.GL_FALSE, ortho)

        self.rectangles_vertex_array = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.rectangles_vertex_array)
        
        self.rectangles_buffer = GL.glGenBuffers(1)
        self.update_rectangles()

        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_position"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_position"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_size"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_size"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(2 * 4))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_colour"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.rectangle_shader.shader, "in_colour"), 4, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(4 * 4))

    def update_rectangles(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.rectangles_buffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.rectangle_points.tobytes(), GL.GL_DYNAMIC_DRAW)
    
    def draw_rectangles(self):
        if self.rectangle_buffer_needs_updating:
            self.update_rectangles()
            self.rectangle_buffer_needs_updating = False

        self.rectangle_shader.use()
        GL.glBindVertexArray(self.rectangles_vertex_array)
        GL.glDrawArrays(GL.GL_POINTS, 0, len(self.rectangle_points) // 8)