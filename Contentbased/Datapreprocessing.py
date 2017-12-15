import pandas as pd
import numpy as np
import random

def processing(sampledata, metadata):


    dat = pd.merge(sampledata, metadata, on=['productID'])
    dat = dat[['productID', 'title']]
    dat1 = dat.drop_duplicates()
    dat1 = dat1.reset_index(drop=True)


    return dat1

if __name__ == '__main__':

    dt = pd.read_csv('data/sample_data.csv', index_col=0)
    dt1 = pd.read_csv('data/sample_data_meta.csv', index_col=0)
    print processing(dt,dt1)


