#!/usr/bin/env python3

import os 
import pandas as pd 
import json
import re
import glob


from clize import run 


def merge(source, target):

    '''Merges all available Data into one single Dataframe for Training '''

    #source = '/root/data/interim'
    #target = '/root/data/canonical'
    reviews = pd.read_csv('/root/data/interim/reviews/csv/reviews.csv', index_col='listing_id')
    # drop those who only have one character
    reviews = reviews[reviews.comment_length>=2]
    mean_comment_length = reviews.groupby(reviews.index)['comment_length'].mean().to_frame()
    mean_polarity = reviews.groupby(reviews.index)['polarity'].mean().to_frame()
    review_count = reviews.groupby(reviews.index)['review_id'].count().to_frame(name='review_count')
    df1 = mean_comment_length.merge(mean_polarity, on='listing_id')
    df2 = df1.merge(review_count, on='listing_id')
    df_names = ['train', 'test']
    for df_name in df_names:
        
        df = pd.read_csv(os.path.join(source + '/' + df_name + '/'+ df_name + '.csv'), index_col='listing_id')
        amenities_df = pd.read_csv(os.path.join(source + '/' + df_name + '/'+ 'amenities.csv'), index_col='listing_id')
        df = df.merge(amenities_df, on='listing_id')
        input_images = open(os.path.join(source + '/'+ df_name + '/' + 'images.jsonl'))
        image_data = [json.loads(input_line) for input_line in input_images]
        listing_ids = [image_data[index]['listing_id'] for index in range(len(image_data))]
        brightness_values = [image_data[index]['Brightness'] for index in range(len(image_data))]
        blues = [image_data[index]['BGR'][0] for index in range(len(image_data))]
        greens = [image_data[index]['BGR'][1] for index in range(len(image_data))]
        reds = [image_data[index]['BGR'][2] for index in range(len(image_data))] 

        a = {'listing_id': listing_ids, 'Brightness': brightness_values, 'Blue_Values': blues, 'Green_Values': greens, 'Red_Values': reds}
        images = pd.DataFrame.from_dict(a, orient='index')
        images = images.transpose()
        images = images.set_index('listing_id')
        images = images.astype('float32')

        merged_df = df.merge(images, on='listing_id', how='left').fillna(0)
        merged_df = merged_df.merge(df2, on='listing_id', how='left').fillna(0)
        numerics = merged_df.select_dtypes(['float64', 'int64']).columns
        merged_df[numerics] = merged_df[numerics].astype('float32')
        merged_df.to_csv(os.path.join(target + '/' + df_name + '/' + df_name + '.csv'))
    
    return

if __name__=='__main__':
    run(merge)

