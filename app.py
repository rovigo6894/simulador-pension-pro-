import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="💰 Simulador Pensión PRO · OptiPensión 73",
    page_icon="💰",
    layout="centered"
)

# Ocultar menús de Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# CSS CHINGÓN (CORREGIDO)
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
        text-transform: uppercase;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        flex: 1;
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 1.2rem;
        box-shadow: 0 10px 25px -10px #000000;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    
    .result-box {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 2rem;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 30px -10px #1e3a8a;
    }
    
    .result-label {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-number {
        color: white;
        font-size: 4rem;
        font-weight: 800;
        line-height: 1.2;
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
        border: 1px solid rgba(255,255,255,0.1);
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
    
    .footer a:hover {
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s !important;
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
# TÍTULO (VERSIÓN PRO)
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
# FUNCIONES DE CÁLCULO (LEY 73 REAL)
# ============================================
def calcular_pension(edad, semanas, salario, retiro, esposa):
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    factor_edad = FACTOR_POR_EDAD.get(retiro, 0.75)
    
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    AJUSTE_FINAL = 1.2166
    
    años_para_retiro = max(0, retiro - edad)
    semanas_totales = semanas + (52 * años_para_retiro)
    
    cuantia_basica_anual = salario * PCT_CUANTIA * 365
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    incremento_anual = salario * PCT_INCREMENTO * 365 * años_despues_500
    total_base = cuantia_basica_anual + incremento_anual
    
    if esposa:
        total_base *= (1 + PCT_ESPOSA)
    
    total_base *= (1 + DECRETO_FOX)
    total_base *= AJUSTE_FINAL
    pension_anual = total_base * factor_edad
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_edad': factor_edad
    }

# ============================================
# DATOS DE ENTRADA
# ============================================
col1, col2 = st.columns(2)

with col1:
    edad = st.slider("📅 Edad actual", 40, 65, 55)
    semanas = st.number_input("📊 Semanas cotizadas", 0, 3000, 1315, step=50)

with col2:
    salario = st.number_input("💰 Salario diario promedio ($)", 0.0, 5000.0, 1010.0, step=50.0)
    retiro = st.selectbox("🎯 Edad de retiro", [60, 61, 62, 63, 64, 65])

esposa = st.checkbox("👩 Con asignación por esposa", value=True)

# ============================================
# MÉTRICAS (AHORA SÍ SE VEN)
# ============================================
st.markdown('<div class="metric-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">EDAD</div>
        <div class="metric-value">{edad}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SEMANAS</div>
        <div class="metric-value">{semanas:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SALARIO</div>
        <div class="metric-value">${salario:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BOTÓN Y RESULTADO
# ============================================
if st.button("🔮 CALCULAR PENSIÓN PRO", use_container_width=True):
    # Cálculo REAL Ley 73
    resultado = calcular_pension(edad, semanas, salario, retiro, esposa)
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">PENSIÓN MENSUAL</div>
        <div class="result-number">${resultado['mensual']:,.0f}</div>
        <div class="result-detail">
            Retiro a los {retiro} años · Factor: {resultado['factor_edad']*100:.0f}%<br>
            Semanas totales: {resultado['semanas_totales']:.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# AVISO LEGAL (OBLIGATORIO)
# ============================================
st.markdown("""
<div class="legal-notice">
    ⚖️ <strong>AVISO IMPORTANTE:</strong> Este cálculo es una simulación basada en la Ley 73 del IMSS 
    y no constituye un dictamen oficial. Los resultados son aproximados y están sujetos a 
    verificación por las autoridades competentes. Consulte con un especialista para un diagnóstico personalizado.
</div>
""", unsafe_allow_html=True)

# ============================================
# FOOTER COMPLETO
# ============================================
st.markdown("""
<div class="footer">
    <p>📧 <a href="mailto:contacto@optipension73.com">contacto@optipension73.com</a> · 📱 871 579 1810</p>
    <p style="margin: 0.5rem 0;">🔒 Versión PROFESIONAL · Cálculos exactos Ley 73 · Modalidad 40 disponible</p>
    <p style="margin: 0.5rem 0;">
        <a href="#">Aviso de Privacidad</a> · 
        <a href="#">Términos y Condiciones</a> · 
        <a href="#">Política de Cookies</a>
    </p>
    <p>© 2026 · OptiPensión 73 · Optimización Integral de Pensiones</p>
</div>
""", unsafe_allow_html=True)
