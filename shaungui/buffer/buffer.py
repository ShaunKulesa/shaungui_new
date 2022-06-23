from OpenGL import GL

class Buffer():
    def __init__(self):
        self.buffer = GL.glGenBuffers(1)
    
    def bind(self, target_type):
        GL.glBindBuffer(target_type, self.buffer)
    
    def bind_data(self, target_type, data):
        GL.glBufferData(target_type, data, GL.GL_DYNAMIC_DRAW)


