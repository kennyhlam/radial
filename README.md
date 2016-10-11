# Notes
All development was done on Ubuntu 16.04.1 (xenial), but as long as the valid version of `python` is within your `PATH`, it should run on OSX as well.

The basic implementation of the system skips facilities without an `overall_rating` field, this is equivalent to assuming that such facilities have a rating of 0. It would be inappropriate to try and interpolate in this value based on data found in any other row(s); a reasonable method would be to try to estimate the value based on other fields which could be available such as `staff_rating`, `quality_rating`, `survey_rating`, etc. However, without clear documentation on how this value was achieved, I have simply chosen to ignore records without a valid `overall_rating`.

Calculations for distance stem for the [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula). As mentioned in the article, antipodal points can lead to floating point errors and invalid `asin`. Since the data is all based in America, this case is ignored and it is assumed all calculations lead to valid trigonometry.

With regard to efficiency, the code is generally pretty efficient. The big items are that the `zip_code`/`search_radius` filtered facilities are looped over a few times: once to score every entry & prepare it for output, again to offset the scores to start at 1.0, and at least once more to generate the keys for sorting (sorting then takes `O(n log n)`). Some of these steps could be combined, specifically the scoring and key geneartion, but practically you should just always call `list.sort` since the likelihood of errors when sorting manually is very much higher. A different choice of score function could save one iteration of those facilities.

In terms of productization and scaling, the slowness of the script simply has to do with needing the quality measures from the `QualityMsrClaims_Download.csv` and `QualityMsrMDS_Download.csv`, wich both need to be loaded and parsed to find the data for the relevant facilities. To reduce the issues, it would be much simpler to just implement a client which just calls an API to return the results instead of doing client-side computation. A properly set up infrastructure would simply cache this data in the already-processed form onto a cache server like memcached or Redis for fast and easy access.

# Score
The optional portion of implementing a score was done in `score.py` (lower scores are better, scores start at 1.0 and go upwards). Primarily, it is assumed that the distance plays a major role in the score; all values weight the score as a proportion of the distance. The `overall_rating`, combined with MDS measures and claims measures (all weighted), give a more holistic measure of quality. The difference between the distance and this quality metric then represents the score (values are then offset so the minimum is 1.0). Because a higher number indicates a better quality, lower scores then correspond to better quality, and hence are generally "better" for the same distance.

The MDS measures, fall into one of three general buckets: clearly the success/fault of the facility, likely correlated to the treatment at the facility, or unclear relation to treatment at the facility. These buckets have weights of 1.0, 0.5, and 0.1, respectively--positive weights indicate positive quality, while negative weights indicate negative quality. The measures can be found in `mds_weights`, where each row is `measure code | measurement | weighting`.

The claims measures fall into one of two buckets: correlated to success of the facility, or correlated to shortcomings of the facililty. They have weights of 2.0 and -1.0, respectively. These weights are much heftier than the MDS measures since they are much more definitive in their correlations. These measures can similarly be found in `claim_weights`.

The score also includes an added penalty for quality: if any negatively weighted measure is exceedingly high, then there's an added penalty of 3x the weight. This is because a measure which is high implies a more likely correlation of that measure and the treatment at the facility. This is also an artifact of my personal perception of quality: I believe people are more likely to be harsh towards negative outcomes that stem out of facility treatment than praiseful of positive outcomes.

However, the formulation has major shortcomings and should be used as a guesstimate more than any authority. The weights were chosen completely arbitarily, without a good metric to measure them by. Additionally, measures which aren't available are completely skipped, meaning that a facility with all-positive measurements or all-negative measurements can strongly bias the quality metric (and therefore the score). The scores also have no absolute meaning, but are a relative measure within the set of results for any single query.

# Implementation
- python (2.7.12)

# Installation
Required is the data provided from the flat CSV files at https://data.medicare.gov/data/nursing-home-compare to be unzipped into the `data` directory. The directory should look like this:

```
├── claim_weights
├── data
│   ├── DataMedicareGov_MetadataAllTabs_v11.xls
│   ├── Deficiencies_Download.csv
│   ├── DMG_CSV_DOWNLOAD20160901.zip
│   ├── Ownership_Download.csv
│   ├── Penalties_Download.csv
│   ├── ProviderInfo_Download.csv
│   ├── QualityMsrClaims_Download.csv
│   ├── QualityMsrMDS_Download.csv
│   ├── StateAverages_Download.csv
│   ├── SurveySummary_Download.csv
│   └── zip_code_centroids.csv
├── data_loader.py
├── distance.py
├── mds_weights
├── README.md
├── requirements.txt
├── score.py
├── search.py
├── validate_data.py
└── workspace.py
```

The stock version of python 2.7.12 will be sufficient to run the scripts, the `pep8` specification in the `requirements.txt` file is simply for style checking.

# Usage
```
(radial) vagrant:radial-analytics/ (master*) $ python search.py -h
usage: search.py [-h] [--radius RADIUS] [--rating RATING] ZIP

Command line search for the Nursing Home Compare datasets for Skilled Nursing
Facilities (SNFs).

positional arguments:
  ZIP              Zip code to center search around.

optional arguments:
  -h, --help       show this help message and exit
  --radius RADIUS  Radius, in miles, to search around specified zip code.
                   Default is 10 miles.
  --rating RATING  Minimum acceptable rating for SNF in search, on a scale
                   from 1-5. Default is 1.

(radial) vagrant:radial-analytics/ (master*) $ python search.py 02139 --radius 2
[
    {
        "distance_miles": 1.3173706145256399, 
        "phone": "6177764420", 
        "address": "186 HIGHLAND AVENUE", 
        "lat": 42.3814093, 
        "lng": -71.0967141, 
        "city": "SOMERVILLE", 
        "name": "JEANNE JUGAN RESIDENCE", 
        "state": "MA", 
        "score": 1.532891745736934, 
        "zip_code": "02143", 
        "overall_rating": 5
    }, 
    {
        "distance_miles": 1.9897282954575293, 
        "phone": "6174970600", 
        "address": "640 CONCORD AVENUE", 
        "lat": 42.3796372, 
        "lng": -71.1351523, 
        "city": "CAMBRIDGE", 
        "name": "NEVILLE CENTER AT FRESH POND FOR NURSING & REHAB", 
        "state": "MA", 
        "score": 1.0, 
        "zip_code": "02138", 
        "overall_rating": 5
    }, 
    {
        "distance_miles": 1.9897282954575293, 
        "phone": "6178682200", 
        "address": "799 CONCORD AVENUE", 
        "lat": 42.3796372, 
        "lng": -71.1351523, 
        "city": "CAMBRIDGE", 
        "name": "SANCTA MARIA NURSING FACILITY", 
        "state": "MA", 
        "score": 1.6296591512562897, 
        "zip_code": "02138", 
        "overall_rating": 4
    }, 
    {
        "distance_miles": 1.9897282954575293, 
        "phone": "6178644267", 
        "address": "8 DANA STREET", 
        "lat": 42.3796372, 
        "lng": -71.1351523, 
        "city": "CAMBRIDGE", 
        "name": "CAMBRIDGE REHABILITATION & NURSING CENTER", 
        "state": "MA", 
        "score": 1.9972876310725942, 
        "zip_code": "02138", 
        "overall_rating": 2
    }
]
```