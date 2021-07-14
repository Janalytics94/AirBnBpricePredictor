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

def text(source, target):
    '''
    Function to read in the jsonl files of the processed text data to get the necessary features in order to join 
    it with the different dataframes (other features like images and dfs) 
    '''

    df_names = ['train', 'test']
    for df_name in df_names:
        with open(os.path.join(source, df_name, df_name + ".jsonl"), "r") as stream:
    
            text = [json.loads(line) for line in stream]
            listing_ids = [text[index]['listing_id'] for index in range(len(text))]        
            name = [text[index]['name'] for index in range(len(text))] 
            description = [text[index]['description'] for index in range(len(text))] 
            transit = [text[index]['transit'] for index in range(len(text))] 
            house_rules = [text[index]['house_rules'] for index in range(len(text))] 
            neighborhood_overview = [text[index]['neighborhood_overview'] for index in range(len(text))] 
            lemmas_name = [text[index]['lemmas_name'] for index in range(len(text))] 
            common_words_name = [text[index]['common_words_name'] for index in range(len(text))] 
            lemmas_description = [text[index]['lemmas_description'] for index in range(len(text))] 
            common_words_description = [text[index]['common_words_description'] for index in range(len(text))] 
            lemmas_transit = [text[index]['lemmas_transit'] for index in range(len(text))] 
            common_words_transit = [text[index]['common_words_transit'] for index in range(len(text))] 
            lemmas_house_rules = [text[index]['lemmas_house_rules'] for index in range(len(text))] 
            common_words_house_rules = [text[index]['common_words_house_rules'] for index in range(len(text))] 
            common_words_neighborhood_overview = [text[index]['common_words_neighborhood_overview'] for index in range(len(text))] 
            lemmas_neighborhood_overview = [text[index]['lemmas_neighborhood_overview'] for index in range(len(text))] 
            
            
            a = {'listing_id': listing_ids, 'name': name,
                 'description': description, 'transit': transit, 
                 'house_rules': house_rules, 'neighborhood_overview': neighborhood_overview,
                 'lemmas_name': lemmas_name, 'common_words_name': common_words_name,
                 'lemmas_description': lemmas_description, 'common_words_description': common_words_description,
                 'lemmas_transit': lemmas_transit, 'common_words_transit': common_words_transit,
                 'lemmas_house_rules': lemmas_house_rules, 'common_words_house_rules': common_words_house_rules,
                 'common_words_neighborhood_overview': common_words_neighborhood_overview, 'lemmas_neighborhood_overview': lemmas_neighborhood_overview
                 }
            text_df = pd.DataFrame.from_dict(a, orient='index')
            text_df = text_df.T
            text_df = text_df.set_index('listing_id')
            text_df.to_csv(os.path.join(target, df_name, 'texts.csv'))
        
        return

if __name__=='__main__':
    run(text)
