#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""
import sys
from sortedcontainers import SortedList
from geo.segment import Segment, load_segments
from geo.tycat import tycat
from events import Events
from solution import Solution

CREATION = 0
DESTRUCTION = 1
INTERSECTION = 2

def bentley_ottmann(segments, solution):
    """
    computes and returns the result of the bentley ottmann algorithm for the given
    segments and ajuster.
    the intesections are given for each segments.
    """
    # adds all the creation and destruction events for the given segments
    events = Events(segments)


    # creates the structure for the 'alive' segments:
    # the structure contains a list with the segment and it's key
    living_segments = SortedList()
    Segment.current_point = None

    while not events.isempty():

        # getting the first event in the events list
        current_event = events.event_list.pop(0)

        #finishing the segments which end on the current event
        events.finish_segments(current_event, living_segments, solution)

        #updating the global current point
        Segment.current_point = current_event.key

        #beginning the segments which start from the current_event
        events.begin_segments(current_event, living_segments, solution)

def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)

    # The adjuster is used by all the segments to compute their keys
    Segment.adjuster = adjuster

    # Initializes the solution for the segments
    solution = Solution(segments)

    # Algorithm
    bentley_ottmann(segments, solution)

    # Printing the output of the algorithm
    tycat(segments)
    tycat(solution.segments(), solution.intersection_points())
    solution.summary()

    # Compute the solution with the simple algorithm
    # solution.simple_algorithm()

    # In order to draw graph
    return solution

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
