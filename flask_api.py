#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 22:44:59 2023

@author: gopalakrishnan
"""

from flask import Flask, request
import FoodRecommendation
app = Flask(__name__)
foodRecommendation = FoodRecommendation.FoodRecommendation()

# Creating helath check method
@app.route('/', methods=['GET'])
def getstatus():
    return 'ok'

# route to get list of all the dishes
@app.route('/dish', methods=['GET'])
def get_dish():
    return foodRecommendation.RecipeDataset[['name','cuisine']].to_dict()

# route to get list of all the allergies
@app.route('/allergy', methods=['GET'])
def get_Allergy():
    return foodRecommendation.AllergyDataset[['Type','Group','Food','Allergy']].to_dict()

# route to get food recommendation
@app.route('/recommedation', methods=['POST'])
def food_recommendation():
    return foodRecommendation.get_recommendation(request.args.get('query'), request.args.get('allergy'))

# route to order the food
@app.route('/order', methods=['POST'])
def order_food():
    return foodRecommendation.order_food(request.args.get('ordered_dishes'))#(request.args.get('ordered_dishes'), request.args.get('recommended_dishes'))

if __name__ == '__main__':
    app.run()
