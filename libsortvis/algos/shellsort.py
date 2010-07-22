
def shellsort(lst):
    t = [5, 3, 1]
    for h in t:
        for j in range(h, len(lst)):
            i = j - h
            r = lst[j]
            flag = 0
            while i > -1:
                if r < lst[i]:
                    flag = 1
                    lst[i+h], lst[i] = lst[i], lst[i+h]
                    i -= h
                    lst.log()
                else:
                    break
            lst[i+h] = r

