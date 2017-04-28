#!/usr/bin/env python3
"""
Module graph
"""

from time import perf_counter
from bo import test
import matplotlib.pyplot as plt

def draw_graph(*test_file):
    """
    draw a graph based on the test for the bentley ottmann algorithm
    """
    plt.plot([1, 2], [2, 4], "ro")
    plt.show()
    results = []
    for file in test_file:
        time1 = perf_counter()
        solution = test(file)
        time2 = perf_counter()
        results.append((len([solution.segments()]), time2-time1))
    results.sort()
    plot_x, plot_y = [], []
    for seg_number, time in results:
        plot_x.append(seg_number)
        plot_y.append(time)
    plt.plot(plot_x, plot_y, "ro")
    plt.show()
