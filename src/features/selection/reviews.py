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
    
    #source = '/root/data/interim/reviews/jsonl/'
    #target  = '/root/data/interim/reviews/csv'
    review = [review for review in glob.glob(os.path.join(source, "*.jsonl"))]
    review_data = []
    for review in review:
        with open(review, "r") as stream:
            for line in stream:
                try:
                    review_data.append(json.loads(line))
                except json.decoder.JSONDecodeError:
                    pass


                
    listing_ids = [review_data[j]['listing_id'] for j in range(len(review_data))]
    comments = [review_data[j]['comments'] for j in range(len(review_data))]
    language = [review_data[j]['language'] for j in range(len(review_data))]
    reviewer_id = [review_data[j]['reviewer_id'] for j in range(len(review_data))]
    review_id = [review_data[j]['review_id'] for j in range(len(review_data))]
    comment_length = [review_data[j]['comment_length'] for j in range(len(review_data))]
    lemmas = [review_data[j]['lemmas'] for j in range(len(review_data))]
    common_words = [review_data[j]['common_words'] for j in range(len(review_data))]
    assessments = [review_data[j]['assessments'] for j in range(len(review_data))]
    subjectivity = [review_data[j]['subjectivity'] for j in range(len(review_data))]
    polarity = [review_data[j]['polarity'] for j in range(len(review_data))]

    a = {
        'listing_id': listing_ids, 'comments': comments, 'language': language, 'reviewer_id': reviewer_id, 'review_id': review_id , 
        'comment_length': comment_length,'lemmas': lemmas,'common_words': common_words, 
        'assessments': assessments, 'subjectivity': subjectivity, 'polarity': polarity
        } 
   
    review_df = pd.DataFrame.from_dict(a, orient='index')
    review_df = review_df.transpose()
    review_df = review_df.set_index('listing_id') 
    
    # erstmal nur 'comment_length und polarity'
    #reviews = reviews[['polarity', 'comment_length']]
    
    review_df.to_csv(os.path.join(target + '/reviews.csv'))
    
    return

if __name__=='__main__':
    run(reviews)
