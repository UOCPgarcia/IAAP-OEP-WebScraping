"""
Created on Thu Oct 21 13:59:37 2021
@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4
# pip install selenium
# pip install tqdm
# pip install python-whois


import os #robots
import whois

import pandas as pd
from bs4 import BeautifulSoup
import pickle
import time

from datetime import date

from tqdm import tqdm

import random 
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

# %% Inicialización de variables

base_url ="https://www.juntadeandalucia.es/institutodeadministracionpublica/publico/seleccionjunta.filter?step=refresh&cp=1&id=1&chm=-1&ca=-1&cu=15&cdp=-1&ch=50&v="

# Array con números naturales
nList = list(range(0, 19))


# Lectura de robots

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
       

# Lista que contendra las urls de cada convocatoría
urls_convocatorias = list()

fails_count = 0 # Numero de fallos para el 1º scraper

# %% pool de User-Agents 
# Header para BeautifulSoup

headers_list = [
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",},
{"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",},
{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",},
]


# Create ordered dict from Headers above
ordered_headers_list = []

for headers in headers_list:
    h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
        ordered_headers_list.append(h)

# %%


# Obtenemos los enlaces sobre las distintas convocatorias publicas.
# Iteramos por cada número natural de la lista.
for number in tqdm(nList):
    # Se obtienen las url de la página
    url = base_url + str(number)
    
    # Configuramos el driver (con modo headless)
    option = webdriver.ChromeOptions()
    option.headless= True
    driver = webdriver.Chrome('./chromedriver/chromedriver', options=option)
    driver.get(url) 
    
    try:
        element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, "contenido")))
    
        webpage_list = requests.get(base_url)
        if (webpage_list.status_code == 200):
            # Indicamos la ruta XPATH donde se encuentran los vínculos.
            bloque_convocatorias = driver.find_elements(By.XPATH, '//*[@id="contenido"]/div[3]/table/tbody/tr[*]/td[1]/a')
            
            # Se extraen los enlaces de cada convocatoria
            for url in bloque_convocatorias:
                urls_convocatorias.append(url.get_attribute('href'))
        
        else:
            # En caso de error se avisa al usuario.
            print("\nERROR - Status Code: "+ webpage_list.status_code +"\n")
            fails_count += 1
            # El número máximo de errores es 20. El tiempo de espera es incremental.
            if (fails_count > 20): break
            time.sleep(1 * fails_count)
    finally:
        driver.quit()


# Guardamos los urls en un archivo de texto. Así no tenemos que iterar cada vez.             
with open('./data/urls_convocatorias.pickle', 'wb') as fp:
    pickle.dump(urls_convocatorias, fp)            
           

# %%         
    
with open('./data/urls_convocatorias.pickle', 'rb') as fp:
    urls_convocatorias = pickle.load(fp)

#Inicializamos el diccionario de datos donde cargaremos la información
data = []
  
# Iteramos sobre los links para obtener información de cada uno de ellos.
for convocatoria in tqdm(urls_convocatorias, desc="progress bar"):
    
    try: 
        
        #Pick a random browser headers
        for i in range(1,12):       
            headers = random.choice(headers_list)
        
        # Establecemos una misma session y implementamos retry
        # Intentará conectarse como máximo 5 veces, y con un incremento de *0.3 cada vez.
        # Añadimos los headers
        session = requests.Session() 
        session.headers = headers

        retry = Retry(connect=5, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)   
        
    
        # Obtenemos el html
        webpage_convocatoria = session.get(convocatoria)
        
        if webpage_convocatoria.status_code == 200:
            soup = BeautifulSoup(webpage_convocatoria.text, "html.parser")
            
            # Obtenemos datos convocatoría        
            whole_section = soup.find('div', {'class':"ficha"})
            
            
            # Nombre convocatoría
            try:
                name_convocatoria = whole_section.h3.text
            except:
                name_convocatoria = "NaN"
                
            # Año convocatoría
            try:        
                year_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Año de Oferta Pública:' in element.text)
                for span in year_convocatoria.find_all('span'):
                    span.decompose()
                    year_convocatoria = year_convocatoria.text.strip()
            except:
                year_convocatoria = "NaN"
                
            # Categoría Profesional   
                
            try:    
                category_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Cuerpo:' in element.text)
                for span in category_convocatoria.find_all('span'):
                    span.decompose()
                    category_convocatoria = category_convocatoria.text.strip()
            except:
                category_convocatoria = "NaN"
                
            # Tipo de Acceso     
            try:
                access_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Tipo de Acceso:' in element.text)
                for span in access_convocatoria.find_all('span'):
                    span.decompose()
                    access_convocatoria = access_convocatoria.text.strip()
            except:
                access_convocatoria = "NaN"
                
            # Número de plazas    
            try:
                plazas_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Número de plazas:' in element.text)
                for span in plazas_convocatoria.find_all('span'):
                    span.decompose()
                    plazas_convocatoria = plazas_convocatoria.text.strip()
            except:
                plazas_convocatoria = "NaN"
            
            # Fin plazo de solicitud
            try:
                end_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Finaliza plazo de solicitud:' in element.text)
                for span in end_convocatoria.find_all('span'):
                    span.decompose()
                    end_convocatoria = end_convocatoria.text.strip()
            except:
                end_convocatoria = "NaN"
            
            # Publicación de la convocatoria (BOJA) y link
            try:
                BOJA_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Publicación de la convocatoria:' in element.text)
                for link in BOJA_convocatoria.find_all('a'):    
                    link_BOJA = link.get('href')
                for span in BOJA_convocatoria.find_all('span'):
                    span.decompose()
                    publicacion_BOJA = BOJA_convocatoria.text.strip()
            except:
                publicacion_BOJA = "NaN"
                link_BOJA = "NaN"
            
            # Modificación de la convocatoria (reply: yes/no)
            
            try:
                mod_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Modificación de la convocatoria:' in element.text)
                for spna in mod_convocatoria.find_all('span'):
                    mod_convocatoria = "Yes"
            except:
                mod_convocatoria = "No"        
            
            # Estado
            try:
                status_convocatoria = whole_section.find(lambda element: element.name == 'p' and 'Estado:' in element.text)
                for span in status_convocatoria.find_all('span'):
                    span.decompose()
                    status_convocatoria = status_convocatoria.text.strip()
            except:
                status_convocatoria = "NaN"
                
    
            #append dict to array
            data.append({"Año de Oferta Pública" : year_convocatoria,
                        "Nombre de la Convocatoría" : name_convocatoria,
                        "Tipo de Accesso" : access_convocatoria,
                        "Cuerpo/Especialidad ó Categoría Profesional" : category_convocatoria,
                        "Número de Plazas" : plazas_convocatoria, 
                        "Fin de plazo" : end_convocatoria,
                        "Publicación de la convocatoria" : publicacion_BOJA,
                        "Url BOJA" : link_BOJA,
                        "¿Ha habido modificaciones en la convocatoría?": mod_convocatoria,
                        "Estado": status_convocatoria,
                        "Url de accesso" : convocatoria,
                        "Fecha de extracción": date.today()})
            
    except:
        print("Connection error. Couldn't scraper")


#Como último paso trasladamos los datos a un dataframe para poder volcarlos a un csv
df = pd.DataFrame(data)
df.to_csv('./data/JAconvocatoriasPublicas.csv', index=False)
        



