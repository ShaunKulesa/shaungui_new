from OpenGL import GL
from PIL.ImageFont import truetype
from rectpack import newPacker, SORT_NONE
from PIL import Image
import glfw

glfw.init()

window = glfw.create_window(640, 480, "Texture Atlas", None, None)
glfw.make_context_current(window)

class OpengGLBufferTextAtlas():
    def __init__(self, width, height) -> None:
        self.atlas = GL.glGenTextures(1)
        self.textures = {}
        self.width = width
        self.height = height
    
    def add_texture(self, file_name, texture_name):
         
        image = Image.open(file_name)
        width, height = image.size
        image = image.convert("RGBA")
        data = image.tobytes()

        self.textures[texture_name] = [file_name, None, None, width, height, data]

        self.organise()
    
    def get_buffer(self):
        return self.atlas
    
    def get_size(self):
        return [self.width, self.height]

    def organise(self):
        bins = [(self.width, self.height)]

        packer = newPacker(rotation=False, sort_algo=SORT_NONE)
        
        for key, value in self.textures.items():
            packer.add_rect(value[3], value[4])

        for b in bins:
            packer.add_bin(*b)

        packer.pack()

        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.atlas)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, self.width, self.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, bytes([0] * self.width * self.height * 4))

        # index = 0

        # for rect in packer[0]:
        #     x, y, = rect.x, rect.y

        #     GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, x, y, rect.width, rect.height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, bytes(self.textures[index][9]))
        #     index += 1

        # print(GL.glGetTexImage(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE))

        i = 0
        for texture, values in self.textures.items():
            print(list(packer))
            rect = packer[0][i]
            x, y = rect.x, rect.y

            GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, x, y, rect.width, rect.height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, values[5])
            print(values[5])
        
        Image.frombytes("RGBA", (self.width, self.height), GL.glGetTexImage(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)).save("test.png")



atlas = OpengGLBufferTextAtlas(2000, 2000)
atlas.add_texture("penny.jpg", "penny")