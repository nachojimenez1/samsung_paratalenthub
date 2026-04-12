import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extraer_imagenes(url_objetivo):
    print(f"Iniciando scraping en: {url_objetivo}")
    
    # 1. Creamos la carpeta
    carpeta = "imagenes_lexi"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # 2. Ponemos un navegador real para que la web no nos bloquee
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # 3. Entramos en la web
        respuesta = requests.get(url_objetivo, headers=headers)
        respuesta.raise_for_status() # Comprobamos que no nos hayan echado (Error 404, 403...)
        
        # 4. Le pasamos el código fuente a BeautifulSoup para que busque
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Buscamos TODAS las etiquetas de imagen (<img>)
        imagenes = sopa.find_all('img')
        print(f"🕵️‍♂️ ¡Bingo! He detectado {len(imagenes)} imágenes en el código fuente.")

        # 5. Descargamos una a una
        contador = 1
        for img in imagenes:
            # Sacamos el enlace real de la foto
            url_img = img.get('src')
            
            # Si la imagen no tiene enlace, pasamos a la siguiente
            if not url_img:
                continue
                
            # A veces los enlaces están rotos o son relativos (ej: /assets/foto.jpg)
            # urljoin los arregla uniéndolos a la web original
            url_img_completa = urljoin(url_objetivo, url_img)

            # Extraemos el nombre original del archivo (ej: silla_ruedas.png)
            nombre_original = url_img_completa.split("/")[-1].split("?")[0]
            
            # Si el nombre es muy raro, le ponemos nosotros uno genérico
            if len(nombre_original) < 3:
                nombre_original = f"imagen_{contador}.jpg"

            ruta_guardado = os.path.join(carpeta, nombre_original)

            # Descargamos la imagen física y la guardamos en el disco duro
            try:
                img_data = requests.get(url_img_completa, headers=headers).content
                with open(ruta_guardado, 'wb') as archivo_local:
                    archivo_local.write(img_data)
                print(f"[{contador}] Descargada: {nombre_original}")
                contador += 1
            except Exception as e:
                print(f"Error al descargar {url_img_completa}: {e}")

        print("\n Guardado en carpeta 'imagenes_lexi'.")

    except Exception as e:
        print(f"Error al conectar con la web: {e}")


url_a_extraer = "https://lexi.global/sports/impairment-to-class/" 

extraer_imagenes(url_a_extraer)