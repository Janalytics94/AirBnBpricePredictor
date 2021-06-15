#! /usr/bin/env python3
import os 
import requests
import pandas as pd 
import json
import sys
import csv
sys.path.append('.')
import src.features.preprocess.Textprocessor as Textprocessor
from time import sleep



from clize import run 

def convert_reviews(source, target):
    
    text_processor = Textprocessor()
   
    with open(source, newline='') as csvfile:
        with open(target, 'w') as out_file:
            data =csv.DictReader(csvfile)
            lines = list(data) # adapt it to 0 so it will run through 
            for i in range(128889, len(lines)):
                row = lines[i]
            #for row in data:
                id_ = row['listing_id']
                try:
                    # translate 
                    text = text_processor.translate(row['comments'])
                except requests.exceptions.ConnectionError as e:
                    print('Too Many Requests, let me sleep for 10 seconds...')
                    sleep(10)
                    continue
                # convert emojis 
                text = text_processor.convert_emojis_to_word(text)
                # clean
                text = text_processor.clean(text)
                # process 
                lemmas, common_words = text_processor.process(text)
                # get_sentiments
                assessments, subjectivity, polarity = text_processor.get_sentiments(text)
                json.dump(
                    {
                      'listing_id': id_,
                      'lemmas': lemmas,
                      'common_words': common_words,
                      'assessments': assessments,
                      'subjectivity': subjectivity,
                      'polarity': polarity
                    }, out_file
                )
                out_file.write('\n')

    return 


#def convert_text(source, df_name, target):

 #   columns_of_interest = []


  #  return 

if __name__=='__main__':
    run(convert_reviews)