# bubblesort
![detail](images/weave-bubblesort.png)
## code
```python
def bubblesort(lst):
    bound = len(lst)-1
    while 1:
        t = 0
        for j in range(bound):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                lst.log()
                t = j
        if t == 0:
            break
        bound = t
```

List order is sampled for visualisation whenever `lst.log()` is called.