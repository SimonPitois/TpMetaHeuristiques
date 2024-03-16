from item import *
from strip import *
from bin import *

WIDTH = 10
HEIGHT = 10
donnees = [Item(5,9),Item(4,2),Item(10,6),Item(5,7),Item(6,3),Item(10,7),Item(1,5),Item(3,5),Item(6,9),Item(2,4), Item(6,7),Item(7,2),Item(8,3),Item(4,10),Item(4,5), Item(10,3), Item(7,8), Item(8,7)]


# FINITE BEST STRIP
def finite_best_strip(donnees):
    strip = Strip(WIDTH, donnees)
    strip.fill()
    bins = []
    for shelf in strip.shelves:
        if len(bins) == 0:
            bins.append(Bin(WIDTH,HEIGHT))
            bins[0].shelves.append(shelf)
            bins[0].remaining_vertical_space -= shelf.height
            bins[0].items += shelf.items
        else:
            result = None
            for bin in bins:
                if bin.remaining_vertical_space >= shelf.height and result is None:
                    result = bin
                elif bin.remaining_vertical_space >= shelf.height and result is not None:
                    if bin.remaining_vertical_space < result.remaining_vertical_space:
                        result = bin
            if result is None:
                bins.append(Bin(WIDTH, HEIGHT))
                bins[-1].shelves.append(shelf)
                bins[-1].remaining_vertical_space -= shelf.height
                bins[-1].items += shelf.items
            else:
                result.shelves.append(shelf)
                result.remaining_vertical_space -= shelf.height
                result.items += shelf.items
    return bins


def quantity(bin):
    return (5 * (bin.items_weight() / (HEIGHT * WIDTH))) - (bin.nb_items() / len(donnees))


def weakest_bin(bins):
    weakest = None
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


# LOCAL SEARCH
def local_search(bins):
    weakest = weakest_bin(bins)
    stop = False
    while not stop:
        if weakest.nb_items() == 0:
            bins.remove(weakest)
            weakest = weakest_bin(bins)
        size_weakest = len(weakest.items)
        for item in weakest.items:
            for bin in bins:
                if bin != weakest:
                    result = finite_best_strip(bin.items + [item])
                    if len(result) == 1:
                        bins.remove(bin)
                        bins.apppend(result[0])
                        weakest.items.remove(item)
                        for shelf in weakest.shelves:
                            if item in shelf.items:
                                shelf.items.remove(item)
                                if len(shelf.items) == 0:
                                    weakest.shelves.remove(shelf)
                                break
                        break
        if len(weakest.items) == size_weakest:
            stop = True

# SHAKING / DIVERSIFICATION PROCEDURE


if __name__ == '__main__':
    strip = Strip(10,donnees)
    print("Avant classement par hauteur décroissante")
    print(strip.items)
    strip.non_increasing_height()
    print("Après classement par hauteur décroissante")
    print(strip.items)
    print("")
    #print("----------Test Strip----------")
    #strip = Strip(WIDTH,donnees)
    #strip.fill()
    #print(strip)
    #print("Nombre de niveau : " + str(len(strip.shelves)) + "\n")
    print("------Test Bins------" + "\n")
    bins = finite_best_strip(donnees)
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i]))
    print("Nombre de bins : " + str(len(bins)))
    print("")
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items))
    print("")
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
    local_search(bins)
    print("")
    for i in range(len(bins)):
        print("----------Bin %s----------" % i + "\n" + str(bins[i].items))
