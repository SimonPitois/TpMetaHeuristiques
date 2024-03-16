class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.remaining_vertical_space = height
        self.shelves = []
        self.items = []

    def items_weight(self):
        sum = 0
        for item in self.items:
            sum += item.width * item.height
        return sum

    def nb_items(self):
        return len(self.items)

    def __str__(self):
        result = "Largeur bin : %s" % self.width + "\n"
        result += "Hauteur bin : %s" % self.height + "\n" + "\n"
        for i in range(len(self.shelves)):
            result += "Level %s" % i + "\n" + str(self.shelves[i]) + "\n"
        return result

    def __repr__(self):
        result = "Largeur de la bin : %s" % self.width + "\n"
        result += "Hauteur de la bin : %s" % self.height + "\n" + "\n"
        for i in range(len(self.shelves)):
            result += "Level %s" % i + "\n" + str(self.shelves[i]) + "\n"
        return result