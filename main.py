import copy
import random
import tkinter as tk
import time

from item import *
from strip import *
from bin import *

WIDTH = 10
HEIGHT = 10
items = [Item(5, 9, 1), Item(4, 2, 2), Item(10, 6, 3),
         Item(5, 7, 4), Item(6, 3, 5), Item(10, 7, 6),
         Item(1, 5, 7), Item(3, 5, 8), Item(6, 9, 9),
         Item(2, 4, 10), Item(6, 7, 11), Item(7, 2, 12),
         Item(8, 3, 13), Item(4, 10, 14), Item(4, 5, 15),
         Item(10, 3, 16), Item(7, 8, 17), Item(8, 7, 18)]


# --------------------------------- FINITE BEST STRIP ---------------------------------


def minimum_residual_space(root, shelf_height, minimum):
    """
    Cherche la boîte dont l'espace vertical résiduel est minimum pour le niveau à insérer.
    Complexité temporelle : O(log(n))

    @param root : Un noeud de l'arbre AVL (on commence généralement à la racine).
    @param shelf_height : La hauteur du niveau à insérer.
    @param minimum : Un noeud de l'arbre AVL (paramètre évolutif qui stocke la meilleure boîte pour le niveau)
    @return : Le noeud de l'arbre AVL qui contient la boîte la plus adéquate pour le niveau à insérer.
    """
    if root is None:
        return minimum
    elif root.residual_space > shelf_height:
        return minimum_residual_space(root.left, shelf_height, root)
    elif root.residual_space < shelf_height:
        return minimum_residual_space(root.right, shelf_height, minimum)
    else:
        return root


def finite_best_strip(items):
    """
    Cette méthode implémente l'heuristique FBS qui trie initialement les items par hauteur décroissante et se compose
    de deux phases. Tout d'abord, les items sont emballés dans une bande de hauteur infinie et répartis sur différents
    niveaux qui ont une largeur égale à la largeur de la bande et une hauteur différente. Dans la deuxième phase les
    niveaux sont rangées dans des boîtes.
    Complexité temporelle : O(n log(n))

    @param items : Les items à répartir dans les boîtes.
    @return : La liste des boîtes contenant les items.
    """
    strip = Strip(WIDTH, items)
    strip.fill()
    bins = []
    avl = AVLTree()
    avl_residual_space = None
    for shelf in strip.shelves:
        if len(bins) == 0:
            bins.append(Bin(WIDTH, HEIGHT))
            bins[0].add_shelf(shelf)
            avl_residual_space = avl.insert_node(avl_residual_space, bins[0].residual_vertical_space, bins[0])
        else:
            result = minimum_residual_space(avl_residual_space, shelf.height, None)
            if result is None:
                bins.append(Bin(WIDTH, HEIGHT))
                bins[-1].add_shelf(shelf)
                avl_residual_space = avl.insert_node(avl_residual_space, bins[-1].residual_vertical_space, bins[-1])
            else:
                result.list[0].add_shelf(shelf)
                temp = result.list[0]
                avl_residual_space = avl.delete_node(avl_residual_space, result.residual_space, True)
                avl_residual_space = avl.insert_node(avl_residual_space,
                                                     temp.residual_vertical_space,
                                                     temp)
    return bins


# --------------------------------- LOCAL SEARCH ---------------------------------

def quantity(bin):
    """
    Donne une quantité relative à une boîte qui sera utile pour décider de la "weakest bin".
    Complexité temporelle : O(n²)

    @param bin : Une liste de boîtes contenant des items.
    @return : La quantité de la boîte donnée.
    """
    return (5 * (bin.items_weight() / (HEIGHT * WIDTH))) - (bin.nb_items() / len(items))


def weakest_bin(bins):
    """
    Donne la "weakest bin" parmi toutes les boîtes.
    Complexité temporelle : O(n^3)

    @param bins : Une liste de boîtes contenant des items.
    @return : La "weakest bin".
    """
    weakest = None
    weakest_quantity = 0
    for bin in bins:
        if weakest is None:
            weakest = bin
            weakest_quantity = quantity(weakest)
        else:
            bin_quantity = quantity(bin)
            if bin_quantity < weakest_quantity:
                weakest = bin
                weakest_quantity = bin_quantity
    return weakest


