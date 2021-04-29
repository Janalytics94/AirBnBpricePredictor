import pandas as pd
import os 


def read_df(path: str = os.path.join(os.getcwd(), '/data/<My_data>.csv'), **kwargs) -> pd.DataFrame:
    """
    Method importing a DataFrame from a specified path
    :param path: A str pointing to the respective csv file
    :param kwargs: Additional kwargs for pandas' read_csv method
    :return: None
    """
    try:
        df = pd.read_csv(path, **kwargs)
        return df
    except FileNotFoundError:
        print('Data file not found. Path was ' + path)


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
