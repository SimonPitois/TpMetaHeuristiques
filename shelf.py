class Shelf:
    """
    Cette classe représente un niveau.
    """
    def __init__(self, width, height):
        """
        Initialise une nouvelle instance de la classe Shelf avec la largeur et la hauteur données.

        @param width: La largeur du niveau.
        @param height: La hauteur du niveau.
        """
        self.width = width
        self.height = height
        self.items = []  # Liste des items stockés dans le niveau.
        self.residual_horizontal_space = width  # Espace horizontal résiduel sur le niveau.

    def add_item(self, item):
        """
        Ajoute un item dans le niveau.
        Complexité temporelle : 0(1)

        @param item: L'item à ajouter.
        """
        self.items.append(item)
        self.residual_horizontal_space -= item.width

    def __str__(self):
        """
        Méthode qui renvoie une représentation de chaîne conviviale de l'objet Shelf.

        @return: Représentation du niveau sous forme de chaîne.
        """
        result = "Largeur du niveau : %s" % self.width + "\n"
        result += "Hauteur du niveau : %s" % self.height + "\n"
        result += "Espace horizontal résiduel : %s" % self.residual_horizontal_space + "\n"
        result += "Items stockés dans le niveau : " + "\n"
        for item in self.items:
            result += str(item) + "\n"
        return result

    def __repr__(self):
        """
        Méthode qui renvoie une représentation de chaîne de l'objet Shelf qui est utile pour le débogage.

        @return: Représentation du niveau sous forme de chaîne.
        """
        result = "Largeur du niveau : %s" % self.width + "\n"
        result += "Hauteur du niveau : %s" % self.height + "\n"
        result += "Espace horizontal résiduel : %s" % self.residual_horizontal_space + "\n"
        result += "Items stockés dans le niveau : " + "\n"
        for item in self.items:
            result += str(item) + "\n"
        return result
