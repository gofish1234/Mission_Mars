#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:26:12 2019

@author: chrismiller
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdb")

@app.route("/")
def home():
    Mars = mongo.db.collection.find_one()
    return render_template("index.html", Mars=Mars)


@app.route("/scrape")
def scraper():
    New_data = scrape_mars.final_scrape()
    mongo.db.collection.drop
    mongo.db.collection.update({}, New_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

