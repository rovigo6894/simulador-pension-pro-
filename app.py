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
    layout="wide",
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
        font-size: 3rem;
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
    
    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 15px 30px -12px #000000;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 25px 40px -15px #000000;
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
        color: white;
        line-height: 1.2;
    }
    
    .chart-container {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 2rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 35px -15px #000000;
    }
    
    .result-box {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 2rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-number {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
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
        margin-top: 3rem;
        padding-top: 2rem;
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
        width: 100% !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 1rem !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    
    .stNumberInput > div > div {
        border-radius: 1rem !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
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
    <div class="main-title">
        Simulador de Pensión 
        <span class="badge-pro">PRO</span>
    </div>
    <div class="sub-title">Ing. Roberto Villarreal · Ley 73 · Modalidad 40</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CÁLCULO
# ============================================
def calcular_pension(edad, semanas, salario, retiro, esposa=True):
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

def calcular_mod40(edad, semanas, salario, retiro, salario_m40, meses_m40, esposa=True):
    factores_costo = {1: 0.13347, 2: 0.14438, 3: 0.15529, 4: 0.1662}
    meses_por_año = 30.4
    
    inversion = 0
    meses_restantes = meses_m40
    
    for año in range(1, 5):
        if meses_restantes <= 0:
            break
        meses_en_año = min(12, meses_restantes)
        inversion += salario_m40 * meses_en_año * meses_por_año * factores_costo.get(año, 0.13347)
        meses_restantes -= meses_en_año
    
    semanas_m40 = (meses_m40 / 12) * 52
    años_para_retiro = max(0, retiro - edad)
    
    if meses_m40 >= 6:
        semanas_ponderadas = min(semanas_m40, 250)
        semanas_previas = 250 - semanas_ponderadas
        nuevo_promedio = ((salario * semanas_previas) + (salario_m40 * semanas_ponderadas)) / 250 if semanas_previas > 0 else salario_m40
    else:
        nuevo_promedio = salario
    
    base = calcular_pension(edad, semanas, salario, retiro, esposa)
    
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    factor_edad = FACTOR_POR_EDAD.get(retiro, 0.75)
    
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    AJUSTE_FINAL = 1.2166
    
    semanas_totales = semanas + (52 * años_para_retiro) + semanas_m40
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    
    pension_anual = (
        ((nuevo_promedio * PCT_CUANTIA * 365) +
         (nuevo_promedio * PCT_INCREMENTO * 365 * años_despues_500)) *
        (1 + PCT_ESPOSA) * (1 + DECRETO_FOX) * factor_edad * AJUSTE_FINAL
    )
    
    pension_mensual = pension_anual / 12
    incremento = pension_mensual - base['mensual']
    
    recuperacion_meses = inversion / incremento if incremento > 0 else float('inf')
    utilidad_20 = (incremento * 12 * 20) - inversion
    roi = ((incremento * 12 * 20) / inversion * 100) if inversion > 0 else 0
    
    return {
        'base': base['mensual'],
        'con_m40': round(pension_mensual, 2),
        'incremento': round(incremento, 2),
        'inversion': round(inversion, 2),
        'recuperacion': round(recuperacion_meses, 1),
        'utilidad_20': round(utilidad_20, 2),
        'roi': round(roi, 0),
        'nuevo_promedio': round(nuevo_promedio, 2)
    }

# ============================================
# PESTAÑAS PRINCIPALES
# ============================================
tab1, tab2, tab3 = st.tabs([
    "📊 CALCULADORA BASE",
    "📈 MODALIDAD 40",
    "📉 COMPARATIVA"
])

# ============================================
# PESTAÑA 1: CALCULADORA BASE
# ============================================
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📋 Datos personales")
        
        edad = st.slider("Edad actual", 40, 65, 55)
        semanas = st.number_input("Semanas cotizadas", 0, 3000, 1315, step=50)
        salario = st.number_input("Salario diario ($)", 0.0, 5000.0, 1010.0, step=50.0)
        retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65])
        esposa = st.checkbox("Con asignación por esposa", True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Resultado")
        
        if st.button("🔮 CALCULAR PENSIÓN", use_container_width=True):
            res = calcular_pension(edad, semanas, salario, retiro, esposa)
            
            st.markdown(f"""
            <div class="result-box">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">PENSIÓN MENSUAL</div>
                <div class="result-number">${res['mensual']:,.0f}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;">
                    Factor: {res['factor_edad']*100:.0f}% · Semanas: {res['semanas_totales']:.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PESTAÑA 2: MODALIDAD 40
# ============================================
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📋 Parámetros M40")
        
        edad_m40 = st.number_input("Edad actual", 40, 65, 55, key="m40_edad")
        semanas_m40 = st.number_input("Semanas", 0, 3000, 1315, key="m40_sem")
        salario_m40 = st.number_input("Salario actual", 0.0, 5000.0, 1010.0, key="m40_sal")
        salario_tope = st.number_input("Salario a cotizar en M40", 0.0, 10000.0, 2932.0)
        meses_m40 = st.selectbox("Meses en M40", [6,12,18,24,30,36,42,48])
        retiro_m40 = st.selectbox("Edad de retiro", [60,61,62,63,64,65], key="m40_retiro")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Análisis M40")
        
        if st.button("📊 ANALIZAR MODALIDAD 40", use_container_width=True):
            res = calcular_mod40(edad_m40, semanas_m40, salario_m40, retiro_m40, 
                                salario_tope, meses_m40, True)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Incremento", f"${res['incremento']:,.0f}")
                st.metric("Inversión", f"${res['inversion']:,.0f}")
                st.metric("Recuperación", f"{res['recuperacion']} meses")
            
            with col_b:
                st.metric("Pensión base", f"${res['base']:,.0f}")
                st.metric("Pensión M40", f"${res['con_m40']:,.0f}")
                st.metric("ROI", f"{res['roi']}%")
            
            st.info(f"💰 Utilidad a 20 años: ${res['utilidad_20']:,.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PESTAÑA 3: COMPARATIVA
# ============================================
with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Comparativa de Escenarios")
    
    meses_lista = [6,12,18,24,30,36,42,48]
    pension_base = 23030
    pensiones_m40 = [23800, 24600, 25400, 26200, 27000, 27800, 28600, 29400]
    
    fig = go.Figure(data=[
        go.Bar(name='Pensión Base', x=[f"{m}m" for m in meses_lista], 
               y=[pension_base]*8, marker_color='#94a3b8'),
        go.Bar(name='Con M40', x=[f"{m}m" for m in meses_lista], 
               y=pensiones_m40, marker_color='#3b82f6')
    ])
    
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8',
        yaxis_tickformat='$,.0f',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
