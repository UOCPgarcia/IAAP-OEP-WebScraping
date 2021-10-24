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
            
    














A PARTIR DE AQUÍ NO SIRVE 
CÓDIGO BASURA

# %% OBTENER LINKS DE LAS CATEGORIAS

urls_category_dic = {} #Dictionary or list?
url_template = 'https://www.skillshare.com/browse/%?seeAll=1'

for class_type in category_list:
    urls_category_dic[class_type] = url_template.replace('%', str(class_type))

# Obtenemos diccionarios con nombre(key) y url(value) de cada categoría.
# A cada uno de estos links son los que tenemos que hacer scrapping
# %% OBTENER LINK DE CADA COURSE comprentido dentro de cada categoría
# (mediante scrapping)


for class_type in category_list:
    i=0
    print('Working on getting list of all "' + class_type + '" courses')
    url = urls_category_dic[class_type]
        
opts = Options()
opts.headless = True
driver = webdriver.Chrome('./chromedriver/chromedriver', options=opts)
driver.get(url)

classes = browser = browser.find_elements(By.XPATH, '//*[@id="page-wrapper"]/div/div[2]/div[6]/ul/div[*]/div/a')




'https://www.skillshare.com/browse?seeAll=1&tagSlug=%&sort=rating&time=default&length=all&enrollmentType=both&page=#'

for class_type in category_list:
    urls_category_dic[class_type] = url_template.replace('%', str(class_type))



# xPATH to recover links:
# dosn't matter category.  //*[@id="page-wrapper"]/div/div[2]/div[6]/ul/div[*]/div/a


soup = BeautifulSoup(driver.page_source, 'html.parser')
class_link_tags = soup.find_all('div', attrs={"class": "col-4 class-column rendered "})
class_links = [class_link_tag.find('p').find('a')['href'] for class_link_tag in class_link_tags]
class_links_dict[class_type] = class_links
driver.close()

# %%

def get_links_from_txt(file):
    with open(file) as f:
        urls_dict = {}
        
        reader = f.readlines()
        
        for line in reader:
            isStart = True
            foo = line.strip().split(',')
            for item in foo:
                clean_item = item.strip().strip("[").strip("]").strip("'").strip()
                if isStart:
                    isStart = False
                    class_type = clean_item
                    urls_dict[class_type] = []
                else:
                    urls_dict[class_type].append(clean_item)
        return urls_dict

# %%

# get javascript that contains class info
def get_javascript_data(soup):
    projects_section = soup.find_all('script', attrs={"type": "text/javascript"})
    
    if not projects_section:
        return None
    
    for js in projects_section:
        try:
            if js.string:
                if re.search('.*SS.serverBootstrap =.*',js.text):
                    javascript = js.string
                    javascript = javascript.split("SS.serverBootstrap = ", 1)

                    javascript_data = javascript[1].split(";\n        ")[0]
                    javascript_data = json.loads(javascript_data)
        except:
            return None

    return javascript_data

# get author link
def get_title_and_author(soup):
    try:
        title = soup.find('title')
        return [item.strip() for item in title.text.split('|')]
    except:
        return []

# get teacher detail info from the javascripte
def get_detial_author_info(javascript_data):
    try:
        teacherInfo = javascript_data['pageData']['sectionData']['teacherInfo']
        return teacherInfo['fullName'], teacherInfo['headline'], teacherInfo['profileUrl']
    
    except:
        return None, None, None
    
# get class description info 
def get_class_description(soup):
    try:
        description_tag = (soup.find('div', attrs={"class": "about-this-class"})
                           .find('div', attrs={"class": "rich-content-wrapper"}))

        class_description = ""
        images, hyperlinks = 0, 0
        
        for paragraph in description_tag.findChildren():
            class_description += paragraph.text
            if paragraph.name == 'img':
                images += 1
            elif paragraph.name == 'a':
                hyperlinks += 1
                
        return len(class_description), images, hyperlinks
    
    except:
        return None, None, None
            
# get class length
def get_video_length(soup):
    try:
        video_content_tag = (soup.find('div', attrs={"class": "summary"})
                             .text.strip().strip('\n').strip())
        return video_content_tag #video_num, video_length
    except:
        None


# get tags linked to classes 
def get_tags(soup):
    tags = []
    try:
        tags_section = soup.find('div', attrs={"class": "tags-section"})
        for tag in tags_section.find_all('a'):
            tags.append(tag.text.strip())
    except:
        pass
    return tags
        
