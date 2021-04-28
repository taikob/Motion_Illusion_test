import numpy as np
import random

def rand_ints_nodup(a, b, k):
  ns = []
  while len(ns) < k:
    n = random.randint(a, b)
    if not n in ns:
      ns.append(n)
  return ns

def make_sheet(nitr,max,nd):
    #nitr : number of iteration
    #rottable : rotation table

    algnlist=[]#align list
    nall=nitr*nd*2
    for i in [0,1]:#mirror or original
        for j in np.linspace(-max, max, nd):# rotation speed
            for n in range(nitr):
                algnlist.append([i,j])

    randlist=rand_ints_nodup(0, nall-1, nall)

    testsheet=[]
    for i in randlist:
        testsheet.append(algnlist[i])

    return testsheet