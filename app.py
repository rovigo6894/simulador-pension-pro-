import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# ============================================
# SISTEMA DE LICENCIAS (2 ACTIVACIONES)
# ============================================

LICENCIAS = {
    "PRO-001": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-002": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-003": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-004": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-005": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-006": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-007": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-008": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-009": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
    "PRO-010": {"expira": "2026-12-31", "activa": True, "max_usos": 2},
}

ARCHIVO_USOS = "usos_simulador.json"

def cargar_usos():
    if os.path.exists(ARCHIVO_USOS):
        with open(ARCHIVO_USOS, "r") as f:
            return json.load(f)
    return {}

def guardar_usos(usos):
    with open(ARCHIVO_USOS, "w") as f:
        json.dump(usos, f, indent=2)

def verificar_licencia():
    if st.session_state.get("licencia_validada", False):
        return True
    
    usos_registrados = cargar_usos()
    
    st.sidebar.header("🔐 Acceso PRO")
    codigo = st.sidebar.text_input("Código de licencia", type="password", key="codigo_licencia")
    
    if st.sidebar.button("Activar licencia"):
        if codigo in LICENCIAS:
            if not LICENCIAS[codigo]["activa"]:
                st.sidebar.error("❌ Esta licencia fue desactivada")
                return False
            
            fecha_exp = datetime.strptime(LICENCIAS[codigo]["expira"], "%Y-%m-%d")
            if datetime.now() > fecha_exp:
                st.sidebar.error("❌ Licencia expirada")
                return False
            
            usos_actuales = usos_registrados.get(codigo, 0)
            max_usos = LICENCIAS[codigo]["max_usos"]
            
            if usos_actuales >= max_usos:
                st.sidebar.error(f"❌ Límite de {max_usos} activaciones alcanzado")
                return False
            
            usos_registrados[codigo] = usos_actuales + 1
            guardar_usos(usos_registrados)
            
            st.session_state.licencia_validada = True
            st.session_state.codigo_usado = codigo
            st.sidebar.success(f"✅ Activada ({usos_actuales + 1}/{max_usos})")
            st.rerun()
        else:
            st.sidebar.error("❌ Código inválido")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💳 [Comprar licencia](https://wa.me/5218715791810)")
    st.warning("🔒 Versión PRO bloqueada. Ingresa un código válido en la barra lateral.")
    return False

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(page_title="OptiPensión 73 - PRO", layout="centered")

if not verificar_licencia():
    st.stop()

# Ocultar menús de Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Título con marca
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='color: #0066b3; font-size: 3rem; margin-bottom: 0;'>💰 OPTIPENSIÓN 73</h1>
    <p style='color: #666; font-size: 1.2rem;'>Optimización Integral de Pensiones · Ley 73</p>
    <p style='color: #888;'>Ing. Roberto Villarreal · Plan Maestro 2026</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================
# FUNCIONES DE CÁLCULO CORREGIDAS
# ============================================

def calcular_pension(semanas, salario, edad_actual, edad_retiro, esposa=True):
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    FACTOR_EDAD = FACTOR_POR_EDAD.get(edad_retiro, 0.75)
    
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    AJUSTE_FINAL = 1.2166
    
    años_para_retiro = max(0, edad_retiro - edad_actual)
    semanas_60 = semanas + (52 * años_para_retiro)
    
    cuantia_basica_diaria = salario * PCT_CUANTIA
    cuantia_basica_anual = cuantia_basica_diaria * 365
    
    incremento_diario = salario * PCT_INCREMENTO
    años_despues_500 = max(0, (semanas_60 - 500) / 52)
    incrementos_anuales = incremento_diario * 365 * años_despues_500
    
    cuantia_total_anual = cuantia_basica_anual + incrementos_anuales
    asignacion_anual = cuantia_total_anual * PCT_ESPOSA
    total_con_asignacion = cuantia_total_anual + asignacion_anual
    decreto_fox = total_con_asignacion * DECRETO_FOX
    cuantia_base_total = total_con_asignacion + decreto_fox
    
    # Ajuste final (factor empírico calibrado)
    cuantia_base_total *= AJUSTE_FINAL
    
    pension_anual = cuantia_base_total * FACTOR_EDAD
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'anual': round(pension_anual, 2),
        'semanas_60': round(semanas_60, 0),
        'factor_edad': FACTOR_EDAD
    }

