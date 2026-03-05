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
    "PRO-001": {"expira": "2026-12-31", "activa": True, "max_usos": 10},
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
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================
# FUNCIÓN DE CÁLCULO BASE
# ============================================

def calcular_pension_base(semanas, salario_promedio, edad_actual, edad_retiro, esposa=True):
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    FACTOR_EDAD = FACTOR_POR_EDAD.get(edad_retiro, 0.75)
    
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    
    años_para_retiro = max(0, edad_retiro - edad_actual)
    semanas_totales = semanas + (52 * años_para_retiro)
    
    cuantia_basica_diaria = salario_promedio * PCT_CUANTIA
    cuantia_basica_anual = cuantia_basica_diaria * 365
    
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    incremento_diario = salario_promedio * PCT_INCREMENTO
    incremento_anual = incremento_diario * 365 * años_despues_500
    
    cuantia_total_anual = cuantia_basica_anual + incremento_anual
    asignacion_esposa = cuantia_total_anual * PCT_ESPOSA
    total_con_esposa = cuantia_total_anual + asignacion_esposa
    decreto_fox = total_con_esposa * DECRETO_FOX
    cuantia_base_total = total_con_esposa + decreto_fox
    
    pension_anual = cuantia_base_total * FACTOR_EDAD
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'anual': round(pension_anual, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_edad': FACTOR_EDAD
    }

# ============================================
# FUNCIÓN DE MODALIDAD 40 CON INPC
# ============================================

