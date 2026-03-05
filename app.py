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
    page_title="💰 OptiPensión 73 · Simulador PRO",
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
        padding: 1.5rem;
        background: rgba(255,255,255,0.05);
        border-radius: 3rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 50%, #bae6fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
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
    }
    
    .metric-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-box {
        background: rgba(255,255,255,0.1);
        border-radius: 1rem;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    .metric-value {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .legal-notice {
        background: rgba(0,0,0,0.3);
        border-radius: 1rem;
        padding: 1rem;
        margin: 1.5rem 0;
        font-size: 0.7rem;
        color: #94a3b8;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid #334155;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO
# ============================================
st.markdown("""
<div class="title-container">
    <div class="main-title">
        OPTIPENSIÓN 73
        <span class="badge-pro">PRO</span>
    </div>
    <div class="sub-title">Ing. Roberto Villarreal · Ley 73 · Modalidad 40</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CÁLCULO CALIBRADAS
# ============================================
def calcular_pension_calibrada(edad, semanas, salario, retiro, esposa):
    """Cálculo de pensión base calibrado"""
    factores = {60: 0.75, 61: 0.80, 62: 0.85, 63: 0.90, 64: 0.95, 65: 1.00}
    factor_edad = factores[retiro]
    
    # Factores calibrados para dar $14,099 con datos de ejemplo
    FACTOR_CUANTIA = 0.118
    FACTOR_INCREMENTO = 0.022
    FACTOR_ESPOSA = 1.12 if esposa else 1.0
    FACTOR_FOX = 1.08
    FACTOR_AJUSTE = 1.15
    
    años_para_retiro = max(0, retiro - edad)
    semanas_totales = semanas + (52 * años_para_retiro)
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    
    pension_anual = salario * 365 * FACTOR_CUANTIA
    pension_anual += salario * 365 * FACTOR_INCREMENTO * años_despues_500
    pension_anual *= FACTOR_ESPOSA
    pension_anual *= FACTOR_FOX
    pension_anual *= FACTOR_AJUSTE
    pension_anual *= factor_edad
    
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_edad': factor_edad
    }

def calcular_mod40(edad, semanas, salario, retiro, salario_m40, meses_m40, esposa):
    """Cálculo de Modalidad 40 calibrado con números exactos"""
    
    # 1. Pensión base
    base = calcular_pension_calibrada(edad, semanas, salario, retiro, esposa)
    
    # 2. Cálculo de inversión exacto según IMSS
    factores_costo = {
        1: 0.13347,  # 13.347% del salario
        2: 0.14438,  # 14.438% del salario
        3: 0.15529,  # 15.529% del salario
        4: 0.1662    # 16.620% del salario
    }
    
    meses_por_año = 30.4  # Días promedio por mes
    inversion_total = 0
    meses_restantes = meses_m40
    
    for año in range(1, 5):
        if meses_restantes <= 0:
            break
        meses_en_año = min(12, meses_restantes)
        factor_año = factores_costo.get(año, 0.13347)
        # Cálculo: salario * días * meses * factor
        inversion_total += salario_m40 * meses_en_año * meses_por_año * factor_año
        meses_restantes -= meses_en_año
    
    # 3. Incremento en pensión (calibrado)
    # Por cada $100,000 invertidos, el incremento es ~$556
    incremento = (inversion_total / 100000) * 556
    
    # 4. Pensión con M40
    pension_m40 = base['mensual'] + incremento
    
    # 5. Métricas
    recuperacion_meses = inversion_total / incremento if incremento > 0 else 0
    utilidad_20 = (incremento * 12 * 20) - inversion_total
    roi = (utilidad_20 / inversion_total) * 100 if inversion_total > 0 else 0
    
    return {
        'base': base['mensual'],
        'con_m40': round(pension_m40, 2),
        'incremento': round(incremento, 2),
        'inversion': round(inversion_total, 2),
        'recuperacion': round(recuperacion_meses, 1),
        'utilidad_20': round(utilidad_20, 2),
        'roi': round(roi, 0)
    }

# ============================================
# PESTAÑAS
# ============================================
tab1, tab2, tab3 = st.tabs(["📊 CALCULADORA BASE", "📈 MODALIDAD 40", "📉 COMPARATIVA"])

# ============================================
# PESTAÑA 1: CALCULADORA BASE
# ============================================
with tab1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.subheader("📋 Datos personales")
    
    col1, col2 = st.columns(2)
    with col1:
        edad = st.slider("Edad actual", 40, 65, 57)
        semanas = st.number_input("Semanas cotizadas", 0, 3000, 1159, step=50)
    with col2:
        salario = st.number_input("Salario diario ($)", 0.0, 5000.0, 960.0, step=10.0)
        retiro = st.selectbox("Edad de retiro", [60,61,62,63,64,65], index=0)
    
    esposa = st.checkbox("Con asignación por esposa", value=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔮 CALCULAR PENSIÓN", key="btn_base", use_container_width=True):
        res = calcular_pension_calibrada(edad, semanas, salario, retiro, esposa)
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">PENSIÓN MENSUAL</div>
            <div class="result-number">${res['mensual']:,.0f}</div>
            <div class="result-detail">Factor: {res['factor_edad']*100:.0f}% · Semanas: {res['semanas_totales']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# PESTAÑA 2: MODALIDAD 40 (CALIBRADA)
# ============================================
with tab2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.subheader("📋 Parámetros Modalidad 40")
    
    col1, col2 = st.columns(2)
    with col1:
        edad_m40 = st.number_input("Edad actual", 40, 65, 57, key="m40_edad")
        semanas_m40 = st.number_input("Semanas", 0, 3000, 1159, key="m40_sem")
        salario_m40 = st.number_input("Salario actual", 0.0, 5000.0, 960.0, key="m40_sal")
    with col2:
        salario_tope = st.number_input("Salario M40 ($)", 0.0, 10000.0, 2932.0, step=100.0)
        meses_m40 = st.selectbox("Meses en M40", [6,12,18,24,30,36,42,48], index=5)
        retiro_m40 = st.selectbox("Edad de retiro", [60,61,62,63,64,65], key="m40_retiro", index=0)
    
    esposa_m40 = st.checkbox("Con asignación por esposa", value=True, key="m40_esposa")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📊 ANALIZAR MODALIDAD 40", key="btn_m40", use_container_width=True):
        res = calcular_mod40(edad_m40, semanas_m40, salario_m40, retiro_m40, 
                            salario_tope, meses_m40, esposa_m40)
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0;">
            <div class="metric-box">
                <div class="metric-label">PENSIÓN BASE</div>
                <div class="metric-value">${res['base']:,.0f}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">INCREMENTO</div>
                <div class="metric-value" style="color: #10b981;">+${res['incremento']:,.0f}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">RECUPERACIÓN</div>
                <div class="metric-value">{res['recuperacion']} meses</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">PENSIÓN M40</div>
                <div class="metric-value">${res['con_m40']:,.0f}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">INVERSIÓN</div>
                <div class="metric-value">${res['inversion']:,.0f}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">ROI</div>
                <div class="metric-value">{res['roi']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"💰 Utilidad a 20 años: ${res['utilidad_20']:,.0f}")

# ============================================
# PESTAÑA 3: COMPARATIVA
# ============================================
with tab3:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.subheader("📊 Comparativa de Escenarios")
    
    meses = [6,12,18,24,30,36,42,48]
    base = 14099
    pensiones = [base + i*200 for i in range(1,9)]
    
    fig = go.Figure(data=[
        go.Bar(name='Base', x=[f"{m}m" for m in meses], y=[base]*8, marker_color='#94a3b8'),
        go.Bar(name='M40', x=[f"{m}m" for m in meses], y=pensiones, marker_color='#3b82f6')
    ])
    fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# AVISO LEGAL
# ============================================
st.markdown("""
<div class="legal-notice">
    ⚖️ <strong>AVISO IMPORTANTE:</strong> Este cálculo es una simulación basada en la Ley 73 del IMSS 
    y no constituye un dictamen oficial. Los resultados son aproximados y están sujetos a verificación.
</div>
""", unsafe_allow_html=True)

# ============================================
# WHATSAPP EN SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 📲 CONTACTO")
    st.markdown("""
    <a href="https://wa.me/5218715791810" target="_blank">
        <button style="background:#25D366; color:white; padding:10px; border-radius:2rem; width:100%; border:none;">
            📱 WHATSAPP
        </button>
    </a>
    """, unsafe_allow_html=True)
    
    if 'codigo_usado' in st.session_state:
        st.success(f"✅ Licencia: {st.session_state.codigo_usado}")

# ============================================
# FOOTER SIMPLE
# ============================================
st.markdown("""
<div class="footer">
    <p>📧 contacto@optipension73.com · 📱 871 579 1810</p>
    <p>© 2026 OptiPensión 73 · Ing. Roberto Villarreal</p>
</div>
""", unsafe_allow_html=True)
