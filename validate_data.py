#!/usr/bin/env python

from data_loader import *
import re

facs = load_facilities()

exceptional_zips = set([])
exceptional_ratings = set([])
for f in facs:
    if re.match('^[0-9]{5}$', f['ZIP']) is None:
        exceptional_zips.add(f['ZIP'])
    if re.match('^[1-5]$', f['overall_rating']) is None:
        exceptional_ratings.add(f['overall_rating'])

print "Non-standard zips: {}".format(exceptional_zips)
print "Non-standard ratings: {}".format(exceptional_ratings)
