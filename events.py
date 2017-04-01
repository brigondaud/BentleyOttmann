#! /usr/bin/env pytnon3
"""
Events module
contains the Event object and the Events container.
"""

from sortedcontainers import SortedList

CREATION = 0
DESTRUCTION = 1
INTERSECTION = 2

class Event:
    """
    The Event object corresponds to a creation or a destruction of a
    segment or an intersection between two segments. Each event has a key
    in order to sort it in the Events structure.
    """

    def __init__(self, event_type, coordinates):
        """
        event_type is the type of the event (creation, destruction or intersections),
        coordinates, the coordinates of the Point, and segments a list of
        the segments associated to the point.
        """
        #TODO: definition of the class.
        pass
        self.type = event_type
        self.key = coordinates
        self.segments = []

    def event_comparison(self):
        """
        used as a key to compare the elements beetween them.
        """
        return (- self.key[1], - self.key[0])



class Events:
    """
    Contains all the events and keeps the events in order for the insertion
    and the suppression.
    """

    def __init__(self):
        #TODO: compute the optimal load number
        self.event_list = SortedListWithKey(None, Event.event_comparison())