def local_search(bins):
    """
    Cette méthode implémente la recherche locale qui explore le voisinage de la solution initiale en déterminant
    la "weakest bin" et en considérant, tour à tour, chaque élément actuellement rangé dans la "weakest bin" et
    dans les autres boîtes.

    @param bins : Une liste de boîtes contenant des items.
    @return : La liste de boîtes possiblement amélioré.
    """
    weakest = weakest_bin(bins)
    while True:
        if weakest.nb_items() == 0:
            bins.remove(weakest)
            weakest = weakest_bin(bins)
        size_weakest = weakest.nb_items()
        for shelf in weakest.shelves:
            for item in shelf.items:
                for bin in bins:
                    if bin != weakest:
                        result = finite_best_strip(bin.items() + [item])
                        if len(result) == 1:
                            bins.remove(bin)
                            bins.append(result[0])
                            tmp = item.width
                            shelf.items.remove(item)
                            if len(shelf.items) == 0:
                                weakest.residual_vertical_space += shelf.height
                                weakest.shelves.remove(shelf)
                            else:
                                shelf.residual_horizontal_space += tmp
                                weakest.residual_vertical_space = (weakest.residual_vertical_space + shelf.height -
                                                                   shelf.items[0].height)
                                shelf.height = shelf.items[0].height
                            break
        if weakest.nb_items() == size_weakest:
            break


# --------------------------------- SHAKING / DIVERSIFICATION PROCEDURE ---------------------------------
def shaking(current_packing, k):
    """
    Cette méthode implémente la "shaking procedure" qui utilise une répartition initiale d'items dans des boîtes
    et procède à une diversification en déplaçant séparément un certain nombre de ces items dans de nouvelles boîtes.

    @param current_packing : Une liste de boîtes contenant des items.
    @param k : Le nombre d'items à insérer séparément dans une nouvelle boîte.
    """
    if k > len(items):
        print("Erreur : trop d'items à modifier")
    else:
        nb_bins = len(current_packing)
        for i in range(k):
            random_number = random.randrange(nb_bins)
            random_bin = current_packing[random_number]
            random_shelf = random.choice(random_bin.shelves)
            random_item = random.choice(random_shelf.items)
            current_packing.append(Bin(WIDTH, HEIGHT))
            current_packing[-1].add_shelf(Shelf(WIDTH, random_item.height))
            current_packing[-1].shelves[0].add_item(random_item)
            tmp = random_item.width
            random_shelf.items.remove(random_item)
            if len(random_shelf.items) == 0:
                random_bin.residual_vertical_space += random_shelf.height
                random_bin.shelves.remove(random_shelf)
                if len(random_bin.shelves) == 0:
                    current_packing.remove(random_bin)
                    nb_bins = nb_bins - 1
            else:
                random_shelf.residual_horizontal_space += tmp
                random_bin.residual_vertical_space = (random_bin.residual_vertical_space + random_shelf.height -
                                                      random_shelf.items[0].height)
                random_shelf.height = random_shelf.items[0].height


# --------------------------------- Basic Variable Neighborhood Search ---------------------------------
def basic_variable_neighborhood_search(items, max):
    """
    Cette méthode effectue le "basic variable neighborhood search".

    @param items : Les items à répartir dans les boîtes
    @param max : Un nombre maximum d'itérations à effectuer avant d'arrêter la fonction.
    @return : Une liste de boîtes contenant les items et représentant la solution "optimale"
    """
    optimal_solution = finite_best_strip(items)
    local_search(optimal_solution)
    k = 1
    tmp = copy.deepcopy(optimal_solution)
    while k <= max:
        shaking(tmp, random.randrange(len(items)))
        local_search(tmp)
        if len(tmp) <= len(optimal_solution):
            optimal_solution = copy.deepcopy(tmp)
        k = k + 1
    return optimal_solution


