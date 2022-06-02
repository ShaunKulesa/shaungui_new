class Quad():
    __slot__ = {"x", "y", "width", "height", "colour", "parent", "rotation"}
    def __init__(self, parent, width, height, colour, rotation=0):
        self.parent = parent
        self.width = width
        self.height = height
        self.colour = colour
        self.rotation = rotation

        self.x = None
        self.y = None

        self.column = None
        self.row = None
        self.column_padding = 0
        self.row_padding = 0
    
    def place(self, x, y):
        self.x = x
        self.y = y

        self.parent.place_system.add_widget(self)

    def grid(self, column, row, column_padding=0, row_padding=0):
        self.column = column
        self.row = row
        self.column_padding = column_padding
        self.row_padding = row_padding
        
        self.parent.grid_system.add_widget(self, column, row)