def calcular_mod40(semanas, salario, edad_actual, edad_retiro, salario_m40, meses_m40, esposa=True):
    años_para_retiro = max(0, edad_retiro - edad_actual)
    
    factores = {1: 0.13347, 2: 0.14438, 3: 0.15529, 4: 0.1662}
    
    meses_por_año = 30.4
    inversion = 0
    meses_restantes = meses_m40
    
    for año in range(1, 5):
        if meses_restantes <= 0:
            break
        meses_en_año = min(12, meses_restantes)
        inversion += salario_m40 * meses_en_año * meses_por_año * factores.get(año, 0.13347)
        meses_restantes -= meses_en_año
    
    semanas_m40 = (meses_m40 / 12) * 52
    semanas_totales = semanas + (52 * años_para_retiro) + semanas_m40
    
    if meses_m40 >= 6:
        semanas_ponderadas = min(semanas_m40, 250)
        semanas_previas = 250 - semanas_ponderadas
        nuevo_promedio = ((salario * semanas_previas) + (salario_m40 * semanas_ponderadas)) / 250 if semanas_previas > 0 else salario_m40
    else:
        nuevo_promedio = salario
    
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    FACTOR_EDAD = FACTOR_POR_EDAD.get(edad_retiro, 0.75)
    
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    AJUSTE_FINAL = 1.2166
    
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    
    pension_anual = (
        ((nuevo_promedio * PCT_CUANTIA * 365) +
         (nuevo_promedio * PCT_INCREMENTO * 365 * años_despues_500)) *
        (1 + PCT_ESPOSA) * (1 + DECRETO_FOX) * FACTOR_EDAD * AJUSTE_FINAL
    )
    
    pension_mensual = pension_anual / 12
    base = calcular_pension(semanas, salario, edad_actual, edad_retiro, esposa)
    incremento = pension_mensual - base['mensual']
    
    return {
        'base': base['mensual'],
        'con_m40': round(pension_mensual, 2),
        'incremento': round(incremento, 2),
        'inversion': round(inversion, 2),
        'recuperacion_meses': round(inversion / max(1, incremento), 1),
        'utilidad_20': round((incremento * 12 * 20) - inversion, 2),
        'roi': round(((incremento * 12 * 20) / inversion) * 100, 0) if inversion > 0 else 0,
        'nuevo_promedio': round(nuevo_promedio, 2)
    }

# ============================================
# PESTAÑAS
# ============================================

tab1, tab2, tab3 = st.tabs(["📋 Calculadora Base", "📈 Modalidad 40", "📊 Comparativa"])

