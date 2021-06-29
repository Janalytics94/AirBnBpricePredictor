 #!/usr/bin/env python3
import datetime
import pandas as pd
import os 
import geopy
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer

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
    
    #TODO: Funktion überarbeiten
    def outlier_trunctuation(self, df, column, factor):
        
        IQR = df[column].quantile(0.75) - df[column].quantile(0.25) 
        # factor = 1.5
        upper = df[column].quantile(0.75) + factor*IQR
        lower = df[column].quantile(0.25) - factor*IQR
        df_new = df.copy()
        df_new[df[column] < lower] = lower
        df_new[df[column] > upper] = upper
            
        return df_new, IQR
    
    def price_log_transformation(self, price):

        log_price = np.log(price)

        return log_price

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
        values = {
            'bathrooms': 1, 'bedrooms': 1, 'beds': 1,
            'host_total_listings_count': 1, 'reviews_per_month': 0
        }
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
    
    def impute_review_scores(self,df):
        '''
        K Nearest Neigbhour for the review scores regarding cleanliness etc.
        '''
        imputer = KNNImputer(n_neighbors=5)
        scores_df = df[['review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 'review_scores_location', 'review_scores_value']]
        scores_df = pd.DataFrame(imputer.fit_transform(scores_df),columns = scores_df.columns, index=df.index)
        df = df.merge(scores_df, on='listing_id')

        return df

    def drop_features(self, df):
        '''
        drop neighbourhood as we already have neighbourhood_cleansed
        '''
        df = df.drop(['neighbourhood', 'picture_url', 'summary', 'space'], axis=1)

        return df
        
    def get_relevant_features(self, df):
        cols = df.columns.values.tolist()
        if 'price' in cols:
            df = df[[
                'price','accommodates', 'bathrooms', 'bedrooms','beds','guests_included',
                'host_identity_verified','host_has_profile_pic','host_is_superhost' ,
                'bed_type','room_type','host_response_rate', 'host_response_time', 
                'host_memship_in_years', 'host_total_listings_count' , 'reviews_per_month', 'dist', 'description_length',
                'review_scores_rating_y','review_scores_accuracy_y','review_scores_cleanliness_y', 'review_scores_checkin_y',              
                'review_scores_communication_y','review_scores_location_y','review_scores_value_y' 

                #'longitude', 'latitude'
                #'experience_offered' #'property_type'
            ]]
        else:
            df = df[[
                'accommodates', 'bathrooms', 'bedrooms','beds','guests_included',
                'host_identity_verified','host_has_profile_pic','host_is_superhost',
                'bed_type','room_type','host_response_rate', 'host_response_time', 
                'host_memship_in_years', 'host_total_listings_count', 'reviews_per_month','dist', 'description_length',
                'review_scores_rating_y','review_scores_accuracy_y','review_scores_cleanliness_y', 'review_scores_checkin_y',              
                'review_scores_communication_y','review_scores_location_y','review_scores_value_y'
                #'longitude', 'latitude'
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
    
    def feature_cross(self, df):
        ''' Prepare Data for Feature Cross,
        using 100x100 grid
        '''
        max_long = df.longitude.max()
        min_long = df.longitude.min()
        diff_long = max_long - min_long
        long_boundaries = []

        for i in np.arange(min_long, max_long, diff_long):
            long_boundaries.append(min_long+i*diff_long)

        max_lat = df.latitude.max()
        min_lat = df.latitude.min()
        diff_lat = max_lat-min_lat
        lat_boundaries = []

        for i in np.arange(min_lat, max_lat, diff_lat):
            lat_boundaries.append(min_lat+i*diff_lat)
        
        long_marked = tf.feature_column.bucketized_column(
            tf.feature_column.numeric_column('longitude'), boundaries=long_boundaries
        )
        lat_marked = tf.feature_column.bucketized_column(
            tf.feature_column.numeric_column('latitude'), boundaries=lat_boundaries
        )

        crossed_feature = tf.feature_column.crossed_column([long_marked, lat_marked], hash_bucket_size=100)
        feature_layer = tf.keras.layers.DenseFeatures(tf.feature_column.indicator_column(crossed_feature))

        return feature_layer

    def create_train_validation_frames(self, train, target, test):
        ''' 
        Create train and validation set to evaluate model performance of 
        our neural network 
        '''
        
        mn = MinMaxScaler()
    
        train, validate, y_train, y_validate = train_test_split(train,target, test_size=0.2, shuffle=True, random_state=0)
        x_train_scaled = pd.DataFrame(mn.fit_transform(train), columns = train.columns)
        x_validate_scaled = pd.DataFrame(mn.fit_transform(validate), columns = validate.columns)
        x_test_scaled = pd.DataFrame(mn.fit_transform(test), columns = test.columns)
        # Turn everything into a numpy array
        #train = np.asarray(train).astype(np.float32)
        # validate = np.asarray(validate).astype(np.float32)
        # y_train = np.asarray(y_train).astype(np.float32)
        #y_validate = np.asarray(y_validate).astype(np.float32)
        
        return train, validate, y_train, y_validate


    
    

        

        
        

   



        