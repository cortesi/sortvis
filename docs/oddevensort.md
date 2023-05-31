# oddevensort
![detail](images/weave-oddevensort.png)
## code
```python
def oddevensort(lst, nloops=2):
    finished = False
    while not finished:
        finished = True
        for n in range(nloops):
            for i in range(n, len(lst) - 1, nloops):
                if lst[i] > lst[i + 1]:
                    lst[i], lst[i + 1] = lst[i + 1], lst[i]
                    lst.log()
                    finished = False
```

List order is sampled for visualisation whenever `lst.log()` is called.