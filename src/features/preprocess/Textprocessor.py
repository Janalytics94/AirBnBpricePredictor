#!/usr/bin/env python3
# URLS
import pandas as pd
import requests
import numpy as np
from time import sleep

# NLP in general
import spacy
from collections import Counter
from spacytextblob.spacytextblob import SpacyTextBlob

# to handle different langauges in reviews
from google_trans_new import google_translator
# emojies
import pickle
import re


class Textprocessor():
    ''' Class to initilaize text processing '''

    def get_data(self,df, column):
        '''remove missing values / nan in texts'''
        if column == 'description':
            clean = df[pd.isna(df.column)==False]
            #text = clean.description.values.tolist()
        if column == 'comments':
            clean = df[pd.isna(df.column)==False]
           #text = clean.comment.values.tolist()

        return clean

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

    def clean_amenities(self, df):

        # remove missiing values
        df.loc[df.amenities == '{}', 'amenities'] = ""
        df['amenities'] = df['amenities'].map(lambda amns: "|".join([amn.replace('{', '').replace('}', '').replace('"', '') for amn in amns.split(",")]))
        amenities = np.unique(np.concatenate(df['amenities'].map(lambda amns: amns.split("|")).values))
        amenities_matrix = np.array([df['amenities'].map(lambda amns: amn in amns).values for amn in amenities])
        amenities_df = pd.DataFrame(data=amenities_matrix.T, columns=amenities, index=df.index)
        # drop unnecessary columns
        amenities_df = amenities_df.drop(columns=['', 'translation missing: en.hosting_amenity_49', 'translation missing: en.hosting_amenity_50' ])

        # Recoding the original amneities 
        amenitie_dict = {
            # Acessible Room
            'Flat path to guest entrance': 'Accessible Room',
            'Accessible-height bed': 'Accessible Room',
            'Accessible-height toilet': 'Accessible Room',
            'Bathtub with bath chair': 'Accessible Room',
            'Fixed grab bars for shower': 'Accessible Room', 
            'Fixed grab bars for toilet': 'Accessible Room',
            'Handheld shower head': 'Accessible Room',
            'Wheelchair accessible' : 'Accessible Room',
            'Wide clearance to shower': 'Accessible Room', 
            'Wide doorway to guest bathroom': 'Accessible Room',
            'Wide entrance': 'Accessible Room',
            'Wide entrance for guests': 'Accessible Room', 
            'Wide entryway': 'Accessible Room',
            'Wide hallways': 'Accessible Room',
            'Ground floor access': 'Accessible Room',
            'Disabled parking spot': 'Accessible Room',
            'Shower chair': 'Accessible Room',
            'Step-free shower': 'Accessible Room',
            'Single level home': 'Accessible Room',
            'Extra space around bed':'Accessible Room',

            # Pet Friendly
            'Cat(s)': 'Pet Friendly',
            'Pets allowed': 'Pet Friendly',
            'Pets live on this property': 'Pet Friendly',
            'Dog(s)': 'Pet Friendly',
            'Other pet(s)': 'Pet Friendly',

            # Security
            'Doorman': 'Security',
            'Keypad': 'Security',
            'Smart lock': 'Security',
            'Buzzer/wireless intercom': 'Security',
            'Well-lit path to entrance': 'Security',
            'Safety card': 'Security',
            'No stairs or steps to enter': 'Security',
            'Fire extinguisher': 'Security',
            'Carbon monoxide detector': 'Security',
            'Smoke detector': 'Security',


            # Family Friendly
            'Children’s dinnerware': 'Family Friendly',
            'Children’s books and toys': 'Family Friendly',
            'Babysitter recommendations': 'Family Friendly',
            'Baby bath': 'Family Friendly',
            'Baby monitor': 'Family Friendly',
            'Changing table': 'Family Friendly',
            'Crib': 'Family Friendly',
            'Family/kid friendly': 'Family Friendly',
            'Fireplace guards': 'Family Friendly',
            'Stair gates': 'Family Friendly',
            'Window guards': 'Family Friendly',
            'High chair': 'Family Friendly',
            'Pack ’n Play/travel crib': 'Family Friendly',
            'Outlet covers': 'Family Friendly',
            'Table corner guards':'Family Friendly',


            # Essentials
            'Bath towel': 'Essentials',
            'Hair dryer': 'Essentials',
            'Body soap': 'Essentials',
            'Shampoo': 'Essentials',
            'Bed linens': 'Essentials',
            'Toilet paper': 'Essentials',
            ' toilet': 'Toilet',
            'Bathroom essentials': 'Essentials',
            'Trash can': 'Essentials',
            'Shower gel':'Essentials',
            'Hangers': 'Essentials',
            'Standing valet': 'Essentials',
            'Iron': 'Essentials',
            'Ironing Board': 'Essentials',
            'Toilet': 'Essentials',


            # Comfortable Sleep
            'Extra pillows and blankets' : 'Comfortable Sleep',
            'Firm matress' : 'Comfortable Sleep',
            'Firm mattress' : 'Comfortable Sleep',
            'Room-darkening shades' : 'Comfortable Sleep',
            'Memory foam mattress': 'Comfortable Sleep',
            'Pillow-top mattress': 'Comfortable Sleep',
            'Bedroom comforts': 'Comfortable Sleep',
            'Murphy bed': 'Comfortable Sleep',
            'Day bed':  'Comfortable Sleep',
           

            # Comfortable Sleep
            'Extra pillows and blankets' : 'Comfortable Sleep',
            'Firm matress' : 'Comfortable Sleep',
            'Firm mattress' : 'Comfortable Sleep',
            'Room-darkening shades' : 'Comfortable Sleep',
           

            # Hot Water
            'Hot water': 'Hot Water', 
            'Hot water kettle': 'Hot Water',

            # WIFI
            'Pocket wifi': 'WIFI',
            'Internet': 'WIFI',
            'Ethernet connection' : 'WIFI',
            'Wifi' : 'WIFI',

            # 24-Hour-Check-In 
            'Self check-in': '24-hour check-in ',
            '24-hour check-in': '24-hour check-in',
            'Luggage dropoff allowed': '24-hour check-in',
            'Lockbox': '24-hour check-in',
        
           

            # Parking paid or free
            'Free parking on premises' : 'Free parking',
            'Free parking on street' : 'Free parking',
            'Paid parking off premises' : 'Paid parking',

            # Privacy
            'Private bathroom' : 'Privacy', 
            'Private entrance' : 'Privacy',
            'Private living room' : 'Privacy',
            'Lock on bedroom door' : 'Privacy',


            # Climate Control
            'Ceiling fan': 'Air Condition',
            'Air conditioning': 'Air Condition',
            'Air purifier': 'Air Condition',
            'Central air conditioning': 'Air Condition',

            # Cooking Essentials
            'Cooking basics' : 'Cooking Allowed', 
            'Dishes and silverware' : 'Cooking Allowed', 
            'Dishwasher' : 'Cooking Allowed',
            'Microwave' : 'Cooking Allowed', 
            'Oven' : 'Cooking Allowed',
            'BBQ grill' : 'Cooking Allowed',
            'Stove' : 'Cooking Allowed', 
            'Kitchen' : 'Cooking Allowed',
            'Bread maker': 'Cooking Allowed',
            'Refrigerator': 'Cooking Allowed', 
            'Baking sheet':'Cooking Allowed',
            'Convection oven': 'Cooking Allowed',
            'Full kitchen': 'Cooking Allowed',
            'Double oven': 'Cooking Allowed',
            'Freezer': 'Cooking Allowed',
            'Kitchenette':'Cooking Allowed',
            'Steam oven': 'Cooking Allowed',
            'Gas oven':'Cooking Allowed',

       
            'Breakfast table': 'Breakfast',
                
            # TV
            'Cable TV' : 'TV', 
            'Smart TV': 'TV',
   


            # Heating

            'Heated floors': 'Heating',
            'Heated towel rack': 'Heating',
            'Heat lamps' : 'Heating',


            # Elevator,
            'Elevator in building' : 'Elevator', 
            
            # Near Water
            'Lake access' : 'Near Water',
            'Beachfront': 'Near Water',
            'Beach essentials': 'Near Water',
            'Waterfront': 'Near Water',
            'Beach view': 'Near Water',

            'Mobile hoist': 'Mobile host',
            # Luxury
            'Tennis court': 'Luxury',
            'Rain shower': 'Luxury',
            'Pool': 'Luxury',
            'Mudroom': 'Luxury',
            'Indoor fireplace': 'Luxury',
            'Hot tub': 'Luxury',
            'Fire pit': 'Luxury',
            'Wine cooler': 'Luxury',
            'Shared hot tub': 'Luxury',
            'Shared pool':  'Luxury',
            'Private pool': 'Luxury',
            'Stand alone steam shower': 'Luxury',
            'Walk-in shower' : 'Luxury',
            'Sound system': 'Luxury',
            'Game console': 'Luxury',
            'Private hot tub': 'Luxury',
            'Soaking tub': 'Luxury',
            'Bathtub': 'Luxury',
            'Jetted tub': 'Luxury',
            'Pool cover':'Luxury',
            'Alfresco bathtub': 'Luxury',
            'Touchless faucets': 'Luxury',
            'En suite bathroom': 'Luxury',
            'Building staff': 'Luxury',
            "Chef's kitchen": 'Luxury',
            'Bidet': 'Luxury',

            # Outdoor
            'Outdoor kitchen': 'Outdoor',
            'Outdoor parking': 'Outdoor',
            'Outdoor seating': 'Outdoor',
            'Barbecue utensils': 'Outdoor',




            # Gym
            'Exercise equipment': 'Gym',
            'Shared gym': 'Gym',

            # Garden
            'Garden or backyard': 'Garden',

            # Work Space
            'Printer': 'Work Space',
            'Laptop friendly workspace': 'Work Space',
            'High-resolution computer monitor': 'Work Space',
            'Fax machine': 'Work Space',
            'Coffee maker': 'Work Space',
            'Espresso machine': 'Work Space',


            # Cinema Feeling
            'Netflix': 'Cinema Feeling',
            'HBO GO': 'Cinema Feeling',
            'DVD player':'Cinema Feeling',
            'Projector and screen': 'Cinema Feeling',

            # Suitable for events
            'Dining area': 'Suitable for events',
            'Dining table': 'Suitable for events',
            'Formal dining area': 'Suitable for events',
            'Warming drawer': 'Suitable for events',
            
            
            'Washer / Dryer' :'Washer'




                






        }
        amenities_df = amenities_df.rename(columns=amenitie_dict)
        
        


        return  amenities_df


    def clean(self, text):
        ''' 
        Removes unnessary stuff from text like numbers, punctuation, etc. from data set turn everything to lower case
        '''

        text = text.replace("\r","")
        text = text.replace("\n","")
        text = text.replace("\\","")
        text = text.replace("/", "")
        text = text.replace("/", "")
        text = re.sub('[?@#$\&+!*"-]', '', text)
        text = re.sub(r'[0-9]', '', text)
        text = re.sub('\s+',' ', text)
        text = text.strip('/')
        text = text.strip('{')
        text = text.strip('}')
        text = text.strip('(')
        text = text.strip(')')
        text = text.lower()

        return text   

    def remove_URL(self, text):
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

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

       
