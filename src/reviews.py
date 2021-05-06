import pandas as pd
import numpy as np
import os 
import spacy

from spacytextblob.spacytextblob import SpacyTextBlob

#python -m spacy download en_core_web_sm

# my little helpers
import src.helpers as helpers
#import Textprocessor as tp

reviews = helpers.read_df('data/reviews.csv', index_col='listing_id')
reviews = helpers.change_data_types(reviews)

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")
# pipeline Names
print(nlp.pipe_names)
#Stopwords
stpw = spacy.lang.en.stop_words.STOP_WORDS

doc = nlp(reviews.comments[0])
for token in doc:
    print(token)
print(doc._.assessments)