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


def doublon(liste, solution):
    for ind, el1 in enumerate(liste):
        for el2 in liste[ind+1:]:
            if el1 == el2:
                print(el1)
                tycat(solution.segments(), el1)
                for i in range(3):
                    print("YA UN PUTAIN DE DOUBLON")

def bentley_ottmann(segments, adjuster, solution):
    """
    computes and returns the result of the bentley ottmann algorithm for the given
    segments and ajuster.
    the intesections are given for each segments.
    """
    # adds all the creation and destruction events for the given segments
    events = Events(segments)

    # creates the structure for the 'alive' segments:
    # the structure contains a list with the segment and it's key
    #TODO: compute the optimal load for living segments
    living_segments = SortedList()
    Segment.current_point = None
    while not events.isempty():
        # getting the first event in the events list
        current_event = events.event_list.pop(0)

        #finishing the segments which end on the current event
        events.finish_segments(current_event, living_segments, adjuster, solution)

        #updating the global current point
        Segment.current_point = current_event.key

        #beginning the segments which start from the current_event
        events.begin_segments(current_event, living_segments, adjuster, solution)

        solution.draw_step(living_segments, Segment.current_point)

def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    # Initializes the solution for the segments
    solution = Solution(segments)
    bentley_ottmann(segments, adjuster, solution)
    tycat(segments)
    tycat(solution.segments(), solution.intersection_points())

    #TODO: merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    #...
    #tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
