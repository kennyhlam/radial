from math import sin, cos, asin, sqrt, pi

EARTH_RADIUS_MILES = 3959.0


class Point:
    '''
        Wrapper class for zipcode centroids. Really just to make lat and lng
        explicit instead of having tuples and remembering the order of the
        components
    '''
    def __init__(self, zip_code, lat, lng):
        '''
            Constructor function, lat and lng must be in radians
        '''
        self.zip_code = zip_code
        self.lat = lat
        self.lng = lng


def distance(p1, p2):
    '''
        Provides the distance between two point objects on earth's surface,
        in miles, as determined by the haversine formula.
        https://en.wikipedia.org/wiki/Haversine_formula

        Inputs:
        (Point) p1, (Point) p2

        Returns:
        (float) representing the distance between the two points
    '''
    p2_lat = p2.lat * pi / 180.0
    p2_lng = p2.lng * pi / 180.0
    p1_lat = p1.lat * pi / 180.0
    p1_lng = p1.lng * pi / 180.0

    h = sin((p2_lat - p1_lat)/2.0)**2 + \
        cos(p1_lat)*cos(p2_lat)*sin((p2_lng - p1_lng)/2.0)**2

    return 2.0 * EARTH_RADIUS_MILES * asin(sqrt(h))