# get projects submitted for classes
def get_project_authors(javascript_data):    
    try:
        return [project['author']['fullName'] 
                for project in javascript_data['pageData']['sectionData']['topProjects']]
    except:
        return []

# get class sku as index
def get_class_sku(javascript_data):
    try:
        return javascript_data['classData']['sku']
    except:
        return None

# identify if class is free
def isPremium(javascript_data):
    try:
        return javascript_data['pageData']['headerData']['tagText'] == 'Premium class'
    except:
        return None

# get class start date
def get_start_date(javascript_data):
    try:
        return javascript_data['pageData']['syllabusData']['startTs']
    except:
        return None

# get enrollment number
def get_enrollment_number(javascript_data):
    try:
        return javascript_data['pageData']['sectionData']['numStudents']
    except:
        return None

def request_soup(url):
    ua = UserAgent()
    user_agent = {'User-agent': ua.random}
    response  = requests.get(url, headers = user_agent)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    return soup

# %% DATA SCRAPPING

file = 'class_urls-1.csv'

try:
    urls_dict = get_links_from_txt(file)
except:
    urls_dict = make_url(class_types)
    with open('class_list_urls.csv', 'w') as f:
        writer = csv.writer(f)
        for key, val in urls_dict.items():
            writer.writerow([key, val])

# %%            
            
columns = ['class_name',
          'teacher',
          'teacher_title',
          'teacher_profile',
          'description_length',
          'description_image_number',
          'description_link_number',
          'class_length',
          'tags',
          'sample_project',
          'class_sku',
          'paid_class',
          'start_date',
          'enrollment_number']
class_data = {col: [] for col in columns}

# %%

for class_type in class_types:
    
    print("working on ", class_type)
    class_data = {col: [] for col in columns}
    
    i = 0
    
    for this_class in urls_dict[class_type]:        
        time.sleep(5+2*random.random())
        
        try:
            soup = request_soup(this_class)            
        except:
            continue
            
        if not soup:
            continue
        
        isSaved = False
        while response.status_code != 200 or re.search('Access denied.*', soup.find('title').text):
            print("stop here")

            if not isSaved:
                pickle_title = class_type + ".pickle"
                pickle_out = open(pickle_title, "wb")
                pickle.dump(class_data, pickle_out)
                pickle_out.close()
                isSaved = True
                
            time.sleep(60*5)
            soup = request_soup(this_class) 
            
        i += 1
        if i%10 == 0:
            print(i)

        javascript_data = get_javascript_data(soup)

        class_data['class_name'].append(get_title_and_author(soup)[0])

        teacher, teacher_title, teacher_profile = get_detial_author_info(javascript_data)
        class_data['teacher'].append(teacher)
        class_data['teacher_title'].append(teacher_title)
        class_data['teacher_profile'].append(teacher_profile)

        description_length, description_image_number, description_link_number = get_class_description(soup)
        class_data['description_length'].append(description_length)
        class_data['description_image_number'].append(description_image_number)
        class_data['description_link_number'].append(description_link_number)

        class_data['class_length'].append(get_video_length(soup))

        class_data['tags'].append(get_tags(soup))
        class_data['sample_project'].append(teacher in get_project_authors(javascript_data))
        class_data['class_sku'].append(get_class_sku(javascript_data))
        class_data['paid_class'].append(isPremium(javascript_data))
        class_data['start_date'].append(get_start_date(javascript_data))
        class_data['enrollment_number'].append(get_enrollment_number(javascript_data))

    pickle_title = class_type + ".pickle"
    pickle_out = open(pickle_title,"wb")
    pickle.dump(class_data, pickle_out)
    pickle_out.close()

# %% APPENDIX

class_types = ['fine-art',
               'photography',
               'graphic-design',
               'illustration',
               'writing',
               'music-production',
               'animation',
               'ui-ux-design',
               'film-production',
               'marketing',
               'entrepreneurship',
               'productivity',
               'finance',
               'freelance',
               'business-analytics',
               'management',
               'leadership',
               'sales',
               'human-resources',
               'accounting',
               'web-development',
               'mobile-development',
               'it-security',
               'data-science',
               'game-design',
               'product-management',
               'crafts',
               'culinary',
               'health-and-wellness',
               'other',
               'teaching',
               'home-business',
               'languages',
               'gaming']

pickle.dump(class_types, open("class_types.pickle", "wb"))