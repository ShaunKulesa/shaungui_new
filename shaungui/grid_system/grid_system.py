import time

class GridSystem():
    def __init__(self, parent) -> None:
        self.parent = parent
        self.max_column = 0
        self.max_row = 0
        self.columns = {}
        self.rows = {}
        self.widgets = []
        self.queue = []

    def add_widget(self, widget, column, row):
        if column not in self.columns:
            self.columns[column] = [0, 0, 0]
        if row not in self.rows:
            self.rows[row] = [0, 0, 0]
        
        if column > self.max_column:
            self.max_column = column
        if row > self.max_row:
            self.max_row = row
        
        self.widgets.append(widget)
        self.queue.append(widget)

    def set_columns_rows(self):
        for widget in self.widgets:
            
            #set the highest column width and row height
            if widget.width > self.columns[widget.column][1]:
                self.columns[widget.column][1] = widget.width
            if widget.height > self.rows[widget.row][1]:
                self.rows[widget.row][1] = widget.height
            
            #set the highest padding
            if widget.column_padding > self.columns[widget.column][2]:
                self.columns[widget.column][2] = widget.column_padding
            if widget.row_padding > self.rows[widget.row][2]:
                self.rows[widget.row][2] = widget.row_padding
        
        previous_row = None

        for row in self.rows.keys():
            if previous_row == None:
                self.rows[row][0] = self.parent.height
            else:
                self.rows[row][0] = self.rows[previous_row][0] - self.rows[previous_row][1] - self.rows[previous_row][2]
            previous_row = row
        
        previous_column = None

        for column in self.columns.keys():
            if previous_column == None:
                self.columns[column][0] = 0
            else:
                self.columns[column][0] = self.columns[previous_column][0] + self.columns[previous_column][1] + self.columns[previous_column][2]
            previous_column = column

        for widget in self.widgets:
            widget.x = self.columns[widget.column][0]

            # if widget.column == x:
            #     print(widget.x)
            widget.y = self.rows[widget.row][0] - widget.height

            



    # def set_columns(self):
    #     previous_column = None
    #     for column in self.columns:
    #         highest_padding = 0
    #         widest_widget = 0

    #         for widget in self.widgets:
    #             if widget.column == column:
    #                 if widget.column_padding > highest_padding:
    #                     highest_padding = widget.column_padding
    #                 if widget.width > widest_widget:
    #                     widest_widget = widget.width
            
    #         if previous_column != None:
    #             self.columns[column][0] = self.columns[previous_column][1] + highest_padding
    #             self.columns[column][1] = self.columns[previous_column][1] + highest_padding + widest_widget
    #             previous_column = column

    #         if previous_column == None:
    #             self.columns[column][0] = highest_padding
    #             self.columns[column][1] = widest_widget + highest_padding
    #             previous_column = column

    # def set_rows(self):
    #     parent_height = self.parent.height
    #     previous_row = None

    #     for row in self.rows:
    #         highest_padding = 0
    #         tallest_widget = 0

    #         for widget in self.widgets:
    #             if widget.row == row:
    #                 if widget.row_padding > highest_padding:
    #                     highest_padding = widget.row_padding
    #                 if widget.height > tallest_widget:
    #                     tallest_widget = widget.height
            
    #         if previous_row != None:
    #             self.rows[row][0] = self.rows[previous_row][1] - highest_padding
    #             self.rows[row][1] = self.rows[previous_row][1] - highest_padding - tallest_widget
    #             previous_row = row

    #         if previous_row == None:
    #             self.rows[row][0] = parent_height - highest_padding
    #             self.rows[row][1] = parent_height - highest_padding - tallest_widget
    #             previous_row = row
        
    def set_widgets_coordinates(self):
        for widget in self.widgets:
            if widget.x != None and widget.y != None:
                if widget.x != self.columns[widget.column][0] or widget.y != self.rows[widget.row][0] - widget.height:
                    widget.set_movement(self.columns[widget.column][0], self.rows[widget.row][0] - widget.height)
            elif widget.x == None and widget.y == None:
                widget.x = self.columns[widget.column][0]
                widget.y = self.rows[widget.row][0] - widget.height

    def display_queue(self):
        start = time.perf_counter()
    
        self.set_columns_rows()

        # self.set_widgets_coordinates()

        self.parent.quad_drawer.add(self.widgets)

        # print("grid:", time.perf_counter() - start)
        print(self.columns)

        self.queue = []
