#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:48:21 2017

Build a hybrid model

"""
import pandas as pd
import numpy as np
from collections import defaultdict

class HybridModel:
    """
    Inputs: data frame of user-item rating pair
    Output: ranking of recommended items
    """
    def divide_data(df,threshold):
        # Divide users into 2 groups: few vs many ratings
        rating_count = df.pivot_table('rating',index=['reviewerID'],dropna=False,aggfunc='count')

        sparse_group = rating_count.loc[rating_count['rating'] < threshold]
        sparse_group.reset_index(inplace = True)
        sparse_df = df.loc[df['reviewerID'].isin(sparse_group['reviewerID'])]

        dense_group = rating_count.loc[rating_count['rating'] >= threshold]
        dense_group.reset_index(inplace = True)
        dense_df = df.loc[df['reviewerID'].isin(dense_group['reviewerID'])]

        return sparse_df, dense_df
    
    def recommendation_mixer(prediction1, prediction2, prediction3 = None, n = 6):
        """
        Inputs: predictions from sub-models
        Outputs: final list of recommended products
        """
        predictionF = defaultdict(list)
        prediction_list = []
        prediction_list.append(prediction1)
        prediction_list.append(prediction2)
        if prediction3 is not None:
            prediction_list.append(prediction3)
        for user in prediction1:
            i = 0
            j = 0
            k = 0
            p = 0
            while len(predictionF[user]) < n:
                if p == 0:
                    if prediction_list[p][user][i] not in predictionF[user]:
                        predictionF[user].append(prediction_list[p][user][i])
                    i += 1
                    p = 1 
                elif p == 1:
                    if prediction_list[p][user][j] not in predictionF[user]:
                        predictionF[user].append(prediction_list[p][user][j])
                    j += 1
                    if prediction3 == None:
                        p = 0
                    else: 
                        p = 2
                elif p == 2:
                    if prediction_list[p][user][k] not in predictionF[user]:
                        predictionF[user].append(prediction_list[p][user][k])
                    k += 1
                    p = 0

        return predictionF
    
    def combine_prediction(sparse_prediction,dense_prediction):
        """
        Combine prediction of 2 cases: sparse and dense
        """
        final_prediction = {**sparse_prediction,**dense_prediction}
        return final_prediction