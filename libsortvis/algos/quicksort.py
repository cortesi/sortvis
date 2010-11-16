# note: quicksort does unnecessary comparisons of elements  with the same index 
def quicksort(lst, left=0, right=None):
    if right is None:
        right = len(lst) - 1
    l = left
    r = right
    if l <= r: # why not < ?
        mid = lst[(left+right)/2]
        while l <= r: # why not < ?
            while l <= right and lst[l] < mid:
                l += 1
            while r > left and lst[r] > mid:
                r -= 1
            if l <= r:
                lst[l], lst[r] = lst[r], lst[l]
#                if l != r:
#                    lst.log()
                l+=1
                r-=1
        if left < r:
            quicksort(lst, left, r)
        if l < right:
            quicksort(lst, l, right)

