class Item:
    """
    Cette classe représente un rectangle (un item) avec une largeur et une hauteur.
    """

    def __init__(self, width, height):
        """
        Initialise une nouvelle instance de la classe Item avec la largeur et la hauteur données.

        @param width: La largeur de l'item.
        @param height: La hauteur de l'item.
        """
        self.height = height
        self.width = width

    def __str__(self):
        """
        Méthode qui renvoie une représentation de chaîne conviviale de l'objet.

        @return: Représentation de l'item sous forme de chaîne.
        """
        return "Item : (w : %s, h : %s)" % (self.width, self.height)

    def __repr__(self):
        """
        Méthode qui renvoie une représentation de chaîne de l'objet qui est utile pour la débogage.

        @return: Représentation de l'item sous forme de chaîne.
        """
        return "Item : (w : %s, h : %s)" % (self.width, self.height)
