# -*- coding: utf-8 -*-
__author__ = 'Konrad'

import threading


NUMBER_OF_THREADS = 4
ITERATIONS = 1000000
BOUNDARY_A = 0
BOUNDARY_B = 1


def function_pi(x):
    return 1 / (1 + (x * x))


class ParallelIntegral(threading.Thread):
    gResult = 0
    lock = threading.Lock()

    def __init__(self, A, B, iter):
        threading.Thread.__init__(self)
        self.A = A
        self.B = B
        self.iter = int(iter)
        self.result = 0

    def run(self):
        dx = (self.B - self.A) / self.iter
        for j in range(1, self.iter, 1):
            self.result += function_pi(self.A + (j * dx))
        self.result = (self.result + (function_pi(self.A) + function_pi(self.B)) / 2) * dx
        with ParallelIntegral.lock:
            ParallelIntegral.gResult += self.result


iterations = ITERATIONS / NUMBER_OF_THREADS
divider = (BOUNDARY_B - BOUNDARY_A) / NUMBER_OF_THREADS
thread = []
for i in range(0, NUMBER_OF_THREADS-1):
    thread.append(ParallelIntegral(BOUNDARY_A + i * divider, BOUNDARY_A + (i + 1) * divider, iterations))
thread.append(ParallelIntegral(BOUNDARY_A + (NUMBER_OF_THREADS-1)*divider, BOUNDARY_B, iterations))

for t in thread:
    t.start()

for t in thread:
    t.join()

print(4 * ParallelIntegral.gResult)