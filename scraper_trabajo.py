# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 13:59:37 2021

@author: Usuario
"""

# %% 1. Import libraries

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

from selenium import webdriver

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# %% 2. OBTENER LAS CATEGORIAS (mediante scrapping simple)
categories_url = "https://www.skillshare.com/browse"


# Options webdriver
option = webdriver.ChromeOptions()
# not working? # option.add_argument(" — incognito") # open incognito mode
option.add_argument("user-agent=AcademicCrawler") #set our UserAgent name, in this case AcademicCrawler

browser = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=option)

# Get content from objective website
browser.get(categories_url)

# Aply delay
TimeOut = 2
browser.implicitly_wait(TimeOut);

# We trace the block with the categories listed
block_category_list= browser.find_elements(By.XPATH, '//*[@id="page-wrapper"]/div/div[1]/div/div/div/div[*]/a')
category_list = []
for category in block_category_list:
    category_list.append(category.get_attribute("data-ss-tag-slug"))

# Hemos obtenido una lista con los nombres de las categorías

# %% 3. inicializacion de las variables

nList = list(range(0, 500))
base_url = 'https://www.skillshare.com/browse?seeAll=1&tagSlug=%&sort=rating&time=default&length=all&enrollmentType=both&page='


http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36", 
  }

# %% 3.1. OBTENEMOS LINK DE CADA CLASE DE CATEGORIA


for class_type in category_list:
    for num in nList:
        url = base_url + num
        page = requests.get(url, headers=http_header)
        if (page.status_code == 200):
            soup = BeautifulSoup(page.text, "html.parser")
            
            # Extract link for each class
            
