from avltree import AVLTree
from shelf import *


def merge(arr, l, m, r):
    """
    Fusionne deux parties d'un tableau en utilisant un algorithme de fusion.
    Complexité temporelle : O(n)

    @param arr : Le tableau à fusionner.
    @param l : Indice du début de la première moitié du tableau.
    @param m : Indice du milieu du tableau.
    @param r : Indice de fin de la deuxième moitié du tableau.
    @return : Le tableau après fusion.
    """
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i].height <= R[j].height:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort(arr, l, r):
    """
    Trie un tableau en utilisant l'algorithme de tri fusion.
    Complexité temporelle : O(n log(n))

    @param arr : Le tableau à trier.
    @param l : Indice du début du tableau.
    @param r : Indice de fin du tableau.
    @return : Le tableau trié.
    """
    if l < r:
        m = l + (r - l) // 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)


class Strip:
    """
    Cette classe représente une bande de hauteur infinie qui contient des items sur plusieurs niveaux.
    """

    def __init__(self, width, items):
        """
        Initialise une nouvelle instance de la classe Strip avec la largeur et les items donnés.

        @param width: La largeur de la bande.
        @param items: La liste des items à insérer dans la bande.
        """
        self.width = width
        self.items = items
        self.shelves = []  # Liste des niveaux sur la bande
        self.avl_residual_space = None  # Arbre AVL pour stocker l'espace horitontal résiduel des différents niveaux

    def sort_items_decreasing_height(self):
        """
        Trie les items à insérer dans la bande par ordre de hauteur décroissante.
        Complexité temporelle : 0(n log(n))
        """
        merge_sort(self.items, 0, len(self.items) - 1)
        self.items.reverse()

    def minimum_residual_space(self, root, item_width, minimum):
        """
        Cherche dans l'arbre AVL le niveau dont l'espace horizontal résiduel est minimum pour l'item à insérer.
        Complexité temporelle : O(log(n))

        @param root : Un noeud de l'arbre AVL (on commence généralement à la racine).
        @param item_width : La largeur de l'item à insérer.
        @param minimum : Un noeud de l'arbre AVL (paramètre évolutif qui stocke le meilleur niveau pour l'item)
        @return : Le noeud de l'arbre AVL qui contient le niveau le plus adéquat pour l'item à insérer.
        """
        if root is None:
            return minimum
        elif root.residual_space > item_width:
            return self.minimum_residual_space(root.left, item_width, root)
        elif root.residual_space < item_width:
            return self.minimum_residual_space(root.right, item_width, minimum)
        else:
            return root

    def add_shelf(self, item, index):
        """
        Ajoute un nouveau niveau dans la bande et met à jour l'arbre AVL contenant les espaces horizontaux résiduels.
        Complexité temporelle : O(log(n))

        @param item : L'item à insérer dans la bande.
        @param index : Un index relatif à la position du nouveau niveau dans la liste des niveaux de la bande.
        """
        avl = AVLTree()
        self.shelves.append(Shelf(self.width, item.height))
        self.shelves[index].add_item(item)
        self.avl_residual_space = avl.insert_node(self.avl_residual_space,
                                                  self.shelves[index].residual_horizontal_space,
                                                  self.shelves[index])

    def add_item(self, item):
        """
        Ajoute un item dans un niveau existant ou crée un nouveau niveau si nécessaire.
        Complexité temporelle : O(log(n))

        @param item: L'item à ajouter dans la bande.
        """
        if len(self.shelves) == 0:
            self.add_shelf(item, 0)
        else:
            result = self.minimum_residual_space(self.avl_residual_space, item.width, None)
            if result is None:
                self.add_shelf(item, -1)
            else:
                avl = AVLTree()
                result.list[0].add_item(item)
                temp = result.list[0]
                self.avl_residual_space = avl.delete_node(self.avl_residual_space, result.residual_space, True)
                self.avl_residual_space = avl.insert_node(self.avl_residual_space,
                                                          temp.residual_horizontal_space,
                                                          temp)

    def fill(self):
        """
        Remplit la bande avec les items à insérer.
        Complexité temporelle : O(n log(n))
        """
        self.sort_items_decreasing_height()
        for item in self.items:
            self.add_item(item)

    def __str__(self):
        """
        Méthode qui renvoie une représentation de l'objet sous forme de chaîne de caractères.

        @return: Représentation de la bande sous forme de chaîne.
        """
        result = "Largeur de la bande : %s" % self.width + "\n"
        for i in range(len(self.shelves)):
            result += "----------Level %s----------" % i + "\n" + str(self.shelves[i])
        return result

    def __repr__(self):
        """
        Méthode qui renvoie une représentation de l'objet sous forme de chaîne de caractères
        qui est utile pour le débogage.

        @return: Représentation de la bande sous forme de chaîne.
        """
        result = "Largeur de la bande : %s" % self.width + "\n"
        for i in range(len(self.shelves)):
            result += "----------Level %s----------" % i + "\n" + str(self.shelves[i])
        return result
