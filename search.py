#!/usr/bin/env python

import argparse
import json
from calculations import *
from data_loader import *

parser = argparse.ArgumentParser(
    description='Command line search for the Nursing Home Compare ' +
    'datasets for Skilled Nursing Facilities (SNFs).'
)

parser.add_argument('zip_code', metavar='ZIP', type=str,
                    help='Zip code to center search around.')
parser.add_argument('--radius', type=float, metavar='RADIUS',
                    dest='search_radius', default=10.0,
                    help='Radius, in miles, to search around specified ' +
                    'zip code. Default is 10 miles.')
parser.add_argument('--rating', type=int, metavar='RATING',
                    dest='min_overall_rating', default=1,
                    help='Minimum acceptable rating for SNF in search, ' +
                    'on a scale from 1-5. Default is 1.')

args = parser.parse_args()


def find_valid_zips(zip_code, radius):
    '''
        Finds all zip codes centered at zip_code within radius miles

        Inputs:
        (str) zip_code center of search
        (float) radius in miles of search area

        Returns:
        (dict) of {zip_code: (<Point object>, distance-to-center) } mappings
    '''
    all_zips = load_zips()
    center = all_zips[zip_code]

    valid_zips = {}
    for zip_code, point in all_zips.iteritems():
        d = distance(center, point)
        if d <= radius:
            # save the point and distance so no need to recalc later
            valid_zips[zip_code] = (point, d)
    return valid_zips


def find_valid_facilities(zip_codes, rating):
    '''
        Finds all facilities in zip_codes which have at least
        the specified rating

        Inputs:
        (array) zip_codes to search within for facilities
        (rating) minimum rating facilities must meet

        Returns:
        (array) of facility dict objects
    '''
    possible_facs = load_facilities(zip_codes)

    valid_facs = []
    for fac in possible_facs:
        if len(fac['overall_rating']) == 0:
            continue # skip facilities without a rating
        if int(fac['overall_rating']) >= rating:
            valid_facs.append(fac)
    return valid_facs


def remap_facilities(facs, zip_dists):
    '''
        Turns facility dict objects into the specified output format

        Inputs:
        (array) facs which are the facilities to re-map
        (dict) zip_dists specifying the distance of each zip from the
                search center

        Returns:
        (array) of facility dict objects
    '''
    def output_format(fac):
        zip_point = zip_dists[fac['ZIP']][0]
        zip_dist = zip_dists[fac['ZIP']][1]
        return {
            'name': fac['PROVNAME'],
            'address': fac['ADDRESS'],
            'city': fac['CITY'],
            'state': fac['STATE'],
            'zip_code': fac['ZIP'],
            'phone': fac['PHONE'],
            'overall_rating': int(fac['overall_rating']),
            'lat': zip_point.lat,
            'lng': zip_point.lng,
            'distance_miles': zip_dist
        }

    return map(output_format, facs)

relevant_zips = find_valid_zips(args.zip_code, args.search_radius)
valid_facs = find_valid_facilities(relevant_zips.keys(),
                                   args.min_overall_rating)
valid_facs = remap_facilities(valid_facs, relevant_zips)

# sort by distance ascending (normal), and overall_rating descending (reverse)
# (*-1) "reverses" good and bad ratings to sort correctly for overall_rating
valid_facs.sort(key=lambda x:
                (relevant_zips[x['zip_code']][1], -1*x['overall_rating'])
                )
print json.dumps(valid_facs, indent=4)
