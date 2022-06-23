from OpenGL import GL 

class FrameBuffer():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.framebuffer = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.framebuffer)

        self.texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
  
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, 800, 600, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture, 0)
    
    def use(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.framebuffer)
    
    def read_pixels(self, x, y, width, height):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.framebuffer)
        pixels = GL.glReadPixels(x, y, width, height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        return pixels
    
    def delete(self):
        # GL.glDeleteFramebuffers(1, self.framebuffer)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)