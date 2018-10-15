#!/usr/bin/env python 

import multiprocessing
from time import time
import cPickle
import sys

## Simple func to eat up cpu power.
def whileFunc(z):
    while z < 100000:
        z += 1 
    return z

if __name__ == "__main__":
    ## Get current time 
    currtime = time()

    ## How often to run (just a test value)
    N = 1000
    ## Just a list with 1s 
    myList = [1]*N

    nrOfProcessors = multiprocessing.cpu_count() 

    ## Set our pool of processors 
    po = multiprocessing.Pool(nrOfProcessors)
    
    ## create the threads 
    res = po.map_async(whileFunc, myList)
    
    ## If we pass a -po flag, pickle the output and write it out    
    if '-po' in sys.argv[1:]:
        results = len(res.get())
        cPickle.dump(results, sys.stdout, -1)
        sys.stdout.flush()
        sys.exit(0)

    print 'This value below should be a 1000:'
    print len(res.get())
    print 'time elapsed:', time() - currtime