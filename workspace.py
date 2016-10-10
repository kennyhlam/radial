#!/usr/bin/env python

import argparse
import json
from math import sin, cos, asin, sqrt

parser = argparse.ArgumentParser(description='Command line search for the Nursing Home Compare for SNFs.')
parser.add_argument('zip_code', metavar='ZIP', type=str, help='Zip code to center search around.')
parser.add_argument('--radius', type=int, metavar='RADIUS', dest='search_radius',
                            default=10, help='Radius, in miles, to search around specified zip code. Default is 10 miles.')
parser.add_argument('--rating', type=int, metavar='RATING', dest='min_overall_rating',
                            default=1, help='Minimum acceptable rating for SNF in search, on a scale from 1-5. Default is 1.')

args = parser.parse_args()
print args

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