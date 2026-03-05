import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="💰 Simulador Pensión PRO",
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
# CSS CHINGÓN (COMO EL DE GASTOS)
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
        animation: fadeInUp 0.6s ease-out;
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
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 1.2rem;
        box-shadow: 0 10px 25px -10px #000000;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 30px -12px #000000;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(148,163,184,0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
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
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO
# ============================================
st.markdown("""
<div class="title-container">
    <div class="main-title">Simulador de Pensión</div>
    <div class="sub-title">Ing. Roberto Villarreal · Ley 73</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE ENTRADA
# ============================================
col1, col2 = st.columns(2)

with col1:
    edad = st.slider("Edad actual", 40, 65, 55)
    semanas = st.number_input("Semanas cotizadas", 0, 3000, 1315, step=50)

with col2:
    salario = st.number_input("Salario diario promedio ($)", 0.0, 5000.0, 1010.0, step=50.0)
    retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65])

esposa = st.checkbox("Con asignación por esposa", value=True)

# ============================================
# MÉTRICAS
# ============================================
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
        <div class="metric-value">{semanas}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SALARIO</div>
        <div class="metric-value">${salario:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BOTÓN
# ============================================
if st.button("CALCULAR PENSIÓN", use_container_width=True):
    # Cálculo temporal (después pondremos el real)
    pension_temp = salario * 30.4 * {60:0.75,61:0.80,62:0.85,63:0.90,64:0.95,65:1.00}[retiro] * 1.2
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); 
                border-radius: 2rem; padding: 2rem; text-align: center; margin-top: 2rem;">
        <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">PENSIÓN MENSUAL ESTIMADA</div>
        <div style="color: white; font-size: 4rem; font-weight: 800; line-height: 1.2;">
            ${pension_temp:,.0f}
        </div>
        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 0.5rem;">
            Retiro a los {retiro} años
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>📧 contacto@optipension73.com · 📱 871 579 1810</p>
    <p>⚡ Versión DEMO · Cálculos aproximados</p>
    <p>© 2026 · OptiPensión 73</p>
</div>
""", unsafe_allow_html=True)
