# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:15:16 2021

@author: MPilar
"""

"""
Created on Thu Oct 21 13:59:37 2021
@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4
# pip install selenium

import os #robots

#import pandas as pd
#import requests
#from bs4 import BeautifulSoup
#import pickle
#import time
#import csv

#from datetime import date

#from selenium import webdriver
#from selenium.webdriver.common.by import By


# %% Inicialización de variables

base_url ="https://www.juntadeandalucia.es/institutodeadministracionpublica/publico/seleccionjunta.filter?step=refresh&cp=1&id=1&chm=-1&ca=-1&cu=15&cdp=-1&ch=50&v="

# Array con números naturales
nList = list(range(0, 19))


# Lectura de robots <- pendiente de pruebas

result = os.popen("curl https://www.juntadeandalucia.es/robots.txt").read()
result_data_set = {"Disallowed":[], "Allowed":[]}

fic = open("./data/JArobots.txt","w")

for line in result.split("\n"):
    if line.startswith('Allow'):    # this is for allowed url
        result_data_set["Allowed"].append(line.split(': ')[1].split(' ')[0])    # to neglect the comments or other junk info
    elif line.startswith('Disallow'):    # this is for disallowed url
        result_data_set["Disallowed"].append(line.split(': ')[1].split(' ')[0])    # to neglect the comments or other junk info
       
print(result_data_set, file=fic)

fic.close()