# ========== PESTAÑA 1: CALCULADORA BASE ==========
with tab1:
    st.subheader("Datos personales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_actual = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad1")
        semanas_hoy = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1159, step=1, key="sem1")
        salario_promedio = st.number_input("Salario diario ($)", min_value=0.0, max_value=10000.0, value=960.0, step=10.0, key="sal1")
    
    with col2:
        edad_retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65], index=0, key="retiro1")
        asignacion_esposa = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa1")
        inflacion = st.slider("Inflación estimada anual (%)", 0.0, 10.0, 4.0, key="inf1") / 100
    
    if st.button("Calcular pensión base", type="primary", use_container_width=True, key="btn1"):
        with st.spinner("Calculando..."):
            base = calcular_pension(semanas_hoy, salario_promedio, edad_actual, edad_retiro, asignacion_esposa)
            
            st.divider()
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            with col_r2:
                st.markdown(f"""
                <div style='background-color: #0066b3; padding: 20px; border-radius: 10px; text-align: center; color: white'>
                    <h2 style='color: white; margin:0'>PENSIÓN MENSUAL</h2>
                    <h1 style='color: white; font-size: 48px; margin:10px'>${base['mensual']:,.0f}</h1>
                    <p style='color: #e0e0e0; margin:0'>Retiro a los {edad_retiro} años</p>
                    <p style='color: #e0e0e0; margin:0; font-size: 12px;'>Semanas totales: {base['semanas_60']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)

# ========== PESTAÑA 2: MODALIDAD 40 ==========
with tab2:
    st.subheader("Análisis de Modalidad 40")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_m40 = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad2")
        semanas_m40 = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1159, step=1, key="sem2")
        salario_actual = st.number_input("Salario actual ($)", min_value=0.0, max_value=10000.0, value=960.0, step=10.0, key="sal2")
    
    with col2:
        edad_retiro2 = st.selectbox("Edad de retiro", [60,61,62,63,64,65], index=0, key="retiro2")
        esposa2 = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa2")
        salario_m40 = st.number_input("Salario M40 ($)", min_value=0.0, max_value=20000.0, value=2932.0, step=100.0, key="sal_m40")
        meses_m40 = st.selectbox("Meses en M40", [6,12,18,24,30,36,42,48], index=5, key="meses")
    
    if st.button("Calcular Modalidad 40", type="primary", use_container_width=True, key="btn2"):
        with st.spinner("Analizando..."):
            res = calcular_mod40(semanas_m40, salario_actual, edad_m40, edad_retiro2, salario_m40, meses_m40, esposa2)
            
            st.divider()
            
            st.markdown(f"""
            <div style='background-color: #00a86b; padding: 15px; border-radius: 10px; text-align: center; color: white; margin: 15px 0;'>
                <h2 style='color: white; margin:0'>💰 INCREMENTO MENSUAL: ${res['incremento']:,.0f}</h2>
                <p style='color: #e0e0e0;'>Tu pensión aumentaría con Modalidad 40</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.metric("Pensión base", f"${res['base']:,.0f}")
            with col_c2:
                st.metric("Pensión con M40", f"${res['con_m40']:,.0f}")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Inversión total", f"${res['inversion']:,.0f}")
            with col_m2:
                st.metric("Recuperación", f"{res['recuperacion_meses']:.0f} meses")
            with col_m3:
                st.metric("ROI", f"{res['roi']}%")
            
            st.info(f"💰 Utilidad a 20 años: ${res['utilidad_20']:,.0f}")

# ========== PESTAÑA 3: COMPARATIVA ==========
with tab3:
    st.subheader("Comparativa de escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_comp = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad3")
        semanas_comp = st.number_input("Semanas", min_value=0, max_value=3000, value=1159, step=1, key="sem3")
        salario_comp = st.number_input("Salario", min_value=0.0, max_value=10000.0, value=960.0, step=10.0, key="sal3")
    
    with col2:
        edad_retiro3 = st.selectbox("Edad retiro", [60,61,62,63,64,65], index=0, key="retiro3")
        esposa3 = st.checkbox("¿Con asignación?", value=True, key="esposa3")
        salario_tope = st.number_input("Salario M40", min_value=0.0, max_value=20000.0, value=2932.0, step=100.0, key="tope3")
    
    if st.button("Comparar escenarios", type="primary", use_container_width=True, key="btn3"):
        with st.spinner("Generando comparativa..."):
            
            base = calcular_pension(semanas_comp, salario_comp, edad_comp, edad_retiro3, esposa3)
            pension_base = base['mensual']
            
            meses_lista = [6,12,18,24,30,36,42,48]
            pensiones_con_m40 = []
            
            for meses in meses_lista:
                r = calcular_mod40(semanas_comp, salario_comp, edad_comp, edad_retiro3, salario_tope, meses, esposa3)
                pensiones_con_m40.append(r['con_m40'])
            
            st.divider()
            
            # Gráfica
            fig = go.Figure(data=[
                go.Bar(name='Sin M40', x=[f"{m}m" for m in meses_lista], 
                       y=[pension_base]*8, marker_color='#94a3b8'),
                go.Bar(name='Con M40', x=[f"{m}m" for m in meses_lista], 
                       y=pensiones_con_m40, marker_color='#0066b3')
            ])
            
            fig.update_layout(
                barmode='group',
                title="Comparación: Base vs Modalidad 40",
                yaxis_tickformat="$,.0f",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"💡 Pensión base: ${pension_base:,.0f}")

# ============================================
# PIE DE PÁGINA
# ============================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    <p>📧 contacto@optipension73.com · 📱 871 579 1810</p>
    <p>© 2026 OptiPensión 73 · Optimización Integral de Pensiones</p>
    <p>Ing. Roberto Villarreal · Plan Maestro 2028-2068</p>
</div>
""", unsafe_allow_html=True)
