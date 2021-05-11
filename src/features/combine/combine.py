#!/usr/bin/env python3
import os
import glob
import pandas as pd
from clize import run


def combine(source, target):
    '''combines all intermediate results to a dataframe and safes it into data/canonical.
    This directory contains final data which is fed to our model later'''
    source = 'data/interim/'
    path = os.path.join(source + '*.csv')
    dfs  = [pd.read_csv(file) for file in glob.glob(path)]




    return


if __name__ == '__main__':
    run(combine)