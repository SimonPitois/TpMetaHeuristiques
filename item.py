class Item:
    """
    Cette classe représente un item avec une largeur et une hauteur.
    """

    def __init__(self, width, height, number):
        """
        Initialise une nouvelle instance de la classe Item avec la largeur et la hauteur données.

        @param width : La largeur de l'item.
        @param height : La hauteur de l'item.
        @param number : Un numéro pour identifier l'item (sert principalement pour l'affichage).
        """
        self.height = height
        self.width = width
        self.number = number

    def __str__(self):
        """
        Méthode qui renvoie une représentation de l'objet sous forme de chaîne de caractères.

        @return: Représentation de l'item sous forme de chaîne.
        """
        return "Item %s : (w : %s, h : %s)" % (self.number, self.width, self.height)

    def __repr__(self):
        """
        Méthode qui renvoie une représentation de l'objet sous forme de chaîne de caractères
        qui est utile pour le débogage.

        @return: Représentation de l'item sous forme de chaîne.
        """
        return "Item %s : (w : %s, h : %s)" % (self.number, self.width, self.height)
