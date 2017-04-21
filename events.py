#! /usr/bin/env python3
"""
Events module
contains the Event object and the Events container.
"""

from sortedcontainers import SortedListWithKey
from geo.point import Point
from geo.segment import Segment

CREATION = 0
DESTRUCTION = 1
INTERSECTION = 2

class Event:
    """
    The Event object corresponds to a creation or a destruction of a
    segment or an intersection between two segments. Each event has a key
    in order to sort it in the Events structure.
    """

    def __init__(self, event_type, point):
        """
        event_type is the type of the event (creation, destruction or intersections),
        coordinates, the coordinates of the Point, and segments a list of
        the segments associated to the point.
        """
        # Keeping the event_type because in case of intersection
        #the computing of it can produce a "past intersection"
        self.type = event_type
        self.key = point

    def event_comparison(self):
        """
        used as a key to compare the elements beetween them.
        """
        return (-self.key.coordinates[1], -self.key.coordinates[0])

class Events:
    """
    Contains all the events and keeps the events in order for the insertion
    and the suppression.
    """

    def __init__(self, segments):
        """
        creates all the events for the initial segments and write them
        in the sortedlist (with key) structure in order to have a near
        tree structure complexity
        """
        self.begin_points = dict()
        self.end_points = dict()
        #TODO: compute the optimal load number
        self.event_list = SortedListWithKey(None, Event.event_comparison)
        for segment in segments:
            self.init_segment_events(segment)

    def __str__(self):
        """
        returns the events from the event list (debugg)
        """
        return " \n ".join([str(event.key) for event in iter(self.event_list)])

    def init_segment_events(self, segment):
        """
        creates two event for the segment
        """
        # Creating the events for the segment
        event_creation = Event(CREATION, segment.endpoints[1])
        event_destruction = Event(DESTRUCTION, segment.endpoints[0])

        # Adding the segment in the hashtables based on the event key
        if event_creation.key in self.begin_points:
            # if the beginning point alreay exists
            self.begin_points[event_creation.key].append(segment)
        else:
            self.begin_points[event_creation.key] = [segment]

        if event_destruction.key in self.end_points:
            self.end_points[event_destruction.key].append(segment)
        else:
            self.end_points[event_destruction.key] = [segment]

        # Add the two events in the events structure
        self.event_list.add(event_creation)
        self.event_list.add(event_destruction)

    def isempty(self):
        """
        returns true is there are no more events in the structure
        """
        return len(self.event_list) == 0

    def finish_segments(self, event, segments, adjuster):
        """
        finishes the segment on event
        """
        for segment in self.end_points[event.key]:
            intersection_points = intersect_with(segment, segments, adjuster)
            for point, inter_segments in intersection_points:
                # if point not in the past
                if point < Segment.current_point:
                    # If the intersection already exists
                    if self.begin_points[point] is not None:
                        # Adds the segment to the existing intersection
                        # A new event is not needed
                        #TODO
                        pass
                    else:
                        # Creates the intersection event and add it to the
                        # hashtables of segments
                        events.event_list.add(Event(INTERSECTION, point))
                        self.begin_segments[point] = [inter_segment]
                        self.end_points[point] = inter_segment

    def update_curent_point(self, event):
        """
        updates the global current point based on the points of the event
        """
        #TODO
        pass

    def begin_segments(self, event, segments):
        """
        begins the segments on event
        """
        #TODO
        pass

def intersect_with(segment, segments, adjuster):
    """
    computes the intersection with the closest segments from segment
    and returns a list of adjusted intersections with the segments involved
    (including segment in the parameters)
    """
    #TODO
    pass

def events_init_test():
    """
    test the init of a segment in the series of event
    """
    print("\n------------Segment init test------------")
    events = Events([Segment([Point([1.0, 2.0]), Point([3.0, 4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([3.0, -4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([2.0, 4.0])])])
    print(events)
    print(events.begin_points, "begin points\n")
    print(events.end_points, "end_points\n")
    print("printing the type of each key")
    for key in events.begin_points:
        print(type(key))
    print("-----------------------------------------\n")

if __name__ == "__main__":
    """
    run the tests sequence
    """
    events_init_test()
