import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="💰 Simulador de Pensión PRO",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Simulador de Pensión PRO")
st.caption("Ing. Roberto Villarreal · Ley 73")

edad = st.slider("Edad actual", 40, 65, 55)
semanas = st.number_input("Semanas cotizadas", 0, 3000, 1315)
salario = st.number_input("Salario diario promedio ($)", 0.0, 5000.0, 1010.0)

st.metric("Edad", edad)
st.metric("Semanas", semanas)
st.metric("Salario", f"${salario:,.2f}")

st.success("✅ App funcionando correctamente")