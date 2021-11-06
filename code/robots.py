# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:57:46 2021

@author: x
"""

#%% IMPORTACIÓN DE LAS LIBRERIAS

import os #robots
import whois

#%% ANÁLISIS PRELIMINARES

# Lectura de robots.txt

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


# Lectura de propietario (null)

fic2 = open("./data/JAwhois.txt","w")

print(whois.whois("https://www.juntadeandalucia.es"), file=fic2)

fic2.close()
