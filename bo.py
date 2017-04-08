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
from geo.segment import load_segments
from geo.tycat import tycat
from events import Events
from segmenttree import SegmentTree

def bentley_ottmann(segments, adujster):
    """
    computes and returns the result of the bentley ottmann algorithm for the given
    segments and ajuster.
    the intesections are given for each segments.
    """
    # adds all the creation and destruction events for the given segments
    events = Events(segments)
    # creates the structure for the 'alive' segments
    living_segments = SegmentTree()

    while not events.isempty():
        # getting the first event in the events list
        current_event = events.event_list.pop(0)
        


    return events

def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    events = bentley_ottmann(segments, adjuster)
    tycat(segments)
    print(events)
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
