"""
Created on Thu Oct 21 13:59:37 2021
@author: Usuario
"""

# %% 1. Import libraries

# pip install pandas
# pip install bs4
# pip install selenium


import pandas as pd
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By


# %% Inicialización de varibles

# Array con números naturales
nList = list(range(0, 18))
base_url ="https://www.juntadeandalucia.es/institutodeadministracionpublica/publico/seleccionjunta.filter?step=refresh&cp=1&id=1&chm=-1&ca=-1&cu=15&cdp=-1&ch=50&v="

urls_convocatorias = list()

dataframe = pd.DataFrame();
columns = ["Año de Oferta Pública", "Tipo de Accesso", "Cuerpo/Especialidad ó Categoría Profesional", "Plazas", "Fun de plazo", "Estado", "Publicación de la convocatoria", "Url de accesso"]

fails_count = 0


http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
  }


#



# Obtenemos los enlaces sobre las distintas convocatorias publicas
for number in nList:
    # Se obtienen las url de la página
    url = base_url + str(number)
    
    # Configuramos el driver
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=option)
    driver.get(url) # <- problema. El navegador abre cada una de las páginas de las convocatorias...
    
    webpage = requests.get(base_url, headers=http_header)
    if (webpage.status_code == 200):
        
        bloque_convocatorias = driver.find_elements(By.XPATH, '//*[@id="contenido"]/div[3]/table/tbody/tr[*]/td[1]/a')
        
        # Se extraen los enlaces de cada convocatoria
        for url in bloque_convocatorias:
            urls_convocatorias.append(url.get_attribute('href'))
    
    else:
        # En caso de error se avisa al usuario.
        print("\nERROR - Status Code: "+ page.status_code +"\n")
        fails_count += 1
        # El número máximo de errores es 20. El tiempo de espera es incremental.
        if (fails_count > 20): break
        time.sleep(1 * fails_count)
    
    print(urls_convocatorias) # <- parece que podemos obtener los links sin ningún problema. 
    # (nota) CONTINUAR. utilizamos dichos links para obtener información que nos interesa y elaborar la tabla. 
        



# %% NOTAS: TO DO:

- Solamente tenemos 17 paginas de ofertas.
    ¿Que pasa cuando se llega a la pagina 18?
    Implementamos un break, que pare cuando llegue a X
    pagina y no haya más convocatorias. ¿?
- Vemos que los links de cada convocatorias estan repetidos multiples veces. Dificultades:
    * extraer solamente los links de las convocatorias, no link de otros elementos. ¿Como podemos distinguir unos de otros?
        en caso de ser posible su extraccion, nos encontrariamos con muchos links repetidos. (Se puede solucionar facilemnte creando un SET{}??) 
    * Solución propuesta. Utilizamos webdriver, para extraer concretamente los links comprendidos en la primera columna. No tenemos links repetidos.
- A causa de la solución establecida en el punto anterior. El driver abrir cada una de las páginas de convocatoria (en este caso 18!!) ¿solución?
    
# %% partes de codigo descartadas

soup = BeautifulSoup(webpage.text, "html.parser")
