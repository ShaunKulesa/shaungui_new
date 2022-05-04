class PlaceSystem():
    def __init__(self, parent):
        self.queue = []
        self.widgets = []
        self.parent = parent
    
    def add_widget(self, widget):
        self.queue.append(widget)
    
    def display_queue(self):
        self.parent.quad_drawer.add(self.queue)
        self.queue = []