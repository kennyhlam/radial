#!/usr/bin/env python

import argparse
import json
from calculations import *

parser = argparse.ArgumentParser(description='''Command line search for the Nursing Home Compare datasets 
for Skilled Nursing Facilities (SNFs).''')

parser.add_argument('zip_code', metavar='ZIP', type=str, 
    help='Zip code to center search around.')
parser.add_argument('--radius', type=int, metavar='RADIUS', dest='search_radius', default=10, 
    help='Radius, in miles, to search around specified zip code. Default is 10 miles.')
parser.add_argument('--rating', type=int, metavar='RATING', dest='min_overall_rating',default=1, 
    help='Minimum acceptable rating for SNF in search, on a scale from 1-5. Default is 1.')

args = parser.parse_args()
print args

