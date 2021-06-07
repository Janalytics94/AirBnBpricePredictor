#! /usr/bin/env python3
import os 
import pandas as pd 
import json
import sys
import csv
sys.path.append('.')
import src.features.preprocess.Textprocessor as Textprocessor


from clize import run 

def convert_reviews(source, target):
    text_processor = Textprocessor()

    reviews = pd.read_csv(source, index_col='listing_id', usecols=['listing_id','comments'])

    with open(source, newline='') as csvfile:
        with open(target, 'w') as out_file:
            data =csv.DictReader(csvfile)
            for row in data:
                json.dump(
                    {
                      row['listing_id']: row['comments']
                    }, out_file
                )
                out_file.write('\n')

    return 


#def convert_text(source, df_name, target):

 #   columns_of_interest = []


  #  return 

if __name__=='__main__':
    run(convert_reviews)