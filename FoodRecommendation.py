#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 22:20:44 2023

@author: gopalakrishnan
"""

import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from csv import writer

from enum import Enum
 
class season(Enum):
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4

season_dict = {1: season.WINTER.name , 2:season.WINTER.name , 3: season.SPRING.name, 4: season.SPRING.name, 5: season.SPRING.name, 6: season.SPRING.name
              , 7: season.SUMMER.name, 8: season.SUMMER.name, 9: season.AUTUMN.name, 10: season.AUTUMN.name, 11: season.AUTUMN.name, 14: season.WINTER.name}
class FoodRecommendation:
    
    def __init__(self):
        (self.AllergyDataset, self.RecipeDataset) = self.read_File()
        self.Vectorize = TfidfVectorizer(lowercase = True, ngram_range = (1,1))
        self.Text_tfidf = self.Vectorize.fit_transform(self.RecipeDataset['soup'])
        self.Type_tfidf = self.Vectorize.transform(self.RecipeDataset['type'])
        self.Season_tfidf = self.Vectorize.transform(self.RecipeDataset['seasons'])
    
    def read_File(self):
         allergyDataset = pd.read_csv("Allergy.csv").dropna()
         allergyDataset = allergyDataset.iloc[::,1:] 
         allergyDataset['Food'] = allergyDataset['Food'].str.lower().str.replace('[^a-zA-Z]','', regex=True)
         recipeDataset = pd.read_csv("recipe_preprocessed.csv").dropna()
         recipeDataset['soup'] = recipeDataset.apply(lambda x: ''.join(x['cuisine'] + ' ' + x['type'] + ' ' + x['ingredients'] + ' ' + x['seasons']), axis=1)
         return (allergyDataset, recipeDataset)

    def filter_allergy(self, sorted_index, allergy):
        allery_food = self.AllergyDataset[self.AllergyDataset.Allergy.str.contains('Lactose')].Food.tolist()
        df_recom = pd.DataFrame(columns=self.RecipeDataset.columns)
        for index in sorted_index:
            ing = self.RecipeDataset.loc[index].ingredients.split(',')
            if(any( i in allery_food for i in ing) == False):
                df_recom.loc[len(df_recom)] = self.RecipeDataset.loc[index]
        return df_recom
    
    def computeScores(self, vector):
        final_scores = self.Text_tfidf*vector.T*0.2
        final_scores += self.Type_tfidf*vector.T*0.7
        final_scores += self.Season_tfidf*vector.T*0.1
        return final_scores

    def get_recommendation(self, query, allergy):
        currentMonth = datetime.now().month
        query.append(season_dict.get(currentMonth))
        vector = self.Vectorize.transform([' '.join(query)])
        scores = self.computeScores(vector)
        sorted_index = pd.Series(scores.toarray().T[0]).sort_values(ascending = False)[0:10].index
        return self.filter_allergy(sorted_index, allergy)

    def update_orderFile(order):
        with open('order.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(order)
            f_object.close()
    
    def update_orderPerformanceFile(orderid, ordered_dish, recommened_dish):
        performance = [orderid]
        countofRecommendedAndOrdered = len([recommened_dish.index(i) for i in ordered_dish])
        countDishOrdered = len(ordered_dish)
        countDishRecommended = len(recommened_dish)
        countofRecommendedAndNotOrdered = len(recommened_dish) - countofRecommendedAndOrdered
        countofNotRecommendedAndOrdered = countDishOrdered - countofRecommendedAndOrdered
        
        performance += [countDishOrdered, countDishRecommended, countofRecommendedAndOrdered, countofRecommendedAndNotOrdered, countofNotRecommendedAndOrdered]
        
        with open('v1_Order_Performance.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(performance)
            f_object.close()
            
    def order_food(self, order):
        ordered_dish = order[0]
        recommened_dish = order[1]
        orderid = datetime.now().strftime("%d%m%y%H%M%S")
        order_time = datetime.now().strftime("%d/%m/%y %H%:M:%S")
        self.update_orderFile([orderid, order_time, ordered_dish, recommened_dish])
        self.update_orderPerformanceFile(orderid, ordered_dish, recommened_dish)
        return orderid
    
    def order_rating(self, orderRating):
        with open('v1_order_rating.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(orderRating)
            f_object.close()
        
