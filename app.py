import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import platform
import os
import json

# ============================================
# SISTEMA DE LICENCIAS (2 MÁQUINAS)
# ============================================
def get_machine_id():
    machine_info = f"{platform.node()}-{platform.processor()}-{os.name}"
    return hashlib.md5(machine_info.encode()).hexdigest()[:10]

# Base de datos de licencias
LICENCIAS = {
    "ROBERTO-2026": {
        "expira": "2026-12-31", 
        "activa": True, 
        "max_maquinas": 2,
        "maquinas_autorizadas": []
    },
    "DEMO-2026": {
        "expira": "2026-12-31", 
        "activa": True, 
        "max_maquinas": 2,
        "maquinas_autorizadas": []
    }
}

ARCHIVO_LICENCIAS = "licencias_activas.json"

def cargar_licencias():
    if os.path.exists(ARCHIVO_LICENCIAS):
        with open(ARCHIVO_LICENCIAS, "r") as f:
            return json.load(f)
    return {}

def guardar_licencias(estado):
    with open(ARCHIVO_LICENCIAS, "w") as f:
        json.dump(estado, f, indent=2)

def verificar_licencia():
    if st.session_state.get("licencia_validada", False):
        return True
    
    machine_id = get_machine_id()
    estado_licencias = cargar_licencias()
    
    with st.sidebar:
        st.markdown("### 🔐 ACCESO PRO")
        codigo = st.text_input("Código de licencia", type="password")
        
        if st.button("Activar licencia", use_container_width=True):
            if codigo in LICENCIAS:
                licencia = LICENCIAS[codigo]
                
                if not licencia["activa"]:
                    st.error("❌ Licencia desactivada")
                    return False
                
                fecha_exp = datetime.strptime(licencia["expira"], "%Y-%m-%d")
                if datetime.now() > fecha_exp:
                    st.error("❌ Licencia expirada")
                    return False
                
                maquinas = estado_licencias.get(codigo, [])
                
                if machine_id in maquinas:
                    st.session_state.licencia_validada = True
                    st.session_state.codigo_usado = codigo
                    st.success("✅ Acceso concedido")
                    st.rerun()
                    return True
                
                if len(maquinas) < licencia["max_maquinas"]:
                    maquinas.append(machine_id)
                    estado_licencias[codigo] = maquinas
                    guardar_licencias(estado_licencias)
                    st.session_state.licencia_validada = True
                    st.session_state.codigo_usado = codigo
                    st.success(f"✅ Máquina registrada ({len(maquinas)}/{licencia['max_maquinas']})")
                    st.rerun()
                    return True
                else:
                    st.error(f"❌ Límite de {licencia['max_maquinas']} máquinas alcanzado")
                    return False
            else:
                st.error("❌ Código inválido")
        
        st.markdown("---")
        st.markdown("💳 [Comprar licencia](https://wa.me/5218715791810)")
        
    st.warning("🔒 Versión PRO bloqueada. Ingresa un código válido en la barra lateral.")
    return False

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="💰 Simulador Pensión PRO · OptiPensión 73",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Verificar licencia
if not verificar_licencia():
    st.stop()

