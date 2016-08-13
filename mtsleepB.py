#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _thread
from time import sleep, ctime

loops = [4,2]

def loop(nloop, nsec, lock):
    print('start loop', nloop, 'at: ', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at: ', ctime())
    lock.release()

def main():
    print('starting at: ', ctime())
    locks = []
    nloops = range(len(loops))

    for i in nloops:
        lock = _thread.allocate_lock() #分配锁
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))
        for i in nloops:
            while locks[i].locked(): pass

    print('all DONE at: ', ctime())

if __name__ == '__main__':
    main()


# starting at:  Mon Jul  4 21:14:44 2016
# start loop 0 at:  Mon Jul  4 21:14:44 2016
# loop 0 done at:  Mon Jul  4 21:14:48 2016





