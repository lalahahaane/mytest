# -*- coding: utf-8 -*-

from threading import Thread

import time

class CountdownTask:
    def __init__(self):
        self._running = True
        # self.n = 0

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

import multiprocessing
c = CountdownTask()
p = multiprocessing.Process(target=c.run, args=(5,))
p.start()