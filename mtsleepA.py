# -*- coding: utf-8 -*-

import _thread
from time import sleep, ctime

def loop0():
    print('start loop 0 at:', ctime())
    sleep(4)
    print('loop 0 done at:', ctime())

def loop1():
    print('start loop 1 at:', ctime())
    sleep(2)
    print('loop 1 done at:', ctime())

def main():
    print('starting at:', ctime())
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    sleep(6)
    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()

# starting at: Mon Jul  4 20:06:19 2016
# start loop 0 at: Mon Jul  4 20:06:19 2016
# start loop 1 at: Mon Jul  4 20:06:19 2016
# loop 1 done at: Mon Jul  4 20:06:21 2016
# loop 0 done at: Mon Jul  4 20:06:23 2016
# all DONE at: Mon Jul  4 20:06:25 2016