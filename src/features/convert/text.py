#! /usr/bin/env python3
import os 
import requests
import pandas as pd 
import json
import sys
import csv
import langdetect
sys.path.append('.')
import src.features.preprocess.Textprocessor as Textprocessor
import src.features.preprocess.Processor as Processor
from time import sleep
from langdetect import detect

from clize import run 


def process_reviews(source,target):
    
    text_processor = Textprocessor()
    processor = Processor()

    with open(source, newline='') as csvfile:
        with open(target, 'w') as out_file:
            data =csv.DictReader(csvfile)
            lines = list(data) # adapt it to 0 so it will run through 
            for i in range(209127, len(lines)):
                row = lines[i]
            #for row in data:
                id_ = row['listing_id']
                reviewer_id = row['reviewer_id']
                review_id = row['review_id']
                text = row['comments']
                length = len(text)
                # clean
                text = text_processor.clean(text)
                text = text_processor.remove_URL(text)
                text = text_processor.convert_emojis_to_word(text)
                try:
                    # detect_language
                    language = detect(text)
                    if language != 'en':
                        try:
                        # translate 
                            text = text_processor.translate(text)
                        except requests.exceptions.ConnectionError as e:
                            print('Too Many Requests, let me sleep for 10 seconds...')
                            sleep(10)
                            continue

                except langdetect.lang_detect_exception.LangDetectException:
                    print('No features in text...')
                    continue
                # process 
                lemmas, common_words = text_processor.process(text)
                # get_sentiments
                assessments, subjectivity, polarity = text_processor.get_sentiments(text)
                # all texts as texts could play a crucial role
                if length >= 1:
                    json.dump(
                        {
                            'listing_id': id_,
                            'comments':  text,
                            'language': language,
                            'reviewer_id': reviewer_id,
                            'review_id': review_id,
                            'comment_length': length,
                            'lemmas': lemmas,
                            'common_words': common_words,
                            'assessments': assessments,
                            'subjectivity': subjectivity,
                            'polarity': polarity

                        }, out_file
                    )
                    out_file.write('\n')
                
    return
                

if __name__=='__main__':
    run(process_reviews)