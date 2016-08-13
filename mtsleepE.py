# -*- coding: utf-8 -*-
# subclass Thread and Create Subclass Instance

import threading
from time import sleep, ctime

loops = (4, 2)

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

def loop(nloop, nsec):
    print('start loop', nloop, 'at: ', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at: ', ctime())

def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops: # start all threads
        threads[i].start()

    for i in nloops: # wait for competion
        threads[i].join()

    print('all DONE at: ', ctime())

if __name__ == '__main__':
    main()

# starting at: Tue Jul  5 22:46:24 2016
# start loop 0 at:  Tue Jul  5 22:46:24 2016
# start loop 1 at:  Tue Jul  5 22:46:24 2016
# loop 1 done at:  Tue Jul  5 22:46:26 2016
# loop 0 done at:  Tue Jul  5 22:46:28 2016
# all DONE at:  Tue Jul  5 22:46:28 2016
