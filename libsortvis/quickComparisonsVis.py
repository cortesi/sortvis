# -*- coding: utf-8 -*-
'''
A quick & dirty demo script using scipy and matplotlib to visualize compared elements.
Created on Nov 14, 2010

@author: joern
'''

from libsortvis import graph, algos, sortable
import random
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

if __name__ == '__main__':
    lst = range(100)
    random.shuffle(lst)
    
    verbose = True # get # of comparisons
    debug = False
    drawComparisons = True # mark each comparison between 2 elements with a dot on both
    compress = False # only draw each column if it changed.
    
    createGraphic = False # save output
    
    if createGraphic:
        gstart = graph.rgb("ffffff")
        gend = graph.rgb("000000")
        csource = graph.ColourGradient(gstart, gend)
        background = graph.rgb("ffffff")
        titlecolour = graph.rgb("000000")
        line = 6
        border = 1
        titleheight = 20
        rotate = False
        height = (line + border + 5) * len(lst)
        width = int(height * 3)
        prefix = "" # file output prefix
        title = ""
        ldrawer = graph.Weave(
            csource,
            width,
            height,
            titleheight,
            titlecolour,
            background,
            rotate,
            line,
            border
        )
    
    
    assert not (drawComparisons and compress), "can't show both in one image,"\
        " decide if you want to show which items are compared or only show lists if they change."
    
    todraw = ["timsort", "mergesort", "quicksort", "bubblesort", "insertionsort"]
    
    for algo in todraw:
        if verbose: print algo
        
        track = sortable.TrackList(lst) # wrap lst with our TrackList
        algos.algorithms[algo](track) # apply the sorting algorithm and sort the list
        track.log() # could happen that the last comparison swaps elements, so log again
        
        if verbose:
            print "\t%s comparisons"%(track.total_comparisons)
        
        m = []
        for j in track:
            m.append(j.path)
        a = sc.array(m)
        if compress:
            prev = -1
            todel = []
            for i in range(a.shape[1]):
                col = a[:,i]
                if (col == prev).all():
                    if debug: print "delete column", i
                    todel.append(i)
                prev = col
            a = sc.delete(a, todel, 1)
        assert (a[:,0][sc.array(lst)] == sc.array(lst)[a[:,0]]).all(), \
            "first path column are does not correspond to init positions of all sorted elements"
        assert (sorted(a[:,-1]) == a[:,-1]).all(), \
            "last path column not sorted"
        if debug: print a
        
        
        plt.figure()
        plt.title(algo)
        
        # line colors
        sm = cm.ScalarMappable(cmap=cm.get_cmap("hot"),
                               norm=colors.Normalize(vmin=0, vmax=(1/0.65)*len(lst))) # use only lower 0.65 of cm
        for i,row in enumerate(a):
            c = sm.to_rgba(i)
            plt.plot(row, color=c)
        if drawComparisons:
            comps = sc.array(track.comparisonList)
            plt.plot(range(1,len(track.comparisonList)+1), comps[:,0], 'o', color=(0., 0., 1.), alpha=0.5)
            plt.plot(range(1,len(track.comparisonList)+1), comps[:,1], 'o', color=(1., 0., 0.), alpha=0.5)
        
        
        if createGraphic:
            name = prefix + algo + ".png"
            ldrawer.draw(
                track,
                algo if title else None,
                name,
            )
        
    plt.show()
        
        


