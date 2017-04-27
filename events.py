#! /usr/bin/env python3
"""
Events module
contains the Event object and the Events container.
"""
#pylint: disable=C0103

from sortedcontainers import SortedList, SortedListWithKey
from geo.point import Point
from geo.segment import Segment
from geo.coordinates_hash import CoordinatesHash
from geo.tycat import tycat

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

    def __eq__(self, other):
        """
        two events are equal if they have the same key
        """
        return self.key == other.key

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

    def event_exists(self, event):
        """
        returns ture if the event already exists in the events structure.
        """
        for ev in self.event_list:
            if ev == event:
                return True
        return False

    def init_segment_events(self, segment):
        """
        creates two event for the segment
        """
        # Creating the events for the segment
        event_creation = Event(CREATION, max(segment.endpoints))
        event_destruction = Event(DESTRUCTION, min(segment.endpoints))

        # Adding the segment in the hashtables based on the event key
        if event_creation.key in self.begin_points:
            # if the beginning point alreay exists
            self.begin_points[event_creation.key].append(segment)
        else:
            self.begin_points[event_creation.key] = [segment]
            #Adds the event in the events structure
            if not self.event_exists(event_creation):
                self.event_list.add(event_creation)

        if event_destruction.key in self.end_points:
            self.end_points[event_destruction.key].append(segment)
        else:
            self.end_points[event_destruction.key] = [segment]
            #Adds the event in the event structure
            if not self.event_exists(event_destruction):
                self.event_list.add(event_destruction)

    def isempty(self):
        """
        returns true is there are no more events in the structure
        """
        return len(self.event_list) == 0

    def finish_segments(self, event, living_segments, adjuster, solution):
        """
        finishes the segments on event
        """
        # if no segments are finishing on the current event
        if not event.key in self.end_points:
            return


        for segment in self.end_points[event.key]:

            #neighbours for the current segment
            [neighbour_left, neighbour_right] = list(neighbours(segment, living_segments))

            # removes the segment on the current event
            for index, seg in enumerate(living_segments):
                if seg == segment:
                    living_segments.pop(index)
                    break

            # Test the intersections if there is only two neighbours
            if not(neighbour_left and neighbour_right):
                continue

            inter_point = neighbour_left.intersection_with(neighbour_right)
            if not inter_point:
                continue

            inter_point = adjuster.hash_point(inter_point)

            if not intersection_is_correct(inter_point, neighbour_left, neighbour_right):
                continue

            # Adding the intersection to the solution
            solution.add(neighbour_left, inter_point)
            solution.add(neighbour_right, inter_point)

            # If no event exists for this intersection, the event is created
            if not inter_point in self.end_points and not inter_point in self.begin_points:
                self.add_intersection(inter_point)

            # Adds the segments to the end hashtable on intersection
            end_point = self.end_points[inter_point]
            if not neighbour_left in end_point:
                end_point.append(neighbour_left)
            if not neighbour_right in end_point:
                end_point.append(neighbour_right)

            # Adds the segment to the begin hashtable if it is not
            # on an endpoint of the segment
            begin_point = self.begin_points[inter_point]
            if not neighbour_left in begin_point and not inter_point in neighbour_left.endpoints:
                begin_point.append(neighbour_left)
            if not neighbour_right in begin_point and not inter_point in neighbour_right.endpoints:
                begin_point.append(neighbour_right)

    def begin_segments(self, event, living_segments, adjuster, solution):
        """
        begins the segments on event
        """
        # Check if segments are beginning from the current event
        if not event.key in self.begin_points:
            return

        for segment in self.begin_points[event.key]:
            #print('DEBUT', segment.index)
            # input()
            # Adds the segment to the living segments
            # Checks the intersection with the added segment
            if segment not in living_segments:
                living_segments.add(segment)

            self.check_intersection(event, segment,
                                     living_segments,
                                     adjuster, solution)


    def add_intersection(self, inter_point):
        """
        Adds the intersection point in the events.
        """
        not_exist = not inter_point in self.begin_points and not inter_point in self.end_points
        # Creates the entry in the hastable
        if not inter_point in self.begin_points:
            self.begin_points[inter_point] = []
        if not inter_point in self.end_points:
            self.end_points[inter_point] = []

        # If the intersection does not exists
        # Creates the intersection event and add it to the
        # hashtables of segments
        if not_exist:
            self.event_list.add(Event(INTERSECTION, inter_point))


    def check_intersection(self, event, segment, segments, adjuster, solution):
        """
        check intersection for one segment and the living segments
        """
        for inter_point, inter_segment in \
                                intersect_with(event, segment, segments, adjuster):

            #print("intersection: ", inter_point)
            #print([inter_segment, segment])
            # if point not in the past
            if not intersection_is_correct(inter_point, segment, inter_segment):
                continue
            # If the event does not exists
            # if inter_point not in self.end_points and inter_point not in self.begin_points:
            self.add_intersection(inter_point)
            # if inter_point in self.end_points and inter_point in self.end_points:
            #     self.begin_points[inter_point] = []

            # if the intersection point already exists and if the
            # current segment is involved => it is already in *_points
            # if segment not in self.end_points[inter_point]:
            #     # Adds the segment to the hashtable with the computed intersection
            #     #if inter_point in self.begin_points:
            #     self.end_points[inter_point].append(segment)
            #     # if not segment in self.begin_points[inter_point]:
            #     if not inter_point in segment.endpoints:
            #         self.begin_points[inter_point].append(segment)
            #
            # if inter_segment not in self.end_points[inter_point]:
            #     self.end_points[inter_point].append(inter_segment)
            #     # if not inter_segment in self.begin_points[inter_point]:
            #     if not inter_point in inter_segment.endpoints:
            #         self.begin_points[inter_point].append(inter_segment)


            for s in [inter_segment, segment]:
                # if s.index == 56:
                #     print('6 INTERSECTION ___________________________________________')
                #     print(inter_point)
                #     print('end:', [s.index for s in self.end_points[inter_point]])
                #     print('begin:', [s.index for s in self.begin_points[inter_point]])
                #     print(inter_point in s.endpoints)
                #     print(s.endpoints)
                #     input()

                if s not in self.end_points[inter_point]:
                    self.end_points[inter_point].append(s)
                    # if not s in self.begin_points[inter_point]:
                    if not inter_point in s.endpoints:
                        self.begin_points[inter_point].append(s)

            # Adding the solution
            solution.add(inter_segment, inter_point)
            solution.add(segment, inter_point)

