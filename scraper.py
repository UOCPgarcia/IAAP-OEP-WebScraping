"""
Created on Thu Oct 21 13:59:37 2021
@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4


import pandas as pd
import requests
from bs4 import BeautifulSoup

# %% Inicialización de varibles

# Array con números naturales
nList = list(range(0, 18))
base_url ="https://www.juntadeandalucia.es/institutodeadministracionpublica/publico/seleccionjunta.filter?step=refresh&cp=1&id=1&chm=-1&ca=-1&cu=15&cdp=-1&ch=50&v="

links = list()

dataframe = pd.DataFrame();
columns = ["Año de Oferta Pública", "Tipo de Accesso", "Cuerpo/Especialidad ó Categoría Profesional", "Plazas", "Fun de plazo", "Estado", "Publicación de la convocatoria", "Url de accesso"]


http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
  }

# Obtenemos las convocatorias sobre las distintas convocatorias publicas
for number in nList:
    # Se obtienen las url
    url = base_url + number

    webpage = requests.get(base_url, headers=http_header)
    if (webpage.status_code == 200):
        
        soup = BeautifulSoup(webpage.text, "html.parser")
        
        # Se extraen los enlaces de cada convocatoria
        convocatorias = soup.findAll("a", {"href": re.compile()}) 


# %% NOTAS: TO DO:

- Solamente tenemos 17 paginas de ofertas.
    ¿Que pasa cuando se llega a la pagina 18?
    Implementamos un break, que pare cuando llegue a X
    pagina y no haya más convocatorias. ¿?
    ¿O nos interesa determinar manualmente el número de paginas a hacer web scraping?
            
  
