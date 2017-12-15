import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel



def model(dt,dt1):


    dict1={}
    for row in dt.itertuples():
        dict1.setdefault(row.reviewerID,[])
        if row.rating==5 or row.rating==4:
            dict1[row.reviewerID].append(row.productID)

    dat=pd.merge(dt,dt1,on=['productID'])

    dat=dat[['productID','title']]

    dat1=dat.drop_duplicates()

    dat1 = dat1.reset_index(drop=True)

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')

    tfidf_matrix = tf.fit_transform(dat1['title'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    for idx, row in dat1.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], dat1['productID'][i]) for i in similar_indices]

    # First item is the item itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
        results[row['productID']] = similar_items[1:]

    print('done!')


    def item(id):
        return dat1.loc[dat1['productID'] == id]['productID'].tolist()[0]


    final = {}


    def recommend(item_id, num):
    # print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    # print("-------")
        recs = results[item_id][:num]
        for rec in recs:
            final[item(rec[1])] = str(rec[0])

        result = [key for key in final]

        return result

    r=recommend(item_id='B00GLP9JI2', num=5)
    for i in r:
        print(i)

    dict2 = {}
    list2 = []
    for row in dt.itertuples():
        dict2.setdefault(row.reviewerID, [])
        for i in dict1[row.reviewerID]:
            r = recommend(i, num=10)
            for j in r:
                list2.append(j)

            for h in random.sample((list2), 6):
                dict2[row.reviewerID].append(h)

    dict3 = {}
    for row in dt.itertuples():
        dict3.setdefault(row.reviewerID, None)

    for d in dict2.keys():
        if len(dict2[d]) >= 6:
            dict3[d] = random.sample((dict2[d]), 6)

    return dict3


dt = pd.read_csv('data/sample_data.csv', index_col=0)
dt1 = pd.read_csv('data/sample_data_meta.csv', index_col=0)

print(model(dt,dt1))
