#!/usr/bin/env python3

# NLP in general
import spacy
from collections import Counter
from spacytextblob.spacytextblob import SpacyTextBlob

# to handle different langauges in reviews
from google_trans_new import google_translator
# emojies
import pickle
import re

class TextProcessor():
    ''' Class to initilaize text processing '''

    def get_data(self,df):
        '''remove missing values / nan in texts'''

        columns = df.columns.tolist()
        if 'description ' in columns:
            clean = df[pd.isna(train.description)==False]
            text = clean.description.values.tolist()
        if 'comment' in columns:
            clean = df[pd.isna(reviews.comment)==False]
            text = clean.comment.values.tolist()

        return text

    def description_length(self, df):
        ''' Calculates Description Length of each Airbnb'''

        df['description_length'] = df.description.apply(lambda x: len(x))

        return df

    def translate(self, text):
        ''' Translates reviews in different languages to english'''

        translator = google_translator()
        trans_text = translator.translate(text)

        return trans_text      

    def convert_emojis_to_word(self, text):
        ''' uses Emoji_Dict.p as bases to convert existing emojis to words to prevent loss of information'''

        with open('/root/data/external/Emoji_Dict.p', 'rb') as fp:
            Emoji_Dict = pickle.load(fp)
        Emoji_Dict = {v: k for k, v in Emoji_Dict.items()}
        for emot in Emoji_Dict:
            text = re.sub(r'('+emot+')', "_".join(Emoji_Dict[emot].replace(",","").replace(":","").split()), text)
        
        return text    

    def process_amenities(self, df):

        ''' process amenities in dataset'''
        amenities = list(df.amenities)
        amenities = " ".join(amenities)
        amenities = amenities.replace('}', '')
        amenities =amenities.replace('{', '')
        amenities = amenities.replace('"', '')
        set_amenities = [x.strip() for x in amenities.split(',')]
        set_amenities = set(set_amenities)

        return set_amenities


    def clean(self, text):
        ''' Removes \n and \r from data set turn everything to lower case'''

        text = text.replace("\r","")
        text = text.replace("\n","")
        text = text.replace("\\","")
        text = text.strip('{')
        text = text.strip('}')
        text = text.lower()

        return text     

    def process(self, text):
        ''' Basic NLP on text data (remove stopwords, lemmatizations, tokens) might need some additional work'''
        
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text) 
        tokens = [token for token in doc]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        # remove puntuations
        filtered = [token for token in filtered if not token.is_punct]
        # remove white spaces 
        filtered = [token for token in filtered if not token.is_space ]
        # lemmatize and turn it to lowercase
        lemmas = [token.lemma_.strip().lower() for token in filtered]
        word_freq = Counter(lemmas)
        # 5 commonly occurring words with their frequencies
        common_words = word_freq.most_common(5)

        return lemmas, common_words
    
    def get_sentiments(self,review):
        ''' Sentimentsanalyse'''

        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("spacytextblob")
        #Stopwords
        stpw = spacy.lang.en.stop_words.STOP_WORDS
        doc = nlp(review)
        tokens = [token for token in doc]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        # remove puntuations
        filtered = [token for token in filtered if not token.is_punct]
        # remove white spaces 
        filtered = [token for token in filtered if not token.is_space ]

        assessments = doc._.assessments 
        subjectivity = doc._.subjectivity
        polarity = doc._.polarity 

        return assessments, subjectivity, polarity

       
