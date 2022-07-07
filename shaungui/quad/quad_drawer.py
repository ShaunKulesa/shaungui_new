from OpenGL import GL
import ctypes
from array import array

from shaungui.shader import Shader

class QuadDrawer():
    def __init__(self, parent, ortho):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        vertex_shader = """
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

        fragment_shader = """
            #version 330 core

            in vec4 gs_colour;
            out vec4 outColour;

            void main()
            {
                outColour = gs_colour;
            }
        """

        #add rotation
        geometry_shader = """
            #version 330
            layout (points) in;
            layout (triangle_strip, max_vertices = 4) out;

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

        self.shader = Shader(vertex_shader, fragment_shader, geometry_shader=geometry_shader)
        self.shader.compile()
        self.shader.use()

        self.uniform_locations = {"proj": self.shader.get_uniform("projection")}

        self.ortho_values = ortho
        self.shader.set_UniformMatrix4fv(self.uniform_locations["proj"], 1, GL.GL_FALSE, self.ortho_values)

        self.buffers_need_updating = False

        self.quads = []

        self.points = array('f', [])

        self.va = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.va)

        self.vbo = GL.glGenBuffers(1)
        self.update()

        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_position"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_position"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_size"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_size"), 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(2 * 4))
        GL.glEnableVertexAttribArray(GL.glGetAttribLocation(self.shader.shader, "in_colour"))
        GL.glVertexAttribPointer(GL.glGetAttribLocation(self.shader.shader, "in_colour"), 4, GL.GL_FLOAT, GL.GL_FALSE, 8 * 4, ctypes.c_void_p(4 * 4))

    def add(self, queue):
        for quad in queue:
            x = quad.x
            y = quad.y
            width = quad.width
            height = quad.height
            colour = quad.colour
            rotation = quad.rotation
            
            self.points.extend([x, y, width, height, colour[0]/255, colour[1]/255, colour[2]/255, colour[3]/255])
            self.buffers_need_updating = True

    def update(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.points.tobytes(), GL.GL_DYNAMIC_DRAW)

    def render(self):
        if self.buffers_need_updating:
            self.update()
            self.buffers_need_updating = False
        
        self.shader.use()

        GL.glBindVertexArray(self.va)

        GL.glDrawArrays(GL.GL_POINTS, 0, len(self.points) // 8)
    
#     def read_pixels(self, x, y, width, height):
#         GL.glViewport(x, y, width, height)
#         GL.glClear(GL.GL_COLOR_BUFFER_BIT)
#         framebuffer = FrameBuffer(width, height)
#         framebuffer.use()
#         self.update()
#         self.render()
#         pixels = framebuffer.read_pixels(x, y, width, height)
#         framebuffer.delete()
#         return pixels