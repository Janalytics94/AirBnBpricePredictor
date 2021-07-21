import numpy as np

class Evaluator():
    ''' Methods to evaluate the existing Models '''

    # MAPE
    def mean_absolute_percentage_error(self, y_true, y_pred): 
        '''
        Calculate Mean Absolute Percentage Error
        '''
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    

    # SMAPE
    def symmetric_mean_absolute_percentage_error(self, y_true, y_pred): 
        '''
        Calculates Symmetric Absolute Percentage Error
        '''

        y_true, y_pred = np.array(y_true), np.array(y_pred)
        
        return 100/len(y_true) * np.sum(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))