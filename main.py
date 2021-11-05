"""
Obtener las playlist de Canal Fiesta Radio
"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import datetime
s = Service('edgedriver_win64/msedgedriver.exe')
driver = webdriver.Edge(service=s)

def aceptarCookies():
    btnsCokkies = driver.find_elements(By.CLASS_NAME, 'fc-button-label')
    btnCookie = []

    for btn in btnsCokkies:
        if btn.text == 'Aceptar':
            btnCookie.append(btn)
    btnCookie[0].click()

def generarCSV(data):

    dtNow = datetime.datetime.now()
    dtFormat = dtNow.strftime('%Y%m%d')
    # print(dtFormat)
    nombre = f"DATOS_PLAYLIST_{dtFormat}"
    dtCSV = data.to_csv(nombre, index_label=False, index=False, sep=';')

def top50():
    btnsMenuNoticias = driver.find_elements(By.CLASS_NAME, 'enlaceMenuNoticias')
    btnTop50 = []
    for btn in btnsMenuNoticias:
        if btn.text == 'TOP 50':
            btnTop50.append(btn)
    btnTop50[0].click()
def obtenerCanciones():
    # Cambiamos a la pestaña 1
    driver.switch_to.window(driver.window_handles[1])
    filas = driver.find_elements(By.TAG_NAME, 'tr')
    posicion = []
    artista = []
    cancion = []
    for f in filas:
        posicion.append(f.find_element(By.TAG_NAME, 'td').text)
        # print(f.find_elements(By.TAG_NAME, 'p')[0].text)
        artista.append(f.find_elements(By.TAG_NAME, 'p')[0].text)
        cancion.append(f.find_elements(By.TAG_NAME, 'p')[1].text)

    playlist = {
        'posicion': posicion
        , 'artista': artista
        , 'cancion': cancion
    }

    dt = pd.DataFrame(playlist)

    return dt


def obtenerPlayList(url):
    driver.get(url)
    time.sleep(1)
    """
        Funcion para aceptar las cookies
    """
    aceptarCookies()
    """
        Funcion para ir a la sección top 50
    """
    top50()
    time.sleep(1)
    """
        Funcion para obtener la playlist de canciones
    """
    data = obtenerCanciones()
    """
        Funcion para generar el CSV
    """
    generarCSV(data)

try:
    URL = 'https://www.canalsur.es/radio/canalfiesta-1293.html'
    print("Obtener la playlist")
    obtenerPlayList(URL)

except Exception as e:
    print(f"Error: {e}")