def draw_bins(canvas, bins):
    """
    Permet d'afficher les boîtes contenant les items.

    @param canvas : Une interface graphique où dessiner les boîtes.
    @param bins : Les boîtes contenant les items.
    """
    x = 50
    for bin in bins:
        y = 100
        canvas.create_rectangle(x, y, x + bin.width * 8, y + bin.height * 8)
        y += bin.height * 8
        tmp = x
        for shelf in bin.shelves:
            for item in shelf.items:
                canvas.create_rectangle(x, y - item.height * 8, x + item.width * 8, y, fill="green")
                text_x = (x + item.width * 4)
                text_y = (y - item.height * 4)
                canvas.create_text(text_x, text_y, text=item.number, fill="white")
                x += item.width * 8
            y -= shelf.height * 8
            x = tmp
        x += bin.width * 2 + 100


def draw_items(canvas, items):
    """
    Permet d'afficher les items à insérer.

    @param canvas : Une interface graphique où dessiner les items.
    @param items : Les items à insérer.
    """
    x0, y0 = 50, 150
    for item in items:
        x1 = x0 + item.width * 8
        canvas.create_rectangle(x0, y0 - item.height * 8, x1, y0, fill="green")
        text_x = (x0 + x1) / 2
        text_y = (y0 - item.height * 4)
        canvas.create_text(text_x, text_y, text=item.number, fill="white")
        x0 = x1 + 10


def draw_strip(canvas, strip):
    """
    Permet d'afficher la bande.

    @param canvas : Une interface graphique où dessiner la bande.
    @param strip : La bande.
    """
    x = 50
    y = 50
    for shelf in strip.shelves:
        y += shelf.height * 8
    for shelf in strip.shelves:
        for item in shelf.items:
            canvas.create_rectangle(x, y - item.height * 8, x + item.width * 8, y, fill="green")
            text_x = (x + item.width * 4)
            text_y = (y - item.height * 4)
            canvas.create_text(text_x, text_y, text=item.number, fill="white")
            x += item.width * 8
        x = 50
        canvas.create_rectangle(x, y - shelf.height * 8, x + shelf.width * 8, y, outline="red")
        y -= shelf.height * 8


if __name__ == '__main__':
    """
    strip = Strip(10, items)
    print("Avant classement par hauteur décroissante")
    print(strip.items)
    # strip.sort_items_decreasing_height()
    # print("Après classement par hauteur décroissante")
    # print(strip.items)
    print("")
    # print("----------Test Strip----------")
    # strip = Strip(WIDTH,items)
    # strip.fill()
    # print(strip)
    # print("Nombre de niveau : " + str(len(strip.list)) + "\n")
    print("------Test Bins------" + "\n")
    bins = finite_best_strip(items)
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i]))
    print("Nombre de bins : " + str(len(bins)))
    print("")
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items()))
    print("---------Test fonction poids items---------")
    print("Poids des items du bin 1 : " + str(bins[0].items_weight()))
    print("")
    print("---------Test fonction weakest bin---------")
    print("Weakest bin : " + str(weakest_bin(bins)))
    print("---------Vérification que le weakest bin est correct---------")
    print("")
    for i in range(len(bins)):
        print("Bin %s quantity : " % i + str(quantity(bins[i])))
    print("")
    print("---------Test Local search---------")
    print("")
    local_search(bins)
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items()))
    print("")
    """
    """
    print("---------Test Shaking---------")
    print("")
    shaking(bins, 5)
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items()))
    print("")
    """
    print("---------Basic Variable Neighborhood Search---------")
    start_time = time.time()
    max = 100
    print("Pour", max, "itérations :")
    optimal = basic_variable_neighborhood_search(items, max)
    end_time = time.time()
    print("Nombre de boîtes dans la solution \"optimale\" :", len(optimal))
    print("Temps exécution :", end_time - start_time, "secondes")
    root = tk.Tk()
    root.title("Affichage")
    canvas = tk.Canvas(root, width=3000, height=5000)
    canvas.pack()
    draw_bins(canvas, optimal)
    root.mainloop()