def calcular_mod40(semanas, salario_actual, edad_actual, edad_retiro, salario_m40, meses_m40, esposa=True, inpc=0.042):
    """
    Cálculo completo de Modalidad 40 con proyección a 2029
    """
    
    # 1. Pensión base sin M40
    base = calcular_pension_base(semanas, salario_actual, edad_actual, edad_retiro, esposa)
    
    # 2. Cálculo de la inversión en M40
    factores_m40 = {1: 0.13347, 2: 0.14438, 3: 0.15529, 4: 0.1662}
    meses_por_año = 30.4
    años_para_retiro = max(0, edad_retiro - edad_actual)
    
    inversion = 0
    meses_restantes = meses_m40
    
    for año in range(1, 5):
        if meses_restantes <= 0:
            break
        meses_en_año = min(12, meses_restantes)
        factor = factores_m40.get(año, 0.13347)
        inversion += salario_m40 * meses_en_año * meses_por_año * factor
        meses_restantes -= meses_en_año
    
    semanas_m40 = (meses_m40 / 12) * 52
    
    # Nuevo salario promedio
    if meses_m40 >= 6:
        semanas_ponderadas = min(semanas_m40, 250)
        semanas_previas = 250 - semanas_ponderadas
        if semanas_previas > 0:
            nuevo_promedio = ((salario_actual * semanas_previas) + (salario_m40 * semanas_ponderadas)) / 250
        else:
            nuevo_promedio = salario_m40
    else:
        nuevo_promedio = salario_actual
    
    # Nuevas semanas totales
    semanas_totales = semanas + (52 * años_para_retiro) + semanas_m40
    
    # Calcular nueva pensión con M40
    PCT_CUANTIA = 0.13
    PCT_INCREMENTO = 0.0245
    PCT_ESPOSA = 0.15 if esposa else 0
    DECRETO_FOX = 0.11
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    FACTOR_EDAD = FACTOR_POR_EDAD.get(edad_retiro, 0.75)
    
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    
    cuantia_basica_anual = nuevo_promedio * PCT_CUANTIA * 365
    incremento_anual = nuevo_promedio * PCT_INCREMENTO * 365 * años_despues_500
    cuantia_total_anual = cuantia_basica_anual + incremento_anual
    
    if esposa:
        cuantia_total_anual *= (1 + PCT_ESPOSA)
    
    cuantia_total_anual *= (1 + DECRETO_FOX)
    pension_anual = cuantia_total_anual * FACTOR_EDAD
    pension_mensual = pension_anual / 12
    
    # Proyección a 2029 con INPC
    años_a_2029 = max(0, 2029 - datetime.now().year)
    factor_inpc_2029 = (1 + inpc) ** años_a_2029
    
    pension_mensual_2029 = pension_mensual * factor_inpc_2029
    base_2029 = base['mensual'] * factor_inpc_2029
    incremento_2029 = pension_mensual_2029 - base_2029
    
    incremento = pension_mensual - base['mensual']
    recuperacion_meses = inversion / incremento if incremento > 0 else float('inf')
    utilidad_20 = (incremento * 12 * 20) - inversion
    roi = (utilidad_20 / inversion * 100) if inversion > 0 else 0
    
    return {
        'base': base['mensual'],
        'base_2029': round(base_2029, 2),
        'con_m40': round(pension_mensual, 2),
        'con_m40_2029': round(pension_mensual_2029, 2),
        'incremento': round(incremento, 2),
        'incremento_2029': round(incremento_2029, 2),
        'inversion': round(inversion, 2),
        'recuperacion': round(recuperacion_meses, 1),
        'utilidad_20': round(utilidad_20, 2),
        'roi': round(roi, 0),
        'nuevo_promedio': round(nuevo_promedio, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_inpc': round(factor_inpc_2029, 3)
    }

# ============================================
# PESTAÑAS
# ============================================

tab1, tab2, tab3 = st.tabs(["📋 CALCULADORA BASE", "📈 MODALIDAD 40", "📊 COMPARATIVA"])

# ========== PESTAÑA 1: CALCULADORA BASE CON INPC ==========
with tab1:
    st.subheader("📋 Datos personales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_actual = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad1")
        semanas_hoy = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1315, step=1, key="sem1")
        salario_promedio = st.number_input("Salario promedio ($)", min_value=0.0, max_value=10000.0, value=965.25, step=10.0, key="sal1")
    
    with col2:
        edad_retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65], index=0, key="retiro1")
        asignacion_esposa = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa1")
        inpc = st.slider("INPC estimado anual (%)", 2.0, 6.0, 4.2, 0.1, key="inpc1") / 100
    
    if st.button("Calcular pensión base", type="primary", use_container_width=True, key="btn1"):
        with st.spinner("Calculando..."):
            base = calcular_pension_base(semanas_hoy, salario_promedio, edad_actual, edad_retiro, asignacion_esposa)
            
            años_a_2029 = max(0, 2029 - datetime.now().year)
            factor_inpc = (1 + inpc) ** años_a_2029
            pension_2029 = base['mensual'] * factor_inpc
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style='background-color: #0066b3; padding: 20px; border-radius: 10px; text-align: center; color: white'>
                    <h2 style='color: white; margin:0'>PENSIÓN HOY</h2>
                    <h1 style='color: white; font-size: 36px; margin:10px'>${base['mensual']:,.0f}</h1>
                    <p style='color: #e0e0e0; margin:0'>Valor presente</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background-color: #00a86b; padding: 20px; border-radius: 10px; text-align: center; color: white'>
                    <h2 style='color: white; margin:0'>PENSIÓN 2029</h2>
                    <h1 style='color: white; font-size: 36px; margin:10px'>${pension_2029:,.0f}</h1>
                    <p style='color: #e0e0e0; margin:0'>Con INPC {inpc*100:.1f}% anual</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.info(f"📈 **Factor INPC:** {factor_inpc:.2f}x · Para mantener poder adquisitivo en 2029")

