import random
from item import *
from strip import *
from bin import *

WIDTH = 10
HEIGHT = 10
donnees = [Item(5, 9), Item(4, 2), Item(10, 6),
           Item(5, 7), Item(6, 3), Item(10, 7),
           Item(1, 5), Item(3, 5), Item(6, 9),
           Item(2, 4), Item(6, 7), Item(7, 2),
           Item(8, 3), Item(4, 10), Item(4, 5),
           Item(10, 3), Item(7, 8), Item(8, 7)]


def minimum_residual_space(root, shelf_height, minimum):
    """
    Cherche la boîte dont l'espace vertical résiduel est minimum pour le niveau à insérer.
    Complexité temporelle : O(log(n))

    @param root: Un noeud de l'arbre AVL (on commence généralement à la racine).
    @param shelf_height: La hauteur du niveau à insérer.
    @param minimum: Un noeud de l'arbre AVL (paramètre évolutif qui stocke la meilleure boîte pour le niveau)
    @return: Le noeud de l'arbre AVL qui contient la boîte la plus adéquate pour le niveau à insérer.
    """
    if root is None:
        return minimum
    elif root.residual_space > shelf_height:
        return minimum_residual_space(root.left, shelf_height, root)
    elif root.residual_space < shelf_height:
        return minimum_residual_space(root.right, shelf_height, minimum)
    else:
        return root


# --------------------------------- FINITE BEST STRIP ---------------------------------
def finite_best_strip(donnees):
    strip = Strip(WIDTH, donnees)
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


def quantity(bin):
    """
    Donne une quantité relative à une boîte et qui sera utile pour décider de la "weakest bin"
    Complexité temporelle : O(n²)

    @param bin: Une boîte.
    @return: La quantité de la boîté donnée.
    """
    return (5 * (bin.items_weight() / (HEIGHT * WIDTH))) - (bin.nb_items() / len(donnees))


def weakest_bin(bins):
    """
    Donne la "weakest bin" parmi toutes les boîtes.
    Complexité temporelle : O(n^3)

    @param bins: Des boîtes.
    @return: La "weakest bin".
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


# --------------------------------- LOCAL SEARCH ---------------------------------
def local_search(bins):
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
                            shelf.items.remove(item)
                            if len(shelf.items) == 0:
                                weakest.shelves.remove(shelf)
                            break
        if weakest.nb_items() == size_weakest:
            break


# --------------------------------- SHAKING / DIVERSIFICATION PROCEDURE ---------------------------------
def shaking(current_packing, k):
    if k > len(donnees):
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
            random_shelf.items.remove(random_item)
            if len(random_shelf.items) == 0:
                random_bin.shelves.remove(random_shelf)
            if len(random_bin.shelves) == 0:
                current_packing.remove(random_bin)
                nb_bins = nb_bins - 1


def basic_variable_neighborhood_search(donnees):
    best_solution = finite_best_strip(donnees)
    local_search(best_solution)
    while len(best_solution) != 6:
        #for i in range(len(best_solution)):
            #print("----------Bin %s----------" % i + "\n" + str(best_solution[i].items()))
        #print("")
        shaking(best_solution,4)
        local_search(best_solution)


if __name__ == '__main__':
    """
    strip = Strip(10, donnees)
    print("Avant classement par hauteur décroissante")
    print(strip.items)
    # strip.sort_items_decreasing_height()
    # print("Après classement par hauteur décroissante")
    # print(strip.items)
    print("")
    # print("----------Test Strip----------")
    # strip = Strip(WIDTH,donnees)
    # strip.fill()
    # print(strip)
    # print("Nombre de niveau : " + str(len(strip.list)) + "\n")
    print("------Test Bins------" + "\n")
    bins = finite_best_strip(donnees)
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
    print("---------Test Random---------")
    print("")
    random_numb = random.randrange(len(bins))
    print(random_numb)
    print("")
    print("---------Test Shaking---------")
    print("")
    shaking(bins, 5)
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items()))
    print("")
    """
    print(int(len(donnees) / 3))
    basic_variable_neighborhood_search(donnees)
    print("Done")
