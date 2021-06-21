#!/usr/bin/env python3

import os 
import pandas as pd 
import json
import re
import glob

from clize import run 


def reviews(source, target):
    '''
    Function to read in the jsonl files of the processed reviews to get the necessary features in order to join 
    it with the different dataframes (other features like images and dfs) 
    '''
    #source = '/root/data/interim/reviews/jsonl'
    #target  = '/root/data/interim/reviews/csv'
    input_paths = [file for file in os.listdir(source) if re.match(r'reviews_processed[0-9]+\.jsonl$', file)]
    input_files = [open(os.path.join(source, input_path)) for input_path in input_paths]
    review_data = [[json.loads(review) for review in input_files[index]] for index in range(len(input_files))]

    listing_ids = [[review_data[j][index]['listing_id'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    comments = [[review_data[j][index]['comments'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    reviewer_id = [[review_data[j][index]['reviewer_id'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    review_id = [[review_data[j][index]['review_id'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    comment_length = [[review_data[j][index]['comment_length'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    lemmas = [[review_data[j][index]['lemmas'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    common_words = [[review_data[j][index]['common_words'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    assessments = [[review_data[j][index]['assessments'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    subjectivity = [[review_data[j][index]['subjectivity'] for index in range(len(review_data[j]))] for j in range(len(review_data))]
    polarity = [[review_data[j][index]['polarity'] for index in range(len(review_data[j]))] for j in range(len(review_data))]

    a = [{
        'listing_id': listing_ids[i], 'comments': comments[i], 'reviewer_id': reviewer_id[i], 'review_id': review_id[i] , 
        'comment_length': comment_length[i],'lemmas': lemmas[i],'common_words': common_words[i], 
        'assessments': assessments[i] , 'subjectivity': subjectivity[i], 'polarity': polarity[i]
        } for i in range(len(review_data))]
   
    review_dfs = [pd.DataFrame.from_dict(a[i], orient='index') for i in range(len(a))]
    review_dfs = [review_df.transpose() for review_df in review_dfs]
    review_dfs = [review_df.set_index('listing_id') for review_df in review_dfs]
    reviews = pd.concat(review_dfs)
    # erstmal nur 'comment_length und polarity'
    reviews = reviews[['polarity', 'comment_length']]
    
    reviews.to_csv(os.path.join(target + '/reviews.csv'))
    
    return

if __name__=='__main__':
    run(merge)