def intersection_is_correct(point, seg1, seg2):
    """
    check if an intersection is correct
    """
    #if point not in the past
    if (point in seg1.endpoints and point in seg2.endpoints):
        return False
    return (point.coordinates[1] <= Segment.current_point.coordinates[1]) or \
           (point.coordinates[1] == Segment.current_point.coordinates[1] and \
            point.coordinates[0] <= Segment.current_point.coordinates[0])
    # if point.coordinates[1] <= Segment.current_point.coordinates[1]:
    #     if point in seg1.endpoints and point in seg2.endpoints:
    #         return False
    #     else:
    #         return True
    # return False

def intersect_with(event, segment, living_segments, adjuster):
    """
    computes the intersection with the closest segments from segment
    and iterates on the adjusted intersections with the segments involved
    """
    # Searching for the current segment in the living segments
    # and searching for its nearest neighbours
    for neighbour in neighbours(segment, living_segments):
        if neighbour is None:
            continue
        inter_point = segment.intersection_with(neighbour)
        # if there's an intersection
        if inter_point is not None:
            inter_point = adjuster.hash_point(inter_point)
            yield inter_point, neighbour

def neighbours(segment, segments):
    """
    yields the neighbour segments of segment in segments
    """
    segment_index = None
    droit, gauche = None, None
    # segment_index = segments.index(segment)
    for index, seg in enumerate(segments):
        if seg is segment:
            segment_index = index
    if segment_index is not None:
        if segment_index < len(segments)-1:
            droit = segments[segment_index + 1]
        if segment_index > 0:
            gauche = segments[segment_index - 1]
    return [gauche, droit]

def events_init_test():
    """
    test the init of a segment in the series of event
    """
    #print("\n------------Segment init test------------")
    events = Events([Segment([Point([1.0, 2.0]), Point([3.0, 4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([3.0, -4.0])]),
                     Segment([Point([-3.0, -4.0]), Point([2.0, 4.0])])])
    #print(events)
    #print("-----------------------------------------\n")

def intersection_test():
    """
    test the intersection on basic cases with one or two neighbours
    """
    #print("\n---------Intersection neighbour test---------")
    seg1 = Segment([Point([0, 0]), Point([2, 2])])
    seg2 = Segment([Point([1, 0]), Point([1, 2])])
    events = Events([seg1, seg2])
    #print("events:", events)

    Segment.current_point = Point([2.0, 2.0])
    living_segments = SortedList()
    living_segments.add(seg1)
    living_segments.add(seg2)

    # while not events.isempty():
    #     current_event = events.event_list.pop(0)
    #     #print("current event: ", current_event.key)
    #     if current_event.key in events.begin_points:
    #         for segment in events.begin_points[current_event.key]:
                #print("segment étudié :", segment)
                #print([p for p in intersect_with(current_event,
                                                #  segment,
                                                #  living_segments,
                                                #  CoordinatesHash())])

    #print("-----------------------------------------\n")

if __name__ == "__main__":
    """
    run the tests sequence
    """
    events_init_test()
    intersection_test()
