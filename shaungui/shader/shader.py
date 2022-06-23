from OpenGL import GL
import OpenGL.GL.shaders

class Shader():
    def __init__(self, vertex_shader, fragment_shader, geometry_shader=None):
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.geometry_shader = geometry_shader
    
    def compile(self):
        shaders = []
        shaders.append(OpenGL.GL.shaders.compileShader(self.vertex_shader, GL.GL_VERTEX_SHADER))
        shaders.append(OpenGL.GL.shaders.compileShader(self.fragment_shader, GL.GL_FRAGMENT_SHADER))

        if self.geometry_shader is not None:
            shaders.append(OpenGL.GL.shaders.compileShader(self.geometry_shader, GL.GL_GEOMETRY_SHADER))

        self.shader = OpenGL.GL.shaders.compileProgram(*shaders)
    
        
    def use(self):
        GL.glUseProgram(self.shader)
    
    def get_uniform(self, name):
        return GL.glGetUniformLocation(self.shader, name)
    
    def set_UniformMatrix4fv(self, location, count, transpose, value):
        GL.glUniformMatrix4fv(location, count, transpose, value)