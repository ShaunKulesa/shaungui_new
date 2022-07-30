import OpenGL.GL as GL
import glfw
from PIL.ImageFont import truetype

glfw.init()
window = glfw.create_window(500, 600, "Tetris", None, None)
glfw.make_context_current(window)

class TextAtlas():
    def __init__(self, width, height, font_size) -> None:
        self.atlas = GL.glGenTextures(1)
        #
        self.letters = {}
        self.width = width
        self.height = height
        self.font_size = font_size

    def add_text(self, letter: str, font_file: str):
        if font_file not in self.letters:
            self.letters[font_file] = {}

        self.letters[font_file][letter] = (None, None, self.get_pixels(letter, font_file))
        
        self.__organise()
    def get_pixels(self, text, font_file) -> tuple[list, int, int]:
        font = truetype(font_file, self.font_size)
        image = font.getmask(text, "RGBA")

        rows, columns = image.size

        return rows, columns, image
    
    def get_text_position(self, letter: str, font_file: str):
        
    
    def get_buffer(self):
        return self.atlas
    
    def get_size(self):
        return [self.width, self.height]
    
    
    def __organise(self):
        bins = [(self.width, self.height)]

        packer = newPacker(rotation=False, sort_algo=SORT_NONE)

        for r in self.texts:
            packer.add_rect(r[7], r[8])

        for b in bins:
            packer.add_bin(*b)

        packer.pack()

        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.atlas)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, self.width, self.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, bytes([255] * self.width * self.height * 4))

        index = 0
        image = Image.new("RGBA", (1000, 1000))

        for rect in packer[0]:
            x, y, = rect.x, rect.y
            self.texts[index][5 : 7] = [x, y]
            GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, x, y, rect.width, rect.height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, bytes(self.texts[index][9]))
            bytes_img = Image.frombytes("RGBA", (rect.width, rect.height), bytes(self.texts[index][9]))
            image.paste(bytes_img, (x, y))
            index += 1
        
        image.save("test.png")
        image.close()
        