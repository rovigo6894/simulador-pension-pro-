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
# FUNCIÓN DE CÁLCULO EXACTA DE LA HOJA 1
# ============================================

def calcular_pension_hoja1(semanas, salario_promedio, edad_actual, edad_retiro, esposa=True):
    """
    Cálculo EXACTO según hoja PENSION 73 de tu Excel
    """
    
    # Factor por edad (celda D6)
    FACTOR_POR_EDAD = {60:0.75, 61:0.80, 62:0.85, 63:0.90, 64:0.95, 65:1.00}
    FACTOR_EDAD = FACTOR_POR_EDAD.get(edad_retiro, 0.75)
    
    # Porcentajes (celdas D14, D15, D9)
    PCT_CUANTIA = 0.13      # D14
    PCT_INCREMENTO = 0.0245  # D15
    PCT_ESPOSA = 0.15 if esposa else 0  # D9
    DECRETO_FOX = 0.11       # 11% fijo
    
    # Semanas totales al retiro (como en tu Excel)
    años_para_retiro = max(0, edad_retiro - edad_actual)
    semanas_totales = semanas + (52 * años_para_retiro)  # D7
    
    # CUANTIA BASICA POR DIA (D17)
    cuantia_basica_diaria = salario_promedio * PCT_CUANTIA
    
    # IMPORTE ANUAL CUANTIA BASICA (D18)
    cuantia_basica_anual = cuantia_basica_diaria * 365
    
    # INCREMENTOS DIARIOS (D20)
    incremento_diario = salario_promedio * PCT_INCREMENTO
    
    # AÑOS DESPUES DE LAS PRIMERAS 500 (D22)
    años_despues_500 = max(0, (semanas_totales - 500) / 52)
    
    # IMPORTE ANUAL INCREMENTOS (D23)
    incremento_anual = incremento_diario * 365 * años_despues_500
    
    # CUANTIA TOTAL DE PENSION ANUAL (D25)
    cuantia_total_anual = cuantia_basica_anual + incremento_anual
    
    # ASIGNACION ESPOSA (D26)
    asignacion_esposa = cuantia_total_anual * PCT_ESPOSA
    
    # TOTAL CUANTIA BASICA + ASIGNACION (D27)
    total_con_esposa = cuantia_total_anual + asignacion_esposa
    
    # 11% DECRETO FOX (D28)
    decreto_fox = total_con_esposa * DECRETO_FOX
    
    # TOTAL DE CUANTIA BASE (D29)
    cuantia_base_total = total_con_esposa + decreto_fox
    
    # RETIRO A LOS 60 AÑOS (D31)
    pension_anual = cuantia_base_total * FACTOR_EDAD
    
    # PENSION MENSUAL TOTAL (D33)
    pension_mensual = pension_anual / 12
    
    return {
        'mensual': round(pension_mensual, 2),
        'anual': round(pension_anual, 2),
        'semanas_totales': round(semanas_totales, 0),
        'factor_edad': FACTOR_EDAD
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
        semanas_hoy = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1315, step=1, key="sem1")
        salario_promedio = st.number_input("Salario promedio ($)", min_value=0.0, max_value=10000.0, value=965.25, step=10.0, key="sal1")
    
    with col2:
        edad_retiro = st.selectbox("Edad de retiro", [60, 61, 62, 63, 64, 65], index=0, key="retiro1")
        asignacion_esposa = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa1")
        inflacion = st.slider("Inflación estimada anual (%)", 0.0, 10.0, 4.0, key="inf1") / 100
    
    if st.button("Calcular pensión base", type="primary", use_container_width=True, key="btn1"):
        with st.spinner("Calculando..."):
            base = calcular_pension_hoja1(semanas_hoy, salario_promedio, edad_actual, edad_retiro, asignacion_esposa)
            
            st.divider()
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            with col_r2:
                st.markdown(f"""
                <div style='background-color: #0066b3; padding: 20px; border-radius: 10px; text-align: center; color: white'>
                    <h2 style='color: white; margin:0'>PENSIÓN MENSUAL</h2>
                    <h1 style='color: white; font-size: 48px; margin:10px'>${base['mensual']:,.0f}</h1>
                    <p style='color: #e0e0e0; margin:0'>Retiro a los {edad_retiro} años</p>
                    <p style='color: #e0e0e0; margin:0; font-size: 12px;'>Semanas totales: {base['semanas_totales']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("🔍 Ver detalle del cálculo"):
                st.write(f"**Factor por edad:** {base['factor_edad']*100:.0f}%")
                st.write(f"**Semanas a los {edad_retiro} años:** {base['semanas_totales']:.0f}")
            
            años_para_retiro = max(0, edad_retiro - edad_actual)
            if años_para_retiro > 0 and inflacion > 0:
                factor_inflacion = (1 + inflacion) ** años_para_retiro
                pension_inflacion = base['mensual'] * factor_inflacion
                st.info(f"📈 Con inflación del {inflacion*100:.1f}% anual: ${pension_inflacion:,.2f} (pesos de hoy)")

# ========== PESTAÑA 2: MODALIDAD 40 ==========
with tab2:
    st.subheader("Análisis de Modalidad 40")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_m40 = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad2")
        semanas_m40 = st.number_input("Semanas cotizadas", min_value=0, max_value=3000, value=1315, step=1, key="sem2")
        salario_actual = st.number_input("Salario actual ($)", min_value=0.0, max_value=10000.0, value=965.25, step=10.0, key="sal2")
    
    with col2:
        edad_retiro2 = st.selectbox("Edad de retiro", [60,61,62,63,64,65], index=0, key="retiro2")
        esposa2 = st.checkbox("¿Con asignación por esposa?", value=True, key="esposa2")
        salario_m40 = st.number_input("Salario M40 ($)", min_value=0.0, max_value=20000.0, value=2932.0, step=100.0, key="sal_m40")
        meses_m40 = st.selectbox("Meses en M40", [6,12,18,24,30,36,42,48], index=0, key="meses")
    
    if st.button("Calcular Modalidad 40", type="primary", use_container_width=True, key="btn2"):
        st.info("🔧 Función de Modalidad 40 en desarrollo")

# ========== PESTAÑA 3: COMPARATIVA ==========
with tab3:
    st.subheader("Comparativa de escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_comp = st.number_input("Edad actual", min_value=40, max_value=65, value=57, step=1, key="edad3")
        semanas_comp = st.number_input("Semanas", min_value=0, max_value=3000, value=1315, step=1, key="sem3")
        salario_comp = st.number_input("Salario", min_value=0.0, max_value=10000.0, value=965.25, step=10.0, key="sal3")
    
    with col2:
        edad_retiro3 = st.selectbox("Edad retiro", [60,61,62,63,64,65], index=0, key="retiro3")
        esposa3 = st.checkbox("¿Con asignación?", value=True, key="esposa3")
    
    if st.button("Comparar edades de retiro", type="primary", use_container_width=True, key="btn3"):
        with st.spinner("Generando comparativa..."):
            
            pensiones = []
            edades = [60,61,62,63,64,65]
            
            for edad in edades:
                res = calcular_pension_hoja1(semanas_comp, salario_comp, edad_comp, edad, esposa3)
                pensiones.append(res['mensual'])
            
            st.divider()
            
            # Gráfica de barras
            fig = go.Figure(data=[
                go.Bar(name='Pensión', x=[f"{e} años" for e in edades], 
                       y=pensiones, marker_color='#0066b3')
            ])
            
            fig.update_layout(
                title="Pensión según edad de retiro",
                xaxis_title="Edad de retiro",
                yaxis_title="Pensión mensual ($)",
                yaxis_tickformat="$,.0f",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla comparativa
            df = pd.DataFrame({
                'Edad retiro': edades,
                'Pensión mensual': [f"${p:,.0f}" for p in pensiones],
                'Factor': [f"{0.75 + (i*0.05):.0%}" for i in range(6)]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

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
