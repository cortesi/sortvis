import bubblesort

algorithms = {}
def _algo(name):
    m = __import__(name, globals(), locals(), fromlist=[], level=-1)
    algorithms[name] = getattr(m, name)


_algo("bubblesort")
_algo("cocktailsort")
_algo("combsort")
_algo("gnomesort")
_algo("heapsort")
_algo("insertionsort")
_algo("mergesort")
_algo("oddevensort")
_algo("quicksort")
_algo("radixsort")
_algo("selectionsort")
_algo("shellsort")
_algo("smoothsort")
_algo("stoogesort")
_algo("timsort")

