# 🦾 Samsung ParaTalent Hub: Clasificación Paralímpica Inteligente y Deteccion de Talento

**ParaTalent Hub** es una plataforma avanzada de triaje y soporte a la clasificación médica para el **Comité Paralímpico Español (CPE)**. Utiliza una arquitectura de **Recuperación Aumentada por Generación (RAG)** para conectar los relatos subjetivos de los atletas con el corpus de conocimiento experto de **LEXI** (Library of Evidence for Classification in Paralympic Sport).

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-04A6E1?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/AI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/Deep_Learning-TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

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

## 🧪 Módulo de Inteligencia Artificial Predictiva (Talent Detection)

Más allá de la clasificación administrativa, **ParaTalent Hub** integra un motor de análisis avanzado para la detección de potencial deportivo. Este módulo procesa métricas biométricas y de rendimiento para sugerir las disciplinas donde el atleta tiene mayor probabilidad de éxito.

### 🤖 Modelos Implementados

Para este proceso de triaje deportivo, se han desarrollado y comparado dos arquitecturas distintas:

* **Random Forest Classifier (Machine Learning):**
    * **Propósito:** Proporcionar un modelo altamente interpretable.
    * **Feature Importance:** Nos permite identificar qué variables físicas (fuerza, rango de movimiento, coordinación) son determinantes para cada deporte.
    * **Robustez:** Ideal para manejar datos tabulares y evitar el sobreajuste (overfitting).

* **MLP - Multi-Layer Perceptron (Deep Learning):**
    * **Propósito:** Modelar relaciones no lineales complejas entre la discapacidad y el rendimiento.
    * **Arquitectura:** Una red neuronal densa con múltiples capas ocultas que procesa los datos del atleta para generar un **Score de Talento**.
    * **Generalización:** Capaz de encontrar patrones sutiles en los datos históricos que los modelos lineales ignoran.

### 📈 Flujo de Decisión Predictiva

1.  **Entrada:** Datos físicos y resultados de pruebas de esfuerzo.
2.  **Inferencia:** Procesamiento paralelo por ambos modelos (RF y MLP).
3.  **Salida:** Posible futuro Talento.

## 🔧 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/nachojimenez1/samsung_paratalenthub.git](https://github.com/nachojimenez1/samsung_paratalenthub.git)
   cd samsung_paratalenthub
