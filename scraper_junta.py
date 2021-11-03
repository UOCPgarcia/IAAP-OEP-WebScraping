#!/usr/bin/env python
# coding: utf-8

# Cargamos las librerías que utilizaremos
from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce


def get_soup(url):
    "Obtiene un BeautifulSoup de la url"
    headers = {
        "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    return soup


def lee_tabla_url(url):
    "Devuelve una matriz con la información de la tabla a partir de la url"
    soup = get_soup(url)
    table_data = soup.find('table', class_ = 'listado')


    headers = []
    rows = []

    for i in table_data.find_all('th'):
        title = i.text
        headers.append(title)
        
    rows.append(headers)

    for j in table_data.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [tr.text for tr in row_data]
        rows.append(row)

    return rows

#url a scrapear
url = "https://www.juntadeandalucia.es/institutodeadministracionpublica/publico/seleccionjunta.filter?cu=15&step=refresh"

# Lee datos de la tabla de la primera página
data = lee_tabla_url(url)

# Obtiene una lista de url de las distintas páginas
soup = get_soup(url)
page_data = soup.find('div', class_ = 'paginacion').find_all('a')
# for embebido
urls = [url.get("href") for url in page_data]

# Otra posible forma de hacer el for anterior, sin embebimiento
#for url in page_data:
#    urls.append(url.get("href"))


# Para cada página obtenemos los datos y los unimos en el listado general data
for url in urls:
    # obtenemos los datos de la página menos la cabecera ([1:]) que ya se metío con la primera página
    data_page = lee_tabla_url(url)[1:]
    # Añadimos los datos de la página a la variable general data
    data.extend(data_page)

# Usamos un dataframe para escribir en fichero csv
df = pd.DataFrame(data[1:], columns=data[0])        
df.to_csv("data/empleo.csv", index=False)
