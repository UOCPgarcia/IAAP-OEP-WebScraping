"""
Created on Thu Oct 21 13:59:37 2021
@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4
# pip install selenium

import os #robots

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle
import time
import csv

from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By


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


# Lectura de propietario


# Lista que contendra las urls de cada convocatoría
urls_convocatorias = list()

fails_count = 0

# Header para BeautifulSoup
http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
  }


# %%

# Obtenemos los enlaces sobre las distintas convocatorias publicas.
# Iteramos por cada número natural de la lista.
for number in nList:
    # Se obtienen las url de la página
    url = base_url + str(number)
    
    # Configuramos el driver
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=option)
    driver.get(url) # <- problema. El navegador abre cada una de las páginas de las convocatorias...
    
    webpage_list = requests.get(base_url, headers=http_header)
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

# Guardamos los urls en un archivo de texto. Así no tenemos que iterar cada vez.             
with open('./data/urls_convocatorias.pickle', 'wb') as fp:
    pickle.dump(urls_convocatorias, fp)            
           

# %%         
    
fails_count = 0

with open('./data/urls_convocatorias.pickle', 'rb') as fp:
    urls_convocatorias = pickle.load(fp)

#Inicializamos el diccionario de datos donde cargaremos la información
data = []
  
# Iteramos sobre los links para obtener información de cada uno de ellos.
for convocatoria in urls_convocatorias:

    # Obtenemos el html
    webpage_convocatoria = requests.get(convocatoria, headers=http_header)
    
    if(webpage_convocatoria.status_code == 200):
        soup = BeautifulSoup(webpage_convocatoria.text, "html.parser")
        
        # Obtenemos datos convocatoría        
        whole_section = soup.find('div', {'class':"ficha"})
        
        
        # Nombre convocatoría
        try:
            name_convocatoria = whole_section.h2.text
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
        



#Como último paso trasladamos los datos a un dataframe para poder volcarlos a un csv
df = pd.DataFrame(data)
df.to_csv('./data/JAconvocatoriasPublicas.csv', index=False)
        

# CHANGES

'''
(27/10/2021). Links de cada convocatoría guardados en un archivo de texto. Así nos estalviamos iterar por la web cada vez que queramos provar si el codigo psterior funciona adecuadamente.
(28/10/2021). Conseguido extraer, correctamente, la información de cada categoría. 
(29/10/2021). Finalmente he podido guardarlo en la estructura correcta.
'''

# ERRORS/PROBLEMS TO SOLVE

'''
(28/10/2021). No acabo de conseguir pasar los datos obtenidos de: listas a columnas del dataset. He creado algo funcional, pero 
    no termina de funcionar correctamente (el dataset queda mal ordenado). Mañana seguramente lo pregunte a StackOverflow.
    (29/10/2021) SOLUCIONADO. Resulta que había un salto de línea delante de cada valor, por eso cuando habría con excel el archivo csv no los veía, porque estaban escondidos.
'''

# %% NOTES/ TO DO:
'''
- Solamente tenemos 18 paginas de ofertas. Ahora mismo estamos delimitando el número de páginas al inicio...con una lista de números (del 0 al 19)
    ¿Que pasa cuando se llega a la pagina 20?
    ¿Implementamos un break, que pare cuando llegue a +20 pagina y no haya más convocatorias?
    
    
- Vemos que los links de cada convocatorias estan repetidos multiples veces. Dificultades:
    * extraer solamente los links de las convocatorias, no link de otros elementos. ¿Como podemos distinguir unos de otros?
        en caso de ser posible su extraccion, nos encontrariamos con muchos links repetidos. (Se puede solucionar facilemnte creando un SET{}??) 
    * SOLUCIÓN PROPUESTA: Utilizamos webdriver para extraer concretamente los links comprendidos en la primera columna. No tenemos links repetidos. Pero:
        a causa de la solución establecida en el punto anterior. El driver abre cada una de las páginas de convocatoria (en este caso 20!!)
        ¿ESTO TIENE SOLUCIÓN o es el comportamiento normal de webdriver?

'''

