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
 # Creating enum for the seasons
class season(Enum):
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4

# creating dictinoary for month and seasons
season_dict = {1: season.WINTER.name , 2:season.WINTER.name , 3: season.SPRING.name, 4: season.SPRING.name, 5: season.SPRING.name, 6: season.SPRING.name
              , 7: season.SUMMER.name, 8: season.SUMMER.name, 9: season.AUTUMN.name, 10: season.AUTUMN.name, 11: season.AUTUMN.name, 14: season.WINTER.name}
              
class FoodRecommendation:
  
    # Initlizing the food recommendation and using TF-IDF to find the word weightage score
    def __init__(self):
        (self.AllergyDataset, self.RecipeDataset) = self.read_File()
        self.Vectorize = TfidfVectorizer(lowercase = True, ngram_range = (1,1))
        self.Text_tfidf = self.Vectorize.fit_transform(self.RecipeDataset['soup'])
        self.Type_tfidf = self.Vectorize.transform(self.RecipeDataset['type'])
        self.Season_tfidf = self.Vectorize.transform(self.RecipeDataset['seasons'])
        self.Mood_tfidf = self.Vectorize.transform(self.RecipeDataset['taste'])

    # Function read_File that reads the allergy and recipe dataset
    def read_File(self):
         allergyDataset = pd.read_csv("Allergy.csv").dropna()
         allergyDataset = allergyDataset.iloc[::,1:] 
         allergyDataset['Food'] = allergyDataset['Food'].str.lower().str.replace('[^a-zA-Z]','', regex=True)
         recipeDataset = pd.read_csv("recipe_preprocessed.csv").dropna()
        # Creating the soup column as a combination of all the features
         recipeDataset['soup'] = recipeDataset.apply(lambda x: ''.join(x['cuisine'] + ' ' + x['type'] + ' ' + x['ingredients'] + ' ' + x['seasons'] + ' ' + x[]), axis=1)
         return (allergyDataset, recipeDataset)

    # Function filter_allergy that takes the recommended dishes and list of allery as input and filters the dishes that doesnot contain allergy ingredients
    def filter_allergy(self, sorted_index, allergy):
        allery_food = self.AllergyDataset[self.AllergyDataset.apply(lambda x : x['Allergy'] in allergy, axis=1)].Food.tolist()
        df_recom = pd.DataFrame(columns=self.RecipeDataset.columns)
        for index in sorted_index:
            ing = self.RecipeDataset.loc[index].ingredients.split(',')
            if(any( i in allery_food for i in ing) == False):
                df_recom.loc[len(df_recom)] = self.RecipeDataset.loc[index]
        return df_recom
    
    # Function computeScores takes 1 parameter vector which of Tf-Idf vectorize for identifying similar dishes by computing the smiliarity scores
    def computeScores(self, vector):
        final_scores = self.Text_tfidf*vector.T*0.2
        final_scores += self.Type_tfidf*vector.T*0.6
        final_scores += self.Season_tfidf*vector.T*0.1
        final_scores += self.Mood_tfidf*vector.T*0.1
        return final_scores

    # Function get_recommendation takes 2 inputs
    # query is the list of cuisines, taste preference that the customer selected
    # allergy is the list of allergy food
    # This function also finds the current season that we are in and transfroms the query + season and finds the similarty scores and returns the non allery dishes
    def get_recommendation(self, query, allergy):
        currentMonth = datetime.now().month
        query.append(season_dict.get(currentMonth))
        vector = self.Vectorize.transform([' '.join(query)])
        scores = self.computeScores(vector)
        sorted_index = pd.Series(scores.toarray().T[0]).sort_values(ascending = False)[0:10].index
        return self.filter_allergy(sorted_index, allergy)

    # update_orderFile function takes the ordered details as input and saves in a csv file
    def update_orderFile(order):
        with open('order.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(order)
            f_object.close()
    
    # update_orderPerformanceFile function takes the ordered details as input and finds the different metrics needed for computing the accuray, precision, recall and F1 score and saves in the csv file per order
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
    
    # order_food function takes the order details as input and add a order id and saves in the csv file
    def order_food(self, order):
        ordered_dish = order[0]
        recommened_dish = order[1]
        orderid = datetime.now().strftime("%d%m%y%H%M%S")
        order_time = datetime.now().strftime("%d/%m/%y %H%:M:%S")
        self.update_orderFile([orderid, order_time, ordered_dish, recommened_dish])
        self.update_orderPerformanceFile(orderid, ordered_dish, recommened_dish)
        return orderid
    
    # function order_rating saving the rating of each order
    def order_rating(self, orderRating):
        with open('v1_order_rating.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(orderRating)
            f_object.close()
