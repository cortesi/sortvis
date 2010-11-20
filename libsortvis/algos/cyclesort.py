

def cyclesort(lst):
    for i in range(len(lst)):
        if i != lst[i]:
            n = i
            while 1: 
                tmp = lst[int(n)]
                if n != i:
                    lst[int(n)] = last_value
                    lst.log()
                else:
                    lst[int(n)] = None
                    lst.log()
                last_value = tmp
                n = last_value
                if n == i:
                    lst[int(n)] = last_value
                    lst.log()
                    break