# Ocultar menús de Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            button[data-testid="collapsed-control"] {
                display: none !important;
            }
            
            section[data-testid="stSidebar"] {
                width: 25rem !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# CSS PROFESIONAL
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(145deg, #0b1c26 0%, #1a2f3a 50%, #0f2a35 100%);
    }
    
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 50%, #bae6fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        font-size: 1rem;
        color: #94a3b8;
    }
    
    .badge-pro {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.2rem 1rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    
    .input-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 2rem;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 35px -15px #000000;
    }
    
    .result-card {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 2rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-number {
        color: white;
        font-size: 4rem;
        font-weight: 800;
        line-height: 1.2;
    }
    
    .result-label {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .result-detail {
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .legal-notice {
        background: rgba(0,0,0,0.3);
        border-radius: 1rem;
        padding: 1rem;
        margin: 2rem 0;
        font-size: 0.7rem;
        color: #94a3b8;
        text-align: center;
    }
    
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(148,163,184,0.2);
    }
    
    .footer a {
        color: #94a3b8;
        text-decoration: none;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.3s !important;
        margin: 1rem 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -8px #1e3a8a !important;
    }
    
    .stNumberInput > div > div {
        border-radius: 1rem !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .stSlider > div > div {
        color: #3b82f6 !important;
    }
    
    .stCheckbox > div > div {
        color: white !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 1rem !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO
# ============================================
st.markdown("""
<div class="title-container">
    <div class="main-title">
        Simulador de Pensión 
        <span class="badge-pro">PRO</span>
    </div>
    <div class="sub-title">Ing. Roberto Villarreal · Ley 73 · Modalidad 40</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCIÓN DE CÁLCULO EXACTA LEY 73
# ============================================
def calcular_pension_exacta(edad, semanas, salario, retiro, esposa):
    """
    Cálculo EXACTO según Ley 73 del IMSS
    """
    
    # Factor por edad (Artículo 167 Ley 73)
    factores = {60: 0.75, 61: 0.80, 62: 0.85, 63: 0.90, 64: 0.95, 65: 1.00}
    factor_edad = factores[retiro]
    
    # Cuantía básica (13% del salario)
    cuantia_basica_diaria = salario * 0.13
    cuantia_basica_anual = cuantia_basica_diaria * 365
    
    # Incremento por años adicionales (2.45% por año después de 500 semanas)
    años_para_retiro = max(0, retiro - edad)
    semanas_totales = semanas + (52 * años_para_retiro)
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    incremento_diario = salario * 0.0245
    incremento_anual = incremento_diario * 365 * años_despues_500
    
    # Cuantía total
    cuantia_total_anual = cuantia_basica_anual + incremento_anual
    
    # Asignación por esposa (15% si aplica)
    if esposa:
        cuantia_total_anual *= 1.15
    
    # Decreto Fox (11% adicional)
    cuantia_total_anual *= 1.11
    
    # Factor de ajuste (21.66% según tablas IMSS)
    cuantia_total_anual *= 1.2166
    
    # Aplicar factor por edad
    pension_anual = cuantia_total_anual * factor_edad
    
    # Pensión mensual
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_edad': factor_edad
    }

# ============================================
# DATOS DE ENTRADA
# ============================================
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.subheader("📋 Datos personales")

col1, col2 = st.columns(2)

with col1:
    edad = st.slider("Edad actual", 40, 65, 55)
    semanas = st.number_input("Semanas cotizadas", 0, 3000, 1315, step=50)

with col2:
    salario = st.number_input("Salario diario ($)", 0.0, 5000.0, 1010.0, step=10.0)
    retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65])

esposa = st.checkbox("Con asignación por esposa", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BOTÓN Y RESULTADO
# ============================================
if st.button("🔮 CALCULAR PENSIÓN", use_container_width=True):
    # Usar la función exacta
    resultado = calcular_pension_exacta(edad, semanas, salario, retiro, esposa)
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PENSIÓN MENSUAL</div>
        <div class="result-number">${resultado['mensual']:,.0f}</div>
        <div class="result-detail">
            Factor: {resultado['factor_edad']*100:.0f}% · Semanas totales: {resultado['semanas_totales']:.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# AVISO LEGAL
# ============================================
st.markdown("""
<div class="legal-notice">
    ⚖️ <strong>AVISO IMPORTANTE:</strong> Este cálculo es una simulación basada en la Ley 73 del IMSS 
    y no constituye un dictamen oficial. Consulte con un especialista para un diagnóstico personalizado.
</div>
""", unsafe_allow_html=True)

# ============================================
# WHATSAPP EN SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 📲 ¿Necesitas ayuda?")
    st.markdown("""
    <a href="https://wa.me/5218715791810" target="_blank">
        <button style="background:#25D366; color:white; padding:10px; border-radius:2rem; width:100%; border:none; font-weight:600; cursor:pointer;">
            📲 CONTACTAR POR WHATSAPP
        </button>
    </a>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Información de la licencia
    if 'codigo_usado' in st.session_state:
        st.info(f"✅ Licencia activa: {st.session_state.codigo_usado}")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>📧 contacto@optipension73.com · 📱 871 579 1810</p>
    <p>🔒 Versión PROFESIONAL · Cálculos exactos Ley 73</p>
    <p>
        <a href="#">Aviso de Privacidad</a> · 
        <a href="#">Términos y Condiciones</a>
    </p>
    <p>© 2026 · OptiPensión 73</p>
</div>
""", unsafe_allow_html=True)
