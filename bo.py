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
from sortedcontainers import SortedListWithKey
from geo.segment import load_segments
from geo.tycat import tycat
from events import Events

CREATION = 0
DESTRUCTION = 1
INTERSECTION = 2

def bentley_ottmann(segments, adujster):
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
    living_segments = SortedListWithKey(None, lambda segment_tuple: segment_tuple[1])

    while not events.isempty():
        # getting the first event in the events list
        current_event = events.event_list.pop(0)
        if current_event.type == CREATION:
            current_segment = current_event.segments[0]
            #the key corresponds to an endpoint of a living segment
            living_segments.add([current_segment, segment_key_compute(current_event, current_segment)])

    return events

def segment_key_compute(event, segment):
    """
    computes the key = [abscissa, angle] based on the current event ordinate
    and the segment.
    """
    # sweep_line = Segment(Point([]))
    #TODO: compute segment keg

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
