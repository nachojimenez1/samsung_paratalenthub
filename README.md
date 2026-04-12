# 🦾 Samsung ParaTalent Hub: Clasificación Paralímpica Inteligente y Deteccion de Talento

**ParaTalent Hub** es una plataforma avanzada de triaje y soporte a la clasificación médica para el **Comité Paralímpico Español (CPE)**. Utiliza una arquitectura de **Recuperación Aumentada por Generación (RAG)** para conectar los relatos subjetivos de los atletas con el corpus de conocimiento experto de **LEXI** (Library of Evidence for Classification in Paralympic Sport).

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-04A6E1?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/AI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)

---

## 🚀 Características Principales

- **Motor RAG de Clasificación:** Transforma descripciones coloquiales en clasificaciones técnicas mediante embeddings vectoriales.
- **Portal del Atleta (`Home.py`):** Interfaz intuitiva para el registro de deportistas y captación de "Medical Flags" (discapacidad visual, física, intelectual).
- **Panel del Inspector (`1_Admin.py`):** Dashboard de alto rendimiento que permite a los técnicos del CPE validar expedientes con soporte de IA.
- **Consistencia Anatómica:** Sistema de reranking con reglas críticas que impide alucinaciones médicas (ej. no sugiere perfiles de amputación si el atleta no tiene pérdida de miembros).
- **Web Scraping Automatizado:** Extracción y estructuración de datos directamente desde `lexi.global`.

## 🛠️ Stack Tecnológico

- **Framework:** Streamlit (UI reactiva).
- **IA Generativa:** OpenAI (GPT-4o-mini y `text-embedding-ada-002`).
- **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search).
- **Backend-as-a-Service:** Airtable (Persistencia en la nube y gestión de estados de expedientes).
- **Procesamiento de Lenguaje:** LangChain para la gestión del flujo RAG.

## 📐 Arquitectura del Sistema

El sistema opera bajo un flujo de 4 etapas:
1. **Normalización Semántica:** Traducción del relato del atleta al inglés médico técnico.
2. **Recuperación (Retrieval):** Búsqueda de los 15 candidatos más cercanos en el espacio vectorial de 1536 dimensiones.
3. **Reranking por Reglas Críticas:** Filtrado lógico basado en Flags médicos (Visual, Intelectual, Físico) y consistencia anatómica.
4. **Validación Humana:** Presentación jerarquizada de los 9 mejores perfiles para la decisión final del inspector.

## 🔧 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/nachojimenez1/samsung_paratalenthub.git](https://github.com/nachojimenez1/samsung_paratalenthub.git)
   cd samsung_paratalenthub
