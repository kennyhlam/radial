from calculations import Point
from collections import defaultdict
import csv


def load_facilities(zips=None):
    '''
        Loads the relevant facility locations.

        Inputs:
        (array) zips of the facility locations to be loaded
                if zips is None, will return the facilities for all zip codes

        Returns:
        (list) of facilities as a (dict) mapping
    '''
    facilities = []

    with open('data/ProviderInfo_Download.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (zips is None) or (row['ZIP'] in zips):
                facilities.append(row)
    return facilities


def load_zips(zips=None):
    '''
        Loads the relevant zip codes as Point objects.

        Inputs:
        (array) zips of the zip codes to retrieve into Point objects
                if zips is None, will return all zip codes

        Returns:
        (dict) of { 'zip-code': <Point object> } mappings
    '''

    zip_idx, lat_idx, lng_idx = 0, 0, 0
    points = {}

    with open('data/zip_code_centroids.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            zip_code = row['zip_code']

            if (zips is None) or (zip_code in zips):
                p = Point(zip_code, float(row['lat']), float(row['lng']))
                points[zip_code] = p

    return points
