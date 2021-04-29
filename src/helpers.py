import pandas as pd
import os 


def load_data(path):
    'Load each data set recursively'
    df = pd.read_csv(path)

    return df

def change_data_types(df):
    '''Change datatypes of features'''
    list_columns = df.columns.values.tolist()
    if 'price' in list_columns:
        df['price'] = df['price'].astype('float32')
        cat_vars = df.select_dtypes(['object']).columns
        df[cat_vars] = df[cat_vars].astype('category')
        # change the other numeric variables to float32
        num_vars = df.select_dtypes(['float64']).columns
        df[num_vars] = df[num_vars].astype('float32')
    else:
    # change objects to category variables
        cat_vars = df.select_dtypes(['object']).columns
        df[cat_vars] = df[cat_vars].astype('category')
    # change the other numeric variables to float32
        num_vars = df.select_dtypes(['float64', 'int64']).columns
        df[num_vars] = df[num_vars].astype('float32')

    return df
