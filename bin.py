class Bin:
    """
    Cette classe représente une boîte.
    """
    def __init__(self, width, height):
        """
        Initialise une nouvelle instance de la classe Bin avec une largeur et une hauteur.

        @param width: La largeur de la boîte.
        @param height: La hauteur de la boîte.
        """
        self.width = width
        self.height = height
        self.residual_vertical_space = height
        self.shelves = []

    def add_shelf(self, shelf):
        """
        Ajoute un niveau dans la boîte.
        Complexité temporelle : O(1)

        @param shelf: Le niveau à ajouter.
        """
        self.shelves.append(shelf)
        self.residual_vertical_space -= shelf.height

    def items_weight(self):
        """
        Donne le "poids" total des items contenus dans la boîte.
        Complexité temporelle : O(n²)

        @return: Le poids total des items.
        """
        sum = 0
        for shelf in self.shelves:
            for item in shelf.items:
                sum += item.width * item.height
        return sum

    def nb_items(self):
        """
        Donne le nombre d'items présents dans la boîte.
        Complexité temporelle : O(n)

        @return: Le nombre total d'items.
        """
        sum = 0
        for shelf in self.shelves:
            sum += len(shelf.items)
        return sum

    def items(self):
        items = []
        for shelf in self.shelves:
            items += shelf.items
        return items

    def __str__(self):
        """
        Méthode qui renvoie une représentation de chaîne conviviale de l'objet Bin.

        @return: Représentation de la boîte sous forme de chaîne.
        """
        result = "Largeur bin : %s" % self.width + "\n"
        result += "Hauteur bin : %s" % self.height + "\n" + "\n"
        for i in range(len(self.shelves)):
            result += "Level %s" % i + "\n" + str(self.shelves[i]) + "\n"
        return result

    def __repr__(self):
        """
        Méthode spéciale qui renvoie une représentation de chaîne de l'objet Bin qui est utile pour le débogage.

        @return: Représentation de la boîte sous forme de chaîne.
        """
        result = "Largeur de la bin : %s" % self.width + "\n"
        result += "Hauteur de la bin : %s" % self.height + "\n" + "\n"
        for i in range(len(self.shelves)):
            result += "Level %s" % i + "\n" + str(self.shelves[i]) + "\n"
        return result
