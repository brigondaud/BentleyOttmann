#! /usr/bin/env pytnon3
"""
Events module
contains the Event object and the Events container.
"""

from sortedcontainers import SortedList

class Event:
    """
    The Event object corresponds to a creation or a destruction of a
    segment or an intersection between two segments. Each event has a key
    in order to sort it in the Events structure.
    """

    def __init__(self, event_type):
        #TODO: definition of the class.
        pass

class Events:
    """
    Contains all the events and keeps the events in order for the insertion
    and the suppression.
    """

    def __init__(self):
        #TODO: definition of the class.
        pass
