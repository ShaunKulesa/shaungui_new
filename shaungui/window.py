import glfw
from OpenGL import GL
import pyrr
import time

from .start import add_window
from .place_system.place_system import PlaceSystem
from .grid_system.grid_system import GridSystem
from .quad.quad_drawer import QuadDrawer
from .input import Input

class Window():
    def __init__(self, title, width, height, background_colour=[0, 0, 0, 255]):
        self.title = title
        self.width = width
        self.height = height
        self.background_colour = background_colour

        self.window = self

        # Force OpenGL context version
        glfw.window_hint(glfw.GLFW.GLFW_CLIENT_API, glfw.GLFW.GLFW_OPENGL_API)
        glfw.window_hint(glfw.GLFW.GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.GLFW.GLFW_CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.GLFW.GLFW_OPENGL_PROFILE,
                         glfw.GLFW.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.GLFW.GLFW_OPENGL_FORWARD_COMPAT, glfw.GLFW.GLFW_TRUE)

        self.glfw_window = glfw.create_window(self.width, self.height, self.title, None, None)
        glfw.make_context_current(self.glfw_window)

        add_window(self)

        glfw.set_window_size(self.glfw_window, self.width, self.height)
        width, height = glfw.get_window_size(self.glfw_window)

        ortho = pyrr.matrix44.create_orthogonal_projection_matrix(
            0, width, 0, height, 0, 1, dtype="float32")

        self.place_system = PlaceSystem(self)

        self.grid_system = GridSystem(self)

        self.quad_drawer = QuadDrawer(self, ortho)

        self.widgets = []

        # timer = time.time()
        # print(timer)

        self.after_functions = []

        self.key_binds = []

        # Instantiate the input system
        self.input = Input(self.glfw_window)

        self.delta_time = 0
    
    def render(self):
        start_time = time.time()

        glfw.make_context_current(self.glfw_window)

        glfw.swap_interval(1)

        GL.glViewport(0, 0, self.width, self.height)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClearColor(self.background_colour[0]/255, self.background_colour[1]/255, self.background_colour[2]/255, self.background_colour[3]/255)

        if len(self.place_system.queue) > 0:
            self.place_system.display_queue()
            self.quad_drawer.buffers_need_updating = True
        
        if len(self.grid_system.queue) > 0:
            self.grid_system.display_queue()
            self.quad_drawer.buffers_need_updating = True
        
        self.quad_drawer.render()
        
        for widget in self.widgets:
            widget.render()

        glfw.swap_buffers(self.glfw_window)

        for after_function in self.after_functions:
            if time.time() >= after_function[1] + after_function[2]:
                after_function[0]()
                self.after_functions.remove(after_function)
        
        for key_bind in self.key_binds:
            if self.input.key_pressed(key_bind[0]) == True:
                key_bind[1]()
        
        self.delta_time = time.time() - start_time
                
    def after(self, function, seconds):
        self.after_functions.append([function, time.time(), seconds])

    def key_bind(self, key, function):
        self.key_binds.append([key, function])
    
    def close(self):
        glfw.set_window_should_close(self.glfw_window, 1)