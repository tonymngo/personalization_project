#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:00:32 2017

@author: tungngo
"""
from collections import defaultdict

class evaluation:
    """
    Some ratios to measure performance of recommendation models
    """
    def recall_at_topk(prediction,holdout):
        """
        For each user, check if the prediction contains any of products in the holdout set. If yes, we count
        the prediction as a success, and a failure otherwise. Recall at top-k is measured as percentage of
        users with sucessful recommendation out of total number of users. This measurement is based on the 
        same idea as in this paper: https://arxiv.org/pdf/1703.02344.pdf
        """
        #Convert holdout dataframe to dictionary
        holdout_records = holdout[['reviewerID','productID']].to_dict('records')
        holdout_dict = defaultdict(list)
        for row in holdout_records:
            holdout_dict[row['reviewerID']].append(row['productID'])
        
        #Calculate recall at top k
        success_count = 0
        check = 0
        for user, items in prediction.items():
            for i in items:
                if i in holdout_dict[user]:
                    check = 1
            if check == 1:
                success_count += 1
                check = 0
        return float(success_count)/float(len(prediction))
    
    def coverage_ratio(prediction,dataset):
        """
        Coverage ratio is measured as number of products recommended over total number of products
        """
        recommended_product = []
        for user, items in prediction.items():
            recommended_product.extend(items)
        return float(len(set(recommended_product)))/float(len(set(dataset['productID'])))