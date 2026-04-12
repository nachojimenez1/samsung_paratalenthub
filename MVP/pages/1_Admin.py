import streamlit as st
import json
import os
import re
from dotenv import load_dotenv
from pyairtable import Api
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# 1. CONFIGURACIÓN E INTERFAZ
load_dotenv()
st.set_page_config(page_title="Panel de Control - CPE", layout="wide", page_icon="🕵️‍♂️")

AIRTABLE_KEY = os.getenv("AIRTABLE_API_KEY", "").replace('"', '').strip()
BASE_ID = os.getenv("AIRTABLE_BASE_ID", "").replace('"', '').strip()
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "").replace('"', '').strip()

# --- ESTADOS PARA PAGINACIÓN ---
if 'candidatos' not in st.session_state:
    st.session_state.candidatos = []
if 'img_seleccionada' not in st.session_state:
    st.session_state.img_seleccionada = None
if 'atleta_actual' not in st.session_state:
    st.session_state.atleta_actual = None
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 0  # Controla si vemos los 1-3, 4-6 o 7-9

@st.cache_resource
def cargar_recursos():
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("faiss_lexi", embeddings, allow_dangerous_deserialization=True)
    with open('mapa_deportes.json', 'r', encoding='utf-8') as f:
        mapa = json.load(f)
    return vectorstore, mapa

vectorstore, mapa_deportes = cargar_recursos()

# 2. SEGURIDAD
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso Restringido")
        pwd = st.text_input("Introduce la clave de Inspector", type="password")
        if st.button("Entrar"):
            if pwd == "CPE2026": 
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
        return False
    return True

if not check_password():
    st.stop()

# 3. LÓGICA DE IA (Modificada solo para pedir 9 IDs en lugar de 3)

def analizar_perfil_avanzado(datos_completos, vectorstore):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 1. Recuperación de todos los checks originales
    checks = []
    if datos_completos.get('D_Visual'): checks.append("Visual")
    if datos_completos.get('D_Intelectual'): checks.append("Intellectual")
    if datos_completos.get('D_Fisica'): checks.append("Ataxia/Hypertonia/Muscle Power")
    if datos_completos.get('D_Extremidades'): checks.append("Limb Deficiency/Amputation")
    
    # String detallado para que el LLM entienda la patología exacta
    info_medica = ", ".join(checks) if checks else "Physical impairment"

    # 2. Traducción técnica
    analisis_previo = llm.invoke(f"""
    Analyze this athlete file for LEXI classification:
    - Description: {datos_completos.get('Descripcion', '')}
    - Causa: {datos_completos.get('Causa_Discapacidad', 'No especificada')}
    - Medical Flags (Specific Impairments): {info_medica}
    - Affected area: {datos_completos.get('Extremidades_Afecta', 'No especificada')}
    
    TASK: Translate the profile to technical English. 
    Use LEXI terminology (e.g., use 'Impaired Muscle Power' or 'Hypertonia' if mentioned).
    Return ONLY the translation.
    """)
    
    translation = analisis_previo.content.strip()

    # 3. Búsqueda Vectorial (Seleccion de 15 candidatos)
    docs_k15 = vectorstore.similarity_search(translation, k=15)
    contexto_lexi = "\n".join([f"ID:{i} - {d.page_content}" for i, d in enumerate(docs_k15)])
    
    # 4. Reranking con TODAS las Reglas Críticas
    prompt_final = f"""
    You are a Medical Classifier for the Spanish Paralympic Committee.
    
    ATHLETE PROFILE (TECHNICAL):
    {translation}

    FLAGS:
    - Visual: {'YES' if datos_completos.get('D_Visual') else 'NO'}
    - Intellectual: {'YES' if datos_completos.get('D_Intelectual') else 'NO'}
    - Limb Deficiency/Amputation: {'YES' if datos_completos.get('D_Extremidades') else 'NO'}
    - Physical (Motor): {'YES' if datos_completos.get('D_Fisica') else 'NO'}

    LEXI CANDIDATES:
    {contexto_lexi}

    TASK: Select the 9 best profiles.
    CRITICAL RULES: 
    1. IF Visual Flag is YES: ONLY select 'Vision Impairment' profiles. EXCLUDE ALL OTHERS.
    2. IF Intellectual Flag is YES: ONLY select 'Intellectual Impairment' profiles. EXCLUDE ALL OTHERS.
    3. IF Limb Deficiency/Amputation Flag is NO: EXCLUDE profiles mentioning 'absence of limb', 'amputation', or 'stump'.
    4. IF Physical Flag is YES: Focus on coordination and muscle power profiles.
    5. ANATOMICAL CONSISTENCY: Strictly respect the localization of the impairment. If the athlete's description is localized (e.g., ONLY arms, ONLY legs, or ONLY one side), EXCLUDE profiles that involve the entire body, the trunk, or unaffected limbs. The match must be anatomically precise
    
    Return ONLY the 9 numerical IDs separated by commas.
    """
    
    res_ids = llm.invoke(prompt_final)
    
    try:
        numeros_encontrados = re.findall(r'\d+', res_ids.content)
        ids = [int(n) for n in numeros_encontrados]
        
        # Devolvemos los documentos correspondientes a esos IDs
        return [docs_k15[i] for i in ids[:9] if i < len(docs_k15)]
    except Exception as e:
        # Si algo falla, devolvemos los 9 primeros de la búsqueda vectorial
        print(f"Error en Reranking: {e}")
        return docs_k15[:9]

