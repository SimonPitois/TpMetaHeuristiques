class Shelf:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.items = []
        self.remaining_horizontal_space = width

    def __str__(self):
        result = "Largeur du level : %s" % self.width + "\n"
        result += "Hauteur du level : %s" % self.height + "\n"
        result += "Espace horizontal restant : %s" % self.remaining_horizontal_space + "\n"
        for item in self.items:
            result += str(item) + "\n"
        return result