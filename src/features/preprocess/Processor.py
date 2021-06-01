 #!/usr/bin/env python3
import datetime
import pandas as pd
import os 
import geopy
import numpy as np

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
        clean['host_memship_in_years'] = clean['host_memship_in_years'].astype('int')
        ## fill NaNs with mean
        mean_membership = clean['host_memship_in_years'].mean()
        df['host_since_year'] = df['host_since'].apply(lambda x: round(x.year,0))
        df['host_memship_in_years'] = datetime.date.today().year - df.host_since_year
        df['host_memship_in_years'] = df['host_memship_in_years'].fillna(mean_membership)
        df = df.drop(['host_since_year', 'host_since'], axis=1)

        return df

    def host_response_rate_to_probabilities(self,df):  
        ''' strip % from column, 
        turn string to numeric features and 
        change them to probabilities , E.G How possible is it that the host answers ?
        '''
        df['host_response_rate'] = df['host_response_rate'].apply(lambda x: str(x))
        df['host_response_rate'] = df['host_response_rate'].apply(lambda x: x.strip('%'))
        df['host_response_rate'] = df['host_response_rate'].apply(lambda x: float(x))
        df['host_response_rate'] = df['host_response_rate'].apply(lambda x: x/100)
        # host does not answer. 
        df['host_response_rate'] = df['host_response_rate'].fillna(0) 
        df['host_response_rate'] = df['host_response_rate'].astype('int')

        return df

    def effect_coding_host_response_time(self, df):
        ''' Effect Coding for the time a host needs to answer 
        within an hour --> 1 
        within a few hours --> 1
        NaN --> not at all e.g -1
        within a day ---> 0
        a few days or more --> 0
        '''
        df['host_response_time'] = df['host_response_time'].apply(lambda x: str(x))
        df = df.replace({'host_response_time': {'within an hour': 1, 'within a few hours': 1,'within a day': 0, 'a few days or more':0}})
        df['host_response_time'] = df['host_response_time'].fillna(-1) 
        df['host_response_time'] = df['host_response_time'].astype('int32')

        return df


    def get_missing_zipcodes(self, df, latitude, longitude):
        ''' fill up the missing values in zipcodes'''
        geolocator = geopy.Nominatim(user_agent='http')
        location = geolocator.reverse("{},{}".format(df[latitude], df[longitude]))

        return location.raw['address']

    def NaNs(self, df):
        ''' methods to deal with the missing values in our data set '''
        values = {'bathrooms': 1, 'bedrooms': 1, 'beds': 1}
        df = df.fillna(value=values)
        # get df where zipcodes are missing
        missing_zipcodes = df[df.zipcode.isnull()==True][['longitude', 'latitude']]
        indecies = missing_zipcodes.index.values.tolist()
        # get zipcodes using function get_missing_zipcodes
        zipcodes = missing_zipcodes.apply(Processor().get_missing_zipcodes, axis =1, latitude='latitude', longitude='longitude').values.tolist()
        zipcode = []
        for index in range(len(zipcodes)):
            for key in zipcodes[index]:
                try:
                    zipcode.append(zipcodes[index]['postcode'])
                except KeyError as e:
                    continue
        zipcodes = list(set(zipcode))
        dict_ = dict(zip(indecies,zipcodes))
        df['zipcode'] = df.replace(dict_)

        return df

    def get_relevant_features(self, df):
        cols = df.columns.values.tolist()
        if 'price' in cols:
            df = df[[
                'price','accommodates', 'bathrooms', 'bedrooms','beds','guests_included',
                'host_identity_verified','host_has_profile_pic','host_is_superhost' ,'bed_type','room_type',
                'host_response_rate', 'host_response_time', 'host_memship_in_years'
                #'experience_offered' #'property_type'
            ]]
        else:
            df = df[[
                'accommodates', 'bathrooms', 'bedrooms','beds','guests_included',
                'host_identity_verified','host_has_profile_pic','host_is_superhost','bed_type','room_type',
                'host_response_rate', 'host_response_time', 'host_memship_in_years'
                #'experience_offered' #'property_type'
                ]]
        return df
    
    def hot_encode(self,df):
        ''' Hot encode the following features:
            * bed_type
            * room_type
            * property_type
        '''
        dummies = pd.get_dummies(df[['bed_type', 'room_type']]) #'property_type'
        df = df.drop(['bed_type', 'room_type'], axis=1) #'property_type'

        X = pd.concat([dummies, df], axis=1)  

        return X  

    
    

        

        
        

   



        