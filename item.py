class Item:
    def __init__(self, width, height):
        self.height = height
        self.width = width

    def __str__(self):
        return "Item : (w : %s, h : %s)" % (self.width, self.height)

    def __repr__(self):
        return "Item : (w : %s, h : %s)" % (self.width, self.height)
