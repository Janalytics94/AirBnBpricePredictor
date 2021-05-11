#!/usr/bin/env python3
import os
import glob
import pandas as pd
from clize import run


def combine(source, target):
    '''combines all intermediate results to a dataframe and safes it into data/canonical.
    This directory contains final data which is fed to our model later'''
    path = os.path.join(source + '*.csv')
    dfs  = [pd.read_csv(file, index_col='listing_id') for file in glob.glob(path)]
    dfs[0]['dist']
    # Additional host_has_profile_pic, host_identity_verified, host_is_superhost
    train_processed = dfs[1][['description_length', 'host_memship_in_years','accommodates','guests_included','beds', 'bathrooms', 'bedrooms','review_scores_cleanliness', 'review_scores_location', 'price']].merge( dfs[0]['dist'], right_on='listing_id', left_on='listing_id')
    train_processed = train_processed[train_processed.description_length.isna()!=True]
    train_processed.to_csv(target)

    return


if __name__ == '__main__':
    run(combine)