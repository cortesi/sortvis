from itertools import chain

def radixsort(lst):
    is_sorted = lambda l: all([a < b for a, b in zip(l[:-1], l[1:])])
    shift = 1
    zeroes = []
    ones = []
    while not is_sorted(lst.lst):
        orig = lst.lst[:]
        while len(orig) != 0:
            # take an item out of the list
            item = orig.pop(0)
            # put it in the right bucket
            if (item.i & shift) == 0:
                zeroes.append(item)
            else:
                ones.append(item)
            # copy the items back into the main list
            for j, item in enumerate(chain(zeroes, orig, ones)):
                lst[j] = item
            # for a more simple graph, comment out the line below
            lst.log()
            #
            if is_sorted(lst):
                return
        lst.log()
        shift = shift << 1
        zeroes[:] = []
        ones[:] = []
