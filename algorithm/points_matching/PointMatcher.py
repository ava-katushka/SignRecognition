__author__ = 'ava-katushka'

class PointMatcher:

    #Eucludian distance
    @staticmethod
    def distance(p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(0.5)

    #Finds matching between 2 sets of points
    #Closest points from different sets match each other
    #Returns Set of Pairs of points, which match each other
    @staticmethod
    def compare_sets(set1, set2):
        if len(set1) == 0 or len(set2) == 0:
            return []
        result = []
        for p1 in set1:
            best = set2[0]
            best_distance = PointMatcher.distance(p1, best)
            for p2 in set2:
                dist = PointMatcher.distance(p1, p2)
                if dist < best_distance:
                    best_distance = dist
                    best = p2
            result.append([p1, best])
        return result


