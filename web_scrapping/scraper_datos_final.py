import requests
from bs4 import BeautifulSoup
import json
import time
import os

def extraer_todo():
    url_principal = "https://lexi.global/sports"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    base_de_datos_completa = {}

    print(f"Extraccion en: {url_principal}")

    try:
        # 1. Obtener la lista de todos los deportes
        res = requests.get(url_principal, headers=headers)
        sopa_principal = BeautifulSoup(res.text, 'html.parser')
        
        # Usamos la clase que descubrimos antes: 'lexi-btn'
        botones_deportes = sopa_principal.find_all('a', class_='lexi-btn')
        
        # Filtramos para tener solo enlaces únicos de deportes reales
        enlaces_deportes = {}
        for b in botones_deportes:
            nombre = b.text.strip()
            url = b.get('href')
            if nombre and url and "ALL SPORTS" not in nombre and "WINTER SPORTS" not in nombre:
                if not url.startswith('http'):
                    url = "https://lexi.global" + url
                enlaces_deportes[nombre] = url

        print(f"Se han detectado {len(enlaces_deportes)} deportes para procesar.\n")

        # 2. Bucle para entrar en cada deporte
        for nombre_deporte, url_deporte in enlaces_deportes.items():
            print(f"Procesando: {nombre_deporte}")
            base_de_datos_completa[nombre_deporte] = {}

            # Entramos al deporte para ver sus categorías
            res_dep = requests.get(url_deporte, headers=headers)
            sopa_dep = BeautifulSoup(res_dep.text, 'html.parser')
            
            menu_categorias = sopa_dep.find('div', id='menuwrap')
            botones_cat = menu_categorias.find_all('a', class_='lexi-btn') if menu_categorias else []
            
            # 3. Bucle para entrar en cada categoría del deporte
            for b_cat in botones_cat:
                nombre_cat = b_cat.text.strip()
                url_cat = b_cat.get('href')
                if not url_cat.startswith('http'):
                    url_cat = "https://lexi.global" + url_cat
                
                print(f"  -> Clase: {nombre_cat}")
                time.sleep(0.5) # Pausa corta para no ser bloqueados

                try:
                    res_cat = requests.get(url_cat, headers=headers)
                    sopa_cat = BeautifulSoup(res_cat.text, 'html.parser')
                    
                    # Extraer descripción y perfiles
                    caja_texto = sopa_cat.find('h4', class_='lexitext')
                    desc = caja_texto.text.strip() if caja_texto else "Sin descripción"
                    
                    perfiles = []
                    imgs = sopa_cat.find_all('img', class_='lexiimg')
                    for i in imgs:
                        u_img = i.get('src', '')
                        perfiles.append({
                            "archivo_local": os.path.basename(u_img),
                            "explicacion_medica": i.get('title', i.get('alt', 'Silueta')).strip()
                        })
                    
                    base_de_datos_completa[nombre_deporte][nombre_cat] = {
                        "descripcion_general": desc,
                        "perfiles_visuales": perfiles
                    }
                except:
                    continue

        # 4. Guardar el Diccionario
        with open('lexi_database_FULL.json', 'w', encoding='utf-8') as f:
            json.dump(base_de_datos_completa, f, ensure_ascii=False, indent=4)
            
        print(f"\n Se ha generado 'lexi_database_FULL.json' con todos los deportes.")

    except Exception as e:
        print(f"Error {e}")

# Lanzar el proceso
extraer_todo()