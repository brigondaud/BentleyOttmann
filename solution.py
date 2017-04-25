"""
Solution module for the Bentley Ottmann algorithm
"""
class Solution:
    """
    solution: associates to all the segment their intersection
    """
    def __init__(self, segments):
        """
        initializes a hastable that associates to all the segments an empty
        set of intersection point
        """
        self.hashtable = dict()
        for segment in segments:
            self.hashtable[segment] = set()

    def add(self, segment, point):
        """
        adds the intersection point to a segment in the solution
        """
        if segment not in self.hashtable:
            print("Segment not in the solution")
        else:
            self.hashtable[segment].add(point)

    def segments(self):
        """
        iterates on all the segments in the solution
        """
        for segment in self.hashtable:
            yield segment

    def points(self, segment):
        """
        iterates on all the intersection points in the solution for the given
        segment
        """
        for point in self.hashtable[segment]:
            yield point

    def intersection_points(self):
        """
        iterates on all the intersections point once
        """
        #TODO
        pass
