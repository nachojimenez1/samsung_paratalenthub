import streamlit as st
import os
from dotenv import load_dotenv
from pyairtable import Api
from datetime import date

# 1. CONFIGURACIÓN
load_dotenv()
AIRTABLE_KEY = os.getenv("AIRTABLE_API_KEY", "").replace('"', '').strip()
BASE_ID = os.getenv("AIRTABLE_BASE_ID", "").replace('"', '').strip()
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "").replace('"', '').strip()

st.set_page_config(page_title="CPE - Registro Atletas", page_icon="🏥", layout="centered")

# Estilo CPE
st.markdown("""
    <style>
    .stButton>button { background-color: #E03126; color: white; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #b3261e; color: white; }
    h1 { color: #E03126; }
    </style>
    """, unsafe_allow_html=True)

api = Api(AIRTABLE_KEY)
tabla = api.table(BASE_ID, TABLE_NAME)

if "enviado" not in st.session_state:
    st.session_state.enviado = False

if st.session_state.enviado:
    st.success("¡Datos enviados correctamente!")
    if st.button("Registrar nuevo atleta"):
        st.session_state.enviado = False
        st.rerun()
    st.stop()

st.title("🏆 Cuestionario de Detección de Talento")

with st.form("cuestionario_total"):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Privacidad", "👤 Personal", "🏫 Entorno", "🧬 Perfil Médico", "🏆 Deporte"])

    with tab1:
        st.subheader("Consentimiento")
        edad_grupo = st.radio("Selecciona tu grupo de edad:", ["Menor de 18 años", "18 años o más"])
        consentimiento = st.checkbox("Acepto el tratamiento de mis datos por el CPE")
        nacionalidad = st.radio("¿Tienes nacionalidad española?", ["Sí", "No"])

    with tab2:
        st.subheader("Datos Personales")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre")
            apellidos = st.text_input("Apellidos")
            fecha_nac = st.date_input("Fecha de nacimiento", value=date(2000, 1, 1))
        with col2:
            email = st.text_input("Correo electrónico")
            telefono = st.text_input("Teléfono")
            provincia = st.text_input("Provincia")
        direccion_completa = st.text_input("Dirección completa (Ciudad y CP)")
        isla = st.selectbox("Isla de residencia", ["No aplica", "Mallorca", "Menorca", "Ibiza", "Formentera", "Tenerife", "Gran Canaria", "Lanzarote", "Fuerteventura", "La Palma", "La Gomera", "El Hierro"])

        nombre_tutor = st.text_input("Nombre del Tutor") if edad_grupo == "Menor de 18 años" else ""
        parentesco_tutor = st.text_input("Parentesco") if edad_grupo == "Menor de 18 años" else ""

    with tab3:
        st.subheader("Entorno")
        como_conocio = st.text_input("¿Cómo has conocido el cuestionario?")
        colegio = st.text_input("Nombre del Colegio")
        asociacion_club = st.text_input("Nombre de la asociación/club")
        ffaa = st.radio("¿Perteneces a las Fuerzas Armadas o Cuerpos de Seguridad?", ["No", "Sí"])

    with tab4:
        st.subheader("Discapacidad")
        causa_discapacidad = st.text_input("Causa de la discapacidad")
        ano_inicio = st.number_input("Año de inicio:", 1950, 2026, 2020)
        descripcion = st.text_area("Describe tu discapacidad (muy importante):")
        d_visual = st.checkbox("Visual")
        d_intelectual = st.checkbox("Intelectual")
        d_fisica = st.checkbox("Física/Coordinación")
        d_extremidades = st.checkbox("Extremidades")
        extremidades_afectadas = st.text_input("Extremidades afectadas")

    with tab5:
        st.subheader("Intereses")
        deporte_interes_1 = st.text_input("Deporte principal de interés")
        deporte_interes_2 = st.text_input("Segundo deporte de interés")
        deporte_actual = st.text_input("¿Qué deporte practicas ahora?")
        tiempo_semana = st.text_input("¿Cuánto tiempo a la semana?")
        meta_alto_nivel = st.radio("¿Quieres competir al más alto nivel?", ["No", "Tal vez", "Sí"])

    enviar = st.form_submit_button("Enviar Cuestionario")

    if enviar:
        if not consentimiento:
            st.error("Debes aceptar la política de privacidad.")
        else:
            try:
                tabla.create({
                    "Nombre": nombre, "Apellidos": apellidos, "Estado": "Pendiente",
                    "Edad_Grupo": edad_grupo, "Nacionalidad": nacionalidad,
                    "Fecha_Nacimiento": str(fecha_nac), "Email": email, "Telefono": telefono,
                    "Direccion_Completa": direccion_completa, "Provincia": provincia,
                    "Nombre_Tutor": nombre_tutor, "Parentesco_Tutor": parentesco_tutor,
                    "Como_Conocio": como_conocio, "Colegio": colegio,
                    "Asociacion_Club": asociacion_club, "FFAA": ffaa,
                    "Causa_Discapacidad": causa_discapacidad, "Año_Inicio": int(ano_inicio),
                    "Descripcion": descripcion, "D_Visual": d_visual, "D_Intelectual": d_intelectual,
                    "D_Fisica": d_fisica, "D_Extremidades": d_extremidades,
                    "Extremidades_Afecta": extremidades_afectadas,
                    "Deporte_Interes_1": deporte_interes_1, "Deporte_Interes_2": deporte_interes_2,
                    "Deporte_Actual": deporte_actual, "Tiempo_Semana": tiempo_semana,
                    "Meta_Alto_Nivel": meta_alto_nivel
                })
                st.session_state.enviado = True
                st.rerun()
            except Exception as e:
                st.error(f"Error al enviar a Airtable: {e}")