# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 13:59:37 2021

@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4
# pip install fake_useragent
# pip install selenium
# pip install chromedriver-binaryy

import pandas as pd
import requests
import json
import re
import time
import os
import csv
import random
import pickle
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree


from selenium import webdriver

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# %% 2. OBTENER LAS CATEGORIAS (mediante scrapping simple)
categories_url = "https://www.skillshare.com/browse"


# Options webdriver
option = webdriver.ChromeOptions()
# option.add_argument(" — incognito") # open incognito mode / not working?
# option.add_argument("user-agent=AcademicCrawler") #set our UserAgent name, in this case AcademicCrawler

# browser = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=option)
# driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=option)
driver = webdriver.Chrome(chrome_options=option, executable_path='./chromedriver/chromedriver')


# Get content from objective website
driver.get(categories_url)

# Aply delay
TimeOut = 2
driver.implicitly_wait(TimeOut);

# We trace the block with the categories listed
block_category_list= driver.find_elements(By.XPATH, '//*[@id="page-wrapper"]/div/div[1]/div/div/div/div[*]/a')
category_list = []
for category in block_category_list:
    category_list.append(category.get_attribute("data-ss-tag-slug"))

# Hemos obtenido una lista con los nombres de las categorías


# %% 3. inicializacion de las variables

nList = list(range(0, 2))
base_url = 'https://www.skillshare.com/browse?seeAll=1&tagSlug=%&sort=rating&time=default&length=all&enrollmentType=both&page='

links = list()



http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36", 
  }

# %% 3.1. OBTENEMOS LINK DE CADA CLASE DE CATEGORIA


for class_type in category_list:
    for num in nList:
        url = base_url.replace('%', str(class_type)) + str(num)
        
        
        driver.implicitly_wait(20)
        driver.get(url)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        print(driver.page_source)

      
              
        class_link_tags = soup.find_all('a', attrs={"class": "ss-card__thumbnail js-class-preview"})
        class_links = [class_link_tag.find('layout')['href'] for class_link_tag in class_link_tags]
        
        
        print(soup)
            
  
