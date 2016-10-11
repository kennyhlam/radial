from distance import Point
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


def load_mds_weights():
    '''
        Loads the weighting for MDS fields

        Returns:
        (dict) of { MDS-field: float } mappings
    '''
    weights = {}
    with open('mds_weights') as f:
        for row in f:
            if row == '\n':
                # empty line breaks
                continue
            code, msr, w = row.split('|')
            weights[code.strip()] = float(w)
    return weights


def load_claim_weights():
    '''
        Loads the weighting for claim fields

        Returns:
        (dict) of { claim-field: float } mappings
    '''
    weights = {}
    with open('claim_weights') as f:
        for row in f:
            if row == '\n':
                # empty line breaks
                continue
            code, msr, w = row.split('|')
            weights[code.strip()] = float(w)
    return weights


def load_mds():
    '''
        Loads the MDS data

        Returns:
        (dict) of { 'provider number' : [MDS data] } mappings
    '''
    mds = defaultdict(list)
    with open('data/QualityMsrMDS_Download.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mds[row['PROVNUM']].append(row)
    return dict(mds)


def load_claims():
    '''
        Loads the claim data

        Returns:
        (dict) of { 'provider number' : [claim data] } mappings
    '''
    claims = defaultdict(list)
    with open('data/QualityMsrClaims_Download.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            claims[row['PROVNUM']].append(row)
    return dict(claims)
