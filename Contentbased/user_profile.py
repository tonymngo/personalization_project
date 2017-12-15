import pandas as pd
import numpy as np
import random
import Datapreprocessing
import product_profile

def recommendation(dt, dat):

    dict1 = {}
    for row in dt.itertuples():
        dict1.setdefault(row.reviewerID, [])
        if row.rating == 5 or row.rating == 4:
            dict1[row.reviewerID].append(row.productID)

    dat1 = dat
    dict2 = {}
    list2 = []
    for row in dt.itertuples():
        dict2.setdefault(row.reviewerID, [])
        for i in dict1[row.reviewerID]:
            r = product_profile.recommend(dat1, i, num=6)
            for j in r:
                list2.append(j[1])

            for h in random.sample(list2, 6):
                dict2[row.reviewerID].append(h)

    dict3 = {}
    for row in dt.itertuples():
        dict3.setdefault(row.reviewerID, [])

    for d in dict2.keys():
        if len(dict2[d]) >= 6:
            for i in random.sample((dict2[d]), 6):
                dict3[d].append(i)

    return dict3


if __name__ == '__main__':
    dt = pd.read_csv('data/sample_data.csv', index_col=0)
    dt1 = pd.read_csv('data/sample_data_meta.csv', index_col=0)

    dat = Datapreprocessing.processing(dt, dt1)

    reco = recommendation(dt, dat)
    print reco
