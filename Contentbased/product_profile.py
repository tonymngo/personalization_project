import pandas as pd
import numpy as np
import random
import Datapreprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def product_similarity(data):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(data['title'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}
    for idx, row in data.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], data['productID'][i]) for i in similar_indices]

    # First item is the item itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
        results[row['productID']] = similar_items[1:]

    return results


def item(dat, id):
    return dat.loc[dat['productID'] == id]['productID'].tolist()[0]


def recommend(dat, item_id, num):
    results = product_similarity(dat)
    final = {}
    recs = results[item_id][:num]
    for rec in recs:
        final[item(dat, rec[1])] = str(rec[0])

    result = [key for key in final]

    return result


if __name__ == '__main__':
    dt = pd.read_csv('data/sample_data.csv', index_col=0)
    dt1 = pd.read_csv('data/sample_data_meta.csv', index_col=0)

    dat_processed = Datapreprocessing.processing(dt, dt1)

    print recommend(dat_processed, item_id='B0004MTMD0', num=6)
