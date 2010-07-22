
def quicksort(lst, left=0, right=None):
    if right is None:
        right = len(lst) - 1
    l = left
    r = right
    if l <= r:
        mid = lst[(left+right)/2]
        while l <= r:
            while l <= right and lst[l] < mid:
                l += 1
            while r > left and lst[r] > mid:
                r -= 1
            if l <= r:
                lst[l], lst[r] = lst[r], lst[l]
                if l != r:
                    lst.log()
                l+=1
                r-=1
        if left < r:
            quicksort(lst, left, r)
        if l < right:
            quicksort(lst, l, right)

