# from OpenGL import GL
# import ctypes
# import array
# from shaun_gui_functions import _quad_rotate_around

# from shaungui.shader import Shader
# from shaungui.buffer import Buffer
# from shaungui.framebuffer import FrameBuffer

# class QuadDrawer():
#     def __init__(self, parent, ortho):
#         GL.glEnable(GL.GL_BLEND)
#         GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

#         vertex_shader = """
#             #version 330

#             layout(location = 0) in vec3 position;
#             layout(location = 1) in vec4 color;

#             out vec4 frag_color;

#             uniform mat4 projection;
            
#             void main() {
#               frag_color = color;
#               gl_Position = projection * vec4(position, 1.0);
#             }
#         """

#         fragment_shader = """
#             #version 330

#             in vec4 frag_color;

#             out vec4 fragColor;

#             uniform sampler2D image;

#             void main() {
#               fragColor = frag_color;
#             }
#         """
        
#         #Shader stuff
#         self.shader = Shader(vertex_shader, fragment_shader)
#         self.shader.compile()
#         self.uniform_locations = {"proj": self.shader.get_uniform("projection")}
#         print(self.uniform_locations["proj"])
#         self.ortho_values = ortho
#         self.shader.use()
#         self.shader.set_UniformMatrix4fv(self.uniform_locations["proj"], 1, GL.GL_FALSE, self.ortho_values)

#         self.buffers_need_updating = False

#         self.vertices = array.array('f', [])

#         self.indices = array.array('I', [])

#         self.quads = []

#         self.indice_count = 0

#         self.va = GL.glGenVertexArrays(1)
#         GL.glBindVertexArray(self.va)

#         self.vertexPositions = Buffer()
#         self.vertexPositions.bind(GL.GL_ARRAY_BUFFER)

#         GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 7 * 4, ctypes.c_void_p(0))
#         GL.glEnableVertexAttribArray(0)

#         GL.glVertexAttribPointer(1, 4, GL.GL_FLOAT, GL.GL_FALSE, 7 * 4, ctypes.c_void_p(3 * 4))
#         GL.glEnableVertexAttribArray(1)

#         self.indexPositions = Buffer()
#         self.indexPositions.bind(GL.GL_ELEMENT_ARRAY_BUFFER)

#     def add(self, queue):
#         for quad in queue:
#             x = quad.x
#             y = quad.y
#             width = quad.width
#             height = quad.height
#             colour = quad.colour
#             rotation = quad.rotation

#             vertices = [
#             x, y, 0, colour[0]/255, colour[1]/255, colour[2]/255, colour[3]/255,
#             x + width, y, 0, colour[0]/255, colour[1]/255, colour[2]/255, colour[3]/255,
#             x + width, y + height, 0, colour[0]/255, colour[1]/255, colour[2]/255, colour[3]/255,
#             x, y + height, 0, colour[0]/255, colour[1]/255, colour[2]/255, colour[3]/255
#             ]
            
#             if rotation != 0:
#                 center_x = x + (width * 0.5)
#                 center_y = y + (height * 0.5)

#                 self.vertices.extend(_quad_rotate_around(rotation, vertices, center_x, center_y))
#             else:
#                 self.vertices.extend(vertices)

#             offset = self.indice_count

#             self.indices.append(offset + 0)
#             self.indices.append(offset + 1)
#             self.indices.append(offset + 2)

#             self.indices.append(offset + 0)
#             self.indices.append(offset + 2)
#             self.indices.append(offset + 3)

#             self.indice_count += 4

#     def update(self):
#         # GL.glBindVertexArray(self.va)
        
#         self.vertexPositions.bind(GL.GL_ARRAY_BUFFER)
#         self.vertexPositions.bind_data(GL.GL_ARRAY_BUFFER, bytes(self.vertices))

#         self.indexPositions.bind(GL.GL_ARRAY_BUFFER)
#         self.indexPositions.bind_data(GL.GL_ARRAY_BUFFER, bytes(self.indices))

#     def render(self):
#         if self.buffers_need_updating:
#             self.update()
#             self.buffers_need_updating = False
        
#         self.shader.use()

#         GL.glBindVertexArray(self.va)

#         GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)
    
#     # def read_pixels(self, x, y, width, height):
#     #     GL.glViewport(x, y, width, height)
#     #     GL.glClear(GL.GL_COLOR_BUFFER_BIT)
#     #     framebuffer = FrameBuffer(width, height)
#     #     framebuffer.use()
#     #     self.update()
#     #     self.render()
#     #     pixels = framebuffer.read_pixels(x, y, width, height)
#     #     framebuffer.delete()
#     #     return pixels


from OpenGL import GL
import ctypes
from array import array
from shaun_gui_functions import _quad_rotate_around

from shaungui.shader import Shader
from shaungui.buffer import Buffer
from shaungui.framebuffer import FrameBuffer

class QuadDrawer():
    def __init__(self, parent, ortho):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

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

        self.uniform_locations = {"proj": self.shader.get_uniform("projection")}

        self.ortho_values = ortho
        self.shader.set_UniformMatrix4fv(self.uniform_locations["proj"], 1, GL.GL_FALSE, self.ortho_values)

        self.buffers_need_updating = False

        self.quads = []

        self.points = []

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
        GL.glBufferData(GL.GL_ARRAY_BUFFER, array('f', self.points).tobytes(), GL.GL_STATIC_DRAW)

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