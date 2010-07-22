
def combsort(lst):
    gap = len(lst)
    swaps = False
    while 1:
        gap = int(gap / 1.25)
        swaps = False
        for i in xrange(len(lst) - gap):
            if lst[i] > lst[i + gap]:
                lst[i], lst[i + gap] = lst[i + gap], lst[i]
                lst.log()
                swaps = True
        if not swaps and gap <= 1:
            break

