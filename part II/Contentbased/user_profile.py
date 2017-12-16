import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#def product_similarity(data):
#    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
#    tfidf_matrix = tf.fit_transform(data['title'])
#    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
#
#    results = {}
#    for idx, row in data.iterrows():
#        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
#        similar_items = [(cosine_similarities[idx][i], data['productID'][i]) for i in similar_indices]
#
#    # First item is the item itself, so remove it.
#    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
#        results[row['productID']] = similar_items[1:]
#
#    return results


def item(dat, id):
    return dat.loc[dat['productID'] == id]['productID'].tolist()[0]


def recommend_item(dat, sim_matrix, item_id, num):
    
    final = {}
    recs = sim_matrix[item_id][:num]
    for rec in recs:
        final[item(dat, rec[1])] = str(rec[0])

    result = [key for key in final]

    return result

def processing(sampledata, metadata):

    dat = pd.merge(sampledata, metadata, on=['productID'])
    dat = dat[['productID', 'title']]
    dat1 = dat.drop_duplicates()
    dat1 = dat1.reset_index(drop=True)

    return dat1

def recommendation(dt, dat):
    #Calculate product similarity
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(dat['title'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}
    for idx, row in dat.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], dat['productID'][i]) for i in similar_indices]

    # First item is the item itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
        results[row['productID']] = similar_items[1:]

    #Store reviewerID and productID as dictionary
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
            r = recommend_item(dat1, results, i, num=6)
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
    
dt = pd.read_csv('data/sample_data.csv', index_col=0)
dt1 = pd.read_csv('data/sample_data_meta.csv', index_col=0)

dat = processing(dt, dt1)

reco = recommendation(dt, dat)