from shaungui.shader import Shader
import pyrr
from OpenGL import GL
from array import array
import ctypes

# turn into batch drawing for multiple charts

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

        self.buffer_update = False
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        
        self.vbo = GL.glGenBuffers(1)        
        self.update()

        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_position"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_position"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_size"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_size"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(2 * 4))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_colour"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_colour"), 4, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(4 * 4))

    def add_quad(self, width, height, x, y, colour):
        self.points.extend([x, y, width, height, colour[0]/255, colour[1]/255,colour[2]/255, colour[3]/255])
        self.buffer_update = True

    def update(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, array('f', self.points).tobytes(), GL.GL_STATIC_DRAW)

    def render(self):
        if self.buffer_update:
            self.update()
            self.buffer_update = False

        self.shader.use()
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, len(self.points) // 8)