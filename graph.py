#!/usr/bin/env python3
"""
Module graph
"""
import sys
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
from bo import test

def theo_graph(x):
    return (x/4000)*np.log10(x)

def draw_graph(test_file):
    """
    draw a graph based on the test for the bentley ottmann algorithm
    """
    results = []
    for file in test_file:
        time1 = perf_counter()
        solution = test(file)
        time2 = perf_counter()
        results.append((len(list(solution.segments())), time2-time1))
    results.sort()
    plot_x, plot_y = [], []
    for seg_number, time in results:
        plot_x.append(seg_number)
        plot_y.append(time)
    plt.plot(plot_x, plot_y, 'ro')
    x_log = np.arange(0, 10000, 1)
    plt.plot(x_log, theo_graph(x_log))
    plt.show()

draw_graph(sys.argv[1:])
