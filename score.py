from data_loader import *

def score_facility(fac, distance, weights, mds_data, claim_data):
    '''
        Takes a facility and computes a score for the facility

        Inputs:
        (dict) fac which is the facility to compute the score of
        (dict) zip_dists which is a { zip_code: distance } mapping

        Returns:
        (float) representing the score
    '''
    fractional = {
        'mds': .1,
        'claim': .3
    }
    poor_performance_perct = 30.0
    poor_mult = 3.0

    base_value = weights['distance'] * distance
    rating = weights['overall_rating'] * int(fac['overall_rating'])
    mds_frac = fractional['mds'] * base_value
    claims_frac = fractional['claim'] * base_value

    mds_total = 0.0
    for mds in mds_data[fac['provnum']]:
        value = mds['MEASURE_SCORE_4QTR_AVG']
        weighting = weights[mds['MSR_CD']]
        if len(value) == 0:
            continue  # skip empty
        elif weighting < 0 and float(value) >= poor_performance_perct:
            mds_total += poor_mult * weighting * float(value)
        else:
            mds_total += weighting * float(value)
    mds_total /= 100.0  # normalize to fraction instead of percentage

    claim_total = 0.0
    for claim in claim_data[fac['provnum']]:
        value = claim['SCORE_ADJUSTED']
        weighting = weights[claim['MSR_CD']]
        if len(value) == 0:
            continue  # skip empty
        elif weighting < 0 and float(value) >= poor_performance_perct:
            claim_total += poor_mult * weighting * float(value)
        else:
            claim_total += weighting * float(value)
    claim_total /= 100.0  # normalize to fraction instead of percentage

    score = base_value
    score -= rating
    score -= (mds_total * mds_frac)
    score -= (claim_total * claims_frac)

    return score
    
def offset_score(facs, min_score):
    for f in facs:
        f['score'] = f['score'] - min_score + 1.0