# 4. INTERFAZ DE TRABAJO (Mantenemos tu diseño)
st.title("🕵️ Panel de Revisión Técnica")

try:
    api = Api(AIRTABLE_KEY)
    tabla = api.table(BASE_ID, TABLE_NAME)
    registros = tabla.all(formula="{Estado} = 'Pendiente'")
    
    if not registros:
        st.success("🎉 ¡Todo al día! No hay atletas pendientes.")
    else:
        nombres = {f"{r['fields'].get('Nombre', '')} {r['fields'].get('Apellidos', '')}": r for r in registros}
        seleccion = st.selectbox("Seleccionar expediente para revisar:", ["-- Elegir --"] + list(nombres.keys()))
        
        if seleccion != "-- Elegir --":
            atleta = nombres[seleccion]
            datos = atleta['fields']
            
            if st.session_state.atleta_actual and st.session_state.atleta_actual['id'] != atleta['id']:
                st.session_state.candidatos = []
                st.session_state.img_seleccionada = None
                st.session_state.pagina_actual = 0 # Reset de página al cambiar atleta

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.write("### 📄 Relato del Atleta")
                st.info(datos.get('Descripcion', 'Sin descripción'))
                st.write(f"**Causa:** {datos.get('Causa_Discapacidad', 'N/A')}")
            with c2:
                st.write("### 🧬 Datos Estructurados")
                st.write(f"**Grupo Edad:** {datos.get('Edad_Grupo', 'N/A')}")
                st.write(f"**Extremidades afectadas:** {datos.get('Extremidades_Afecta', 'N/A')}")
                if datos.get('D_Visual'): st.error("👁️ Discapacidad Visual")
                if datos.get('D_Extremidades'): st.warning("🦾 Deficiencia Extremidades")
                if datos.get('D_Fisica'): st.success("♿ Discapacidad Física")

            if st.button("🔍 Iniciar Análisis de Perfil con IA"):
                with st.spinner("Analizando expediente completo..."):
                    st.session_state.candidatos = analizar_perfil_avanzado(datos, vectorstore)
                    st.session_state.atleta_actual = {"id": atleta['id'], "nombre": seleccion}
                    st.session_state.img_seleccionada = None
                    st.session_state.pagina_actual = 0

except Exception as e:
    st.error(f"⚠️ Error: {e}")

# 5. RESULTADOS CON NAVEGACIÓN
if st.session_state.candidatos:
    st.divider()
    
    # Calculamos qué modelos mostrar (de 3 en 3)
    inicio = st.session_state.pagina_actual * 3
    fin = inicio + 3
    seleccionados = st.session_state.candidatos[inicio:fin]

    st.subheader(f"🖼️ Perfiles LEXI Sugeridos (Opciones {inicio+1} a {min(fin, len(st.session_state.candidatos))})")
    
    cols = st.columns(3)
    for idx, doc in enumerate(seleccionados):
        img_name = doc.metadata.get('img', '')
        with cols[idx]:
            ruta = f"assets/{img_name}"
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
                st.caption(doc.page_content)
                if st.button(f"Validar Perfil {inicio + idx + 1}", key=f"btn_{img_name}"):
                    st.session_state.img_seleccionada = img_name

    # --- BOTONES DE NAVEGACIÓN ---
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.pagina_actual > 0:
            if st.button("⬅️ Ver anteriores"):
                st.session_state.pagina_actual -= 1
                st.rerun()
    with col_next:
        # Solo permite avanzar si hay más candidatos disponibles
        if fin < len(st.session_state.candidatos):
            if st.button("Ver más modelos ➡️"):
                st.session_state.pagina_actual += 1
                st.rerun()

# 6. GUARDADO FINAL (Se mantiene igual)
if st.session_state.img_seleccionada:
    img = st.session_state.img_seleccionada
    deportes = mapa_deportes.get(img, [])
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.success(f"**Perfil elegido:** {img}")
    with col2:
        st.write("**Deportes compatibles:**")
        st.write(", ".join(deportes))
        
    if st.button("💾 Finalizar y Actualizar Airtable"):
        try:
            tabla.update(st.session_state.atleta_actual['id'], {
                "Estado": "Revisado",
                "Imagen_Final": img,
                "Deportes_Sugeridos": ", ".join(deportes)
            })
            st.success("Expediente actualizado correctamente.")
            st.session_state.candidatos = []
            st.session_state.img_seleccionada = None
            st.rerun()
        except Exception as e:
            st.error(f"Fallo al guardar: {e}")
