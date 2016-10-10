from math import sin, cos, asin, sqrt

EARTH_RADIUS_MILES = 3959

class Point:
    '''
        Wrapper class for zipcode centroids. Really just to make lat and lng
        explicit instead of having tuples and remembering which order things are in
    '''
    def __init__(self, lat, lng):
        '''
            Constructor function, lat and lng must be in radians
        '''
        self.lat = lat
        self.lng = lng

def distance(p1, p2):
    '''
            Inputs:
            (Point) p1, (Point) p2

            Returns:
            Distance between the points p1 and p2 as determined by the haversine formula
            https://en.wikipedia.org/wiki/Haversine_formula
    '''
    h = sin((p2.lat - p1.lat)/2.0)**2 + cos(p1.lat)*cos(p2.lat)*sin((p2.lng - p1.lng)/2.0)**2
    return 2 * EARTH_RADIUS_MILES * asin(sqrt(h))