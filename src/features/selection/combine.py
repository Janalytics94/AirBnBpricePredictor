#!/usr/bin/env python3
import os
import glob
import pandas as pd
from clize import run

# PRICE NOT IN TEST! Take care of it!

def combine(source, target):
    '''combines all intermediate results to a dataframe and safes it into data/canonical.
    This directory contains final data which is fed to our model later'''
    path = os.path.join(source + '*.csv')
    dfs  = [pd.read_csv(file, index_col='listing_id') for file in glob.glob(path)]
    dfs[0]['dist']
    # Additional host_has_profile_pic, host_identity_verified, host_is_superhost
    # 'review_scores_cleanliness', 'review_scores_location'
    processed = pd.concat([dfs[1][['description_length', 'host_memship_in_years','accommodates','guests_included','beds', 'bathrooms', 'bedrooms']],dfs[0]['dist']], axis=1)
    processed = processed[processed.isna()!=True]
    processed.to_csv(target)

    return


if __name__ == '__main__':
    run(combine)