# ========== PESTAÑA 2: MODALIDAD 40 CON INPC ==========
with tab2:
    st.subheader("📈 Análisis de Modalidad 40")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_m40 = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad2")
        semanas_m40 = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1159, step=1, key="sem2")
        salario_actual = st.number_input("Salario actual ($)", min_value=0.0, max_value=10000.0, value=960.0, step=10.0, key="sal2")
    
    with col2:
        edad_retiro2 = st.selectbox("Edad de retiro", [60,61,62,63,64,65], index=0, key="retiro2")
        esposa2 = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa2")
        salario_m40 = st.number_input("Salario M40 ($)", min_value=0.0, max_value=20000.0, value=2932.0, step=100.0, key="sal_m40")
        meses_m40 = st.selectbox("Meses en M40", [6,12,18,24,30,36,42,48], index=1, key="meses")
        inpc_m40 = st.slider("INPC (%)", 2.0, 6.0, 4.2, 0.1, key="inpc2") / 100
    
    if st.button("Calcular Modalidad 40", type="primary", use_container_width=True, key="btn2"):
        with st.spinner("Analizando..."):
            res = calcular_mod40(semanas_m40, salario_actual, edad_m40, edad_retiro2, 
                               salario_m40, meses_m40, esposa2, inpc_m40)
            
            st.divider()
            
            # Incremento destacado
            st.markdown(f"""
            <div style='background-color: #00a86b; padding: 15px; border-radius: 10px; text-align: center; color: white; margin: 15px 0;'>
                <h2 style='color: white; margin:0'>💰 INCREMENTO MENSUAL</h2>
                <p style='font-size: 1.5rem; margin:5px'>Hoy: +${res['incremento']:,.0f} · 2029: +${res['incremento_2029']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Comparativa Hoy vs 2029
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 HOY")
                st.metric("Pensión base", f"${res['base']:,.0f}")
                st.metric("Pensión con M40", f"${res['con_m40']:,.0f}")
                st.metric("Inversión", f"${res['inversion']:,.0f}")
                st.metric("Recuperación", f"{res['recuperacion']} meses")
            
            with col2:
                st.markdown("### 📈 2029")
                st.metric("Pensión base", f"${res['base_2029']:,.0f}")
                st.metric("Pensión con M40", f"${res['con_m40_2029']:,.0f}")
                st.metric("ROI", f"{res['roi']}%")
                st.metric("Utilidad 20 años", f"${res['utilidad_20']:,.0f}")
            
            st.info(f"📈 **Factor INPC {res['factor_inpc']:.2f}x** · Para mantener poder adquisitivo")

# ========== PESTAÑA 3: COMPARATIVA CON 4 BARRAS SIDE BY SIDE ==========
with tab3:
    st.subheader("📊 Comparativa de escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_comp = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad3")
        semanas_comp = st.number_input("Semanas base", min_value=0, max_value=3000, value=1159, step=1, key="sem3")
        salario_comp = st.number_input("Salario actual", min_value=0.0, max_value=10000.0, value=960.0, step=10.0, key="sal3")
        salario_m40_comp = st.number_input("Salario M40", min_value=0.0, max_value=20000.0, value=2932.0, step=100.0, key="sal_m40_comp")
    
    with col2:
        edad_retiro_comp = st.selectbox("Edad retiro", [60,61,62,63,64,65], index=0, key="retiro3")
        esposa_comp = st.checkbox("¿Con asignación?", value=True, key="esposa3")
        inpc_comp = st.slider("INPC (%)", 2.0, 6.0, 4.2, 0.1, key="inpc3") / 100
        meses_comparar = st.multiselect("Meses M40 a comparar", 
                                       [6,12,18,24,30,36,42,48], 
                                       default=[12,24,36,48])
    
    if st.button("Comparar escenarios", type="primary", use_container_width=True, key="btn3") and meses_comparar:
        with st.spinner("Generando comparativa..."):
            
            # Pensión base
            base = calcular_pension_base(semanas_comp, salario_comp, edad_comp, edad_retiro_comp, esposa_comp)
            pension_base = base['mensual']
            
            años_a_2029 = max(0, 2029 - datetime.now().year)
            factor_inpc = (1 + inpc_comp) ** años_a_2029
            pension_base_2029 = pension_base * factor_inpc
            
            # Calcular escenarios M40
            resultados = []
            pensiones_m40 = []
            pensiones_m40_2029 = []
            
            for meses in sorted(meses_comparar):
                res = calcular_mod40(semanas_comp, salario_comp, edad_comp, edad_retiro_comp, 
                                    salario_m40_comp, meses, esposa_comp, inpc_comp)
                pensiones_m40.append(res['con_m40'])
                pensiones_m40_2029.append(res['con_m40_2029'])
                resultados.append({
                    "Meses M40": meses,
                    "Pensión HOY": f"${res['con_m40']:,.0f}",
                    "Pensión 2029": f"${res['con_m40_2029']:,.0f}",
                    "Incremento HOY": f"+${res['incremento']:,.0f}",
                    "Incremento 2029": f"+${res['incremento_2029']:,.0f}",
                    "Inversión": f"${res['inversion']:,.0f}",
                    "Recuperación": f"{res['recuperacion']} meses",
                    "ROI": f"{res['roi']}%"
                })
            
            st.divider()
            
            # ===== GRÁFICA CON 4 BARRAS SIDE BY SIDE =====
            fig = go.Figure()
            
            # Preparar datos para las barras
            x_labels = [f"{m} meses" for m in meses_comparar]
            
            # Barras: Base HOY (para cada mes, el mismo valor)
            fig.add_trace(go.Bar(
                name='Base HOY',
                x=x_labels,
                y=[pension_base] * len(meses_comparar),
                marker_color='#94a3b8',
                text=[f"${pension_base:,.0f}"] * len(meses_comparar),
                textposition='outside',
                width=0.15
            ))
            
            # Barras: Base 2029
            fig.add_trace(go.Bar(
                name='Base 2029',
                x=x_labels,
                y=[pension_base_2029] * len(meses_comparar),
                marker_color='#cbd5e1',
                text=[f"${pension_base_2029:,.0f}"] * len(meses_comparar),
                textposition='outside',
                width=0.15
            ))
            
            # Barras: Con M40 HOY
            fig.add_trace(go.Bar(
                name='Con M40 HOY',
                x=x_labels,
                y=pensiones_m40,
                marker_color='#0066b3',
                text=[f"${p:,.0f}" for p in pensiones_m40],
                textposition='outside',
                width=0.15
            ))
            
            # Barras: Con M40 2029
            fig.add_trace(go.Bar(
                name='Con M40 2029',
                x=x_labels,
                y=pensiones_m40_2029,
                marker_color='#00a86b',
                text=[f"${p:,.0f}" for p in pensiones_m40_2029],
                textposition='outside',
                width=0.15
            ))
            
            fig.update_layout(
                title="Comparación: HOY vs 2029",
                xaxis_title="Meses en M40",
                yaxis_title="Pensión mensual ($)",
                yaxis_tickformat="$,.0f",
                height=500,
                barmode='group',
                bargap=0.2,
                bargroupgap=0.1,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de resultados
            st.subheader("📋 Tabla comparativa")
            df = pd.DataFrame(resultados)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Mejor escenario
            mejor_idx = pensiones_m40_2029.index(max(pensiones_m40_2029))
            st.success(f"✨ **Mejor escenario 2029:** {meses_comparar[mejor_idx]} meses M40 - Pensión: ${pensiones_m40_2029[mejor_idx]:,.0f}")


# ============================================
# PIE DE PÁGINA SIMPLE
# ============================================
st.divider()
st.markdown("""
### ⚠️ AVISO IMPORTANTE

Este simulador proporciona estimaciones basadas en la Ley 73 del IMSS. Los resultados son aproximados y no constituyen un dictamen oficial.

Consulte con un asesor certificado para un cálculo definitivo.

---

📧 contacto@optipension73.com · 📱 871 579 1810 · 📍 Torreón, Coahuila

© 2026 OptiPensión 73. Todos los derechos reservados.
""")
