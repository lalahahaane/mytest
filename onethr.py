# -*- coding: utf-8 -*-

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
    loop0()
    loop1()
    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()

# starting at: Mon Jul  4 19:40:41 2016
# start loop 0 at: Mon Jul  4 19:40:41 2016
# loop 0 done at: Mon Jul  4 19:40:45 2016
# start loop 1 at: Mon Jul  4 19:40:45 2016
# loop 1 done at: Mon Jul  4 19:40:47 2016
# all DONE at: Mon Jul  4 19:40:47 2016