# -*- coding: utf-8 -*-
# create Thread Instance,Passing in Function

import threading
from time import sleep, ctime

loops = [4,2]

def loop(nloop, nsec):
    print('start loop', nloop, 'at: ', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at: ', ctime())

def main():
    print('starting at: ', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at: ', ctime())

if __name__ == '__main__':
    main()

# starting at:  Tue Jul  5 17:04:33 2016
# start loop 0 at:  Tue Jul  5 17:04:33 2016
# start loop 1 at:  Tue Jul  5 17:04:33 2016
# loop 1 done at:  Tue Jul  5 17:04:35 2016
# loop 0 done at:  Tue Jul  5 17:04:37 2016
# all DONE at:  Tue Jul  5 17:04:37 2016
