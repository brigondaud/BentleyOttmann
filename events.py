#! /usr/bin/env python3
"""
Events module
contains the Event object and the Events container.
"""

from sortedcontainers import SortedList, SortedListWithKey
from geo.point import Point
from geo.segment import Segment
from geo.coordinates_hash import CoordinatesHash

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
            #Adds the event in the events structure
            self.event_list.add(event_creation)

        if event_destruction.key in self.end_points:
            self.end_points[event_destruction.key].append(segment)
        else:
            self.end_points[event_destruction.key] = [segment]
            #Adds the event in the event structure
            self.event_list.add(event_destruction)

    def isempty(self):
        """
        returns true is there are no more events in the structure
        """
        return len(self.event_list) == 0

    def finish_segments(self, event, living_segments, adjuster):
        """
        finishes the segments on event
        """
        #TODO: add the computed intersection in the solution
        #FIXME: check for intersections between the left and right neighbours
        # from the segment that has just beeen removed
        for segment in self.end_points[event.key]:
            # Computes the intersections for each segment
            self.check_intersection(event, segment, living_segments, adjuster)

            # Removing the current segment from the living segment
            living_segments.pop(segment)

    def begin_segments(self, event, living_segments, adjuster):
        """
        begins the segments on event
        """
        #TODO: add the coputed intersection to the solution

        for segment in self.begin_points[event.key]:
            # Adds the segment to the living segments
            living_segments.add(segment)
            # Checks the intersection with the added segment
            self.check_intersection(event, segment,
                                    living_segments,
                                    adjuster)

    def check_intersection(self, event, segment, segments, adjuster):
        """
        check intersection
        """
        for inter_point, inter_segment in intersect_with(event, segment,
                                                         segments,
                                                         adjuster):
            # if point not in the past
            if inter_point > Segment.current_point:
                # If the intersection does not exists
                if self.begin_points[inter_point] is None:
                    # Creates the intersection event and add it to the
                    # hashtables of segments
                    self.event_list.add(Event(INTERSECTION, inter_point))

                    # Creates the entry in the hastable
                    self.begin_points[inter_point] = []
                    self.end_points[inter_point] = []

                # if the intersection point already exists and if the
                # current segment is involved => it is already in *_points
                if segment not in self.begin_points[inter_point]:
                    # Adds the segment to the hashtable with the computed intersection
                    self.begin_points[inter_point].append(segment)
                    self.end_points[inter_point].append(segment)
                self.begin_points[inter_point].append(inter_segment)
                self.end_points[inter_point].append(inter_segment)

def intersect_with(event, segment, living_segments, adjuster):
    """
    computes the intersection with the closest segments from segment
    and iterates on the adjusted intersections with the segments involved
    """
    # Searching for the current segment in the living segments
    # and searching for its nearest neighbours
    for neighbour in neighbours(segment, living_segments):
        inter_point = segment.intersection_with(neighbour)
        # if there's an intersection
        if inter_point is not None:
            inter_point = adjuster.hash_point(inter_point)
            yield inter_point, neighbour
    if event.type == INTERSECTION:
        # Can produce intersection that already exists
        #TODO
        pass

def neighbours(segment, segments):
    """
    yields the neighbour segments of segment in segments
    """
    print("liste des segments vivants: ", segments)
    # segment_index = segments.index(segment)
    #TODO: debugg the index with minus sign on the angle to replace naive search
    for index, seg in enumerate(segments):
        if seg is segment:
            segment_index = index
    if segment_index < len(segments)-1:
        yield segments[segment_index + 1]
    if segment_index > 0:
        yield segments[segment_index - 1]

def events_init_test():
    """
    test the init of a segment in the series of event
    """
    print("\n------------Segment init test------------")
    events = Events([Segment([Point([1.0, 2.0]), Point([3.0, 4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([3.0, -4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([2.0, 4.0])])])
    print(events)
    print("-----------------------------------------\n")

def intersection_test():
    """
    test the intersection on basic cases with one or two neighbours
    """
    print("\n---------Intersection neighbour test---------")
    seg1 = Segment([Point([0, 0]), Point([2, 2])])
    seg2 = Segment([Point([1, 0]), Point([1, 2])])
    events = Events([seg1, seg2])
    print("events:", events)

    Segment.current_point = Point([2.0, 2.0])
    living_segments = SortedList()
    living_segments.add(seg1)
    living_segments.add(seg2)

    while not events.isempty():
        current_event = events.event_list.pop(0)
        print("\ncurrent event: ", current_event.key)
        if current_event.key in events.begin_points:
            for segment in events.begin_points[current_event.key]:
                print("segment étudié :", segment)
                print([ p for p in intersect_with(current_event,
                                     segment,
                                     living_segments,
                                     CoordinatesHash())])

    print("-----------------------------------------\n")

if __name__ == "__main__":
    """
    run the tests sequence
    """
    events_init_test()
    intersection_test()
