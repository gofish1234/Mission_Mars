#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:23:30 2019

@author: chrismiller
"""
#import dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd

#initialize browser
def init_browser():
    executable_path = {'executable_path': '/Users/chrismiller/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#set up individual scrapes
def scrape_latest_news():
    latest_news ={}
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    Latest_news = soup.find('div', class_="content_title").text.strip()
    Latest_para = soup.find('div', class_="rollover_description_inner").text.strip()
    latest_news["title"] = Latest_news
    latest_news["paragraph"] = Latest_para
    return latest_news


def scrape_featured_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url ="https://www.jpl.nasa.gov"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find("article")
    f_img_url = base_url + article.a['data-fancybox-href']
    return f_img_url
    
def scrape_latest_tweet():
     url = "https://twitter.com/marswxreport?lang=en"
     response = requests.get(url)
     soup = BeautifulSoup(response.text, 'lxml')
     tweet = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
     return tweet   

def scrape_mars_facts():
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    return html_table

    
def scrape_mars_hemispheres():
   url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   response = requests.get(url)
   soup = BeautifulSoup(response.text, 'lxml')
   results = soup.find_all("div", class_="description")
   hemispheres = []
   for result in results:
       hemispheres.append(result.h3.text)

   executable_path = {'executable_path': '/Users/chrismiller/chromedriver'}
   browser = Browser('chrome', **executable_path, headless=False)
   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url)
  
   hemisphere_list = []
   for hemisphere in hemispheres:
       browser.click_link_by_partial_text(f'{hemisphere}')
       html = browser.html
       soup = BeautifulSoup(html, 'html.parser')
       image_link = soup.find('img', class_='wide-image')['src']
       image_url = 'https://astrogeology.usgs.gov' + image_link
       hemi_dict = {}
    
       hemi_dict["title"] = f'{hemisphere}'
       hemi_dict["img_url"] = image_url
       hemisphere_list.append(hemi_dict)

       browser.visit(url)
        
   browser.quit()
   return hemisphere_list 
    

#set up final scrape
def final_scrape():
    Mars = {} 
    Mars["Latest_news"] = scrape_latest_news()["title"]
    Mars["Latest_paragraph"] = scrape_latest_news()["paragraph"]
    Mars["Featured_Image"] = scrape_featured_image()
    Mars["Latest_Tweet"] = scrape_latest_tweet()
    Mars["Mars_Fact"] = scrape_mars_facts()
    Mars["Hemispheres"] = scrape_mars_hemispheres()
    
    return Mars

   