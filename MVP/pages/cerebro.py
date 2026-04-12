import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Cargar JSON
with open('lexi_database_FULL.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Extraer descripciones únicas y mapeo de deportes
docs_para_rag = []
mapa_img_a_deportes = {}
descripciones_vistas = set()

for deporte, categorias in data.items():
    for cat, info in categorias.items():
        for perfil in info['perfiles_visuales']:
            img = perfil['archivo_local']
            desc = perfil['explicacion_medica']
            
            # Mapeo Imagen -> Deportes
            if img not in mapa_img_a_deportes:
                mapa_img_a_deportes[img] = []
            relacion = f"{deporte} - {cat}"
            if relacion not in mapa_img_a_deportes[img]:
                mapa_img_a_deportes[img].append(relacion)
            
            # Documentos para el RAG (solo únicos)
            if desc and desc not in descripciones_vistas:
                docs_para_rag.append(Document(page_content=desc, metadata={"img": img}))
                descripciones_vistas.add(desc)

# 3. Crear base de datos vectorial (Embeddings)
vectorstore = FAISS.from_documents(docs_para_rag, OpenAIEmbeddings())
vectorstore.save_local("faiss_lexi") # Lo guardamos para usarlo en el Admin.py