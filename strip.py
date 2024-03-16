from shelf import *

def merge(arr, l, m, r):
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
    if l < r:
        m = l + (r - l) // 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)


class Strip:
    def __init__(self, width, items):
        self.width = width
        self.items = items
        self.shelves = []

    def non_increasing_height(self):
        merge_sort(self.items, 0, len(self.items) - 1)
        self.items.reverse()

    def add_item(self, item):
        if len(self.shelves) == 0:
            self.shelves.append(Shelf(self.width, item.height))
            self.shelves[0].items.append(item)
            self.shelves[0].remaining_horizontal_space -= item.width
        else:
            result = None
            for shelf in self.shelves:
                if shelf.remaining_horizontal_space >= item.width and result is None:
                    result = shelf
                elif shelf.remaining_horizontal_space >= item.width and result is not None:
                    if shelf.remaining_horizontal_space < result.remaining_horizontal_space:
                        result = shelf
            if result is None:
                self.shelves.append(Shelf(self.width, item.height))
                self.shelves[-1].items.append(item)
                self.shelves[-1].remaining_horizontal_space -= item.width
            else:
                result.items.append(item)
                result.remaining_horizontal_space -= item.width

    def fill(self):
        for item  in self.items:
            self.add_item(item)

    def __repr__(self):
        result = "Largeur de la bande : %s" % self.width + "\n"
        for i in range(len(self.shelves)):
            result += "----------Level %s----------" % i + "\n" + str(self.shelves[i])
        return result

