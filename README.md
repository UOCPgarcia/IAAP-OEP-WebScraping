# Práctica 1: Web scraping
IAAP-OEP-WebScraping,
Práctica WebScrapping UOC M2.851

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos (M2.851), perteneciente
al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya (UOC). En ella, se aplican técnicas de web
scraping mediante el lenguaje de programación Python para extraer así datos de la web de interés y generar un dataset.

La web elegida ha sido el Instituto Andaluz de Administración Pública, que aloja las diferentes ofertas de empleo público de Andalucía.

![Instituto Andaluz de administración publica](https://sindicatotecnos.es/wp-content/uploads/2020/04/Instituto-Andaluz-de-la-Administraci%C3%B3n-P%C3%BAblica.jpg
'Instituto Andaluz de Administración Pública')


## Miembros del equipo

El proyecto ha sido realizado de forma conjunta por:
- **María Pilar Garcia Ruiz**
- **Adrià Cortés Andrés**

## Estructura del repositorio

- ./data/practica1_tipologia.pdf memoría del proyecto, con las respuestas a las preguntas planteadas. 
- ./data/JAconvocatoriasPublicas.csv dataset obtenido.
- ./data/urls_convocatorias.pickle archivo pickle que aloja los links de cada conocatoria.
- ./code/scraper.py archivo Python que contiene el código del web scraper.
- ./code/robots.py archivo Python que contiene el código para el analísis de robots y propietario. 
- ./chromedriver/chromedriver.exe contiene el *driver* de la versión de Chrome especifica, necesaria para Selenium.
- ./otros desarrollos/ contiene proyectos descartados, pero que mantenían cierta funcionalidad.

## DOI 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5651108.svg)](https://doi.org/10.5281/zenodo.5651108)
