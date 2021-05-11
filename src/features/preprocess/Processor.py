 #!/usr/bin/env python3
import datetime
import pandas as pd
import os 

class Processor():
    ''' Methods to clean and develop numeric and categorical features in dataframe'''

    def change_data_types(self,df):
        '''Change datatypes of features'''
        mapping = {'t': True, 'f':False}
        list_columns = df.columns.values.tolist()
        if 'price' in list_columns:
            df['price'] = df['price'].astype('float32')
        if 'host_id' in list_columns:
            df['host_id'] = df['host_id'].astype('int32') 
        if 'accommodates' in list_columns:
            df['accommodates'] = df['accommodates'].astype('int32') 
        if 'guests_included' in list_columns:
            df['guests_included'] = df['guests_included'].astype('int32')
        if 'review_id' in list_columns:
            df['review_id'] = df['review_id'].astype('int32')
        if 'reviewer_id' in list_columns:
            df['reviewer_id'] = df['reviewer_id'].astype('int32')
        if 'host_is_superhost' in list_columns:
            df['host_is_superhost'] = df['host_is_superhost'].map(mapping)
            df['host_is_superhost'] = df['host_is_superhost'].astype('bool')
        if 'host_has_profile_pic' in list_columns:
            df['host_has_profile_pic'] = df['host_has_profile_pic'].map(mapping)#
            df['host_has_profile_pic'] = df['host_has_profile_pic'].astype('bool')
        if 'host_identity_verified' in list_columns:
            df['host_identity_verified']= df['host_identity_verified'].map(mapping)
            df['host_identity_verified']= df['host_identity_verified'].astype('bool')
        if 'host_since' in list_columns:
            df['host_since'] = df['host_since'].astype('datetime64')          
        cat_vars = df.select_dtypes(['object']).columns
        df[cat_vars] = df[cat_vars].astype('category')
        # change the other numeric variables to float32
        floats = df.select_dtypes('float64').columns
        df[floats] = df[floats].astype('float32')

        return df

    def split_df(self,df):
        ''' splits df into supgroups to make the analysis a little easier.
        Information about the Airbnb itself will be one df, information about the review will be one df 
        and information about the host will be another df'''
        
        host = df[['host_id', 'host_since', 'host_response_time', 'host_response_rate',
        'host_is_superhost', 'host_total_listings_count',
        'host_has_profile_pic', 'host_identity_verified']]
        
        airbnb = df[['name', 'summary', 'space', 'description', 'experiences_offered',
        'neighborhood_overview', 'transit', 'house_rules', 'picture_url',
        'neighbourhood','neighbourhood_cleansed', 'zipcode', 'latitude', 'longitude',
        'property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms',
        'beds', 'bed_type', 'amenities', 'price', 'guests_included']]
        
        
        reviews_scores = df[['review_scores_rating', 'review_scores_accuracy',
        'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location',
        'review_scores_value', 'cancellation_policy', 'reviews_per_month' ]] 

        return host, airbnb, reviews_scores
        

    def membership(self,df):
        ''' caluclates Membership of hosts in years '''
        clean = df[df.host_since.isnull()!=True]
        clean['host_since_year'] = clean['host_since'].apply(lambda x: round(x.year,0))
        clean['host_memship_in_years'] = datetime.date.today().year - clean.host_since_year
        
        return clean

   



        