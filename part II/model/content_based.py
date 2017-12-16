#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:14:44 2017

@author: tungngo
"""
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentBasedModel:
    def product_similarity(df_meta):
        df_it = df_meta[['productID','title']]
        df_it = df_it.reset_index()
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(df_it['title'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        results = {}
        for idx, row in df_it.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], df_it['productID'][i]) for i in similar_indices]
        
            # First item is the item itself, so remove it.
            # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
            results[row['productID']] = similar_items[1:]
            
        return results
    
    def content_prediction(results, df_rating, n=6):
        #Acquire top similar product from each product in results
        topk = defaultdict(list)
        sim_items_dict = defaultdict(list)
        for key_item, i_s in results.items():
            topk[key_item] = i_s[:n]
        for key_item, i_s in topk.items():
            for score, item in i_s:
                sim_items_dict[key_item].append(item)
                
        #Turn dataframe into dictionary, only taking into account high rating    
        df_records = df_rating.loc[df_rating['rating']>=0]
#        df_records = df_records[['reviewerID','productID']].to_dict('record')
#        df_dict = defaultdict(list)
#        for row in df_records:
#            df_dict[row['reviewerID']].append(row['productID'])
       
        user_item = []
        user_item_sim = defaultdict(list)
        for row in df_records.itertuples():
            user_item.append((row.reviewerID,row.productID))
        for (user,item) in user_item:
            user_item_sim[(user,item)].append(sim_items_dict[item])
        
        #Construct dataframe for each user-item-similar item
        user_item_sim_df = []
        for (user,item),sim_items in user_item_sim.items(): 
            for sim_item in sim_items[0]:
                user_item_sim_df.append([user,item,sim_item])
        user_item_sim_df = pd.DataFrame(user_item_sim_df,columns=['reviewerID','productID','similar_product'])
        
        #Return top recommendation per user
        recommendation_df = user_item_sim_df.pivot_table('productID',index=['reviewerID','similar_product'],aggfunc='count').reset_index().to_dict('record')
        recommendation_dict = defaultdict(list)
        for row in recommendation_df:
            recommendation_dict[row['reviewerID']].append((row['similar_product'],row['productID']))
        top_k_dict = defaultdict(list)
        for user, item_frequency in recommendation_dict.items():
            item_frequency.sort(key=lambda x: x[1], reverse=True)
            top_k_dict[user] = item_frequency[:n]
        top_k_nofreq = defaultdict(list)
        for user, item_frequency in top_k_dict.items():
            for item, frequency in item_frequency:
                top_k_nofreq[user].append(item)
        return top_k_nofreq