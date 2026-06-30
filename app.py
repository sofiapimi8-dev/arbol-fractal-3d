import streamlit as st
import numpy as np
from fractal import generar_arbol
from visualizacion import crear_grafico_3d
from matematicas import calcular_metricas_solido

st.set_page_config(page_title="Visualizador de Árbol Fractal 3D", layout="wide")

st.title("🌲 Modelado de Árbol Fractal 3D en Cruz")
st.write("Estructura basada en la intersección de dos planos fractales puros a 90°.")

# Barra lateral para los controles
st.sidebar.header("Parámetros del Fractal")
N = st.sidebar.slider("Niveles de recursión (N)", min_value=1, max_value=6, value=4)
r = st.sidebar.slider("Factor de reducción de longitud (r)", min_value=0.4, max_value=0.8, value=0.65, step=0.05)
L0 = st.sidebar.slider("Longitud del tronco inicial (L0)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

st.sidebar.header("Dimensiones Físicas de la Regla")
ancho_regla = st.sidebar.slider("Ancho de la regla (W)", min_value=0.1, max_value=1.0, value=0.3, step=0.05)
espesor_regla = st.sidebar.slider("Espesor de la regla (T)", min_value=0.02, max_value=0.20, value=0.05, step=0.01)

# Generación de los datos geométricos del árbol
inicio_tronco = np.array([0.0, 0.0, 0.0])
direccion_inicial = np.array([0.0, 0.0, 1.0])

ramas = generar_arbol(
    inicio=inicio_tronco,
    direccion=direccion_inicial,
    longitud=L0,
    nivel_actual=0,
    nivel_max=N,
    r=r
)

# Renderizado de la gráfica interactiva
fig = crear_grafico_3d(ramas)
st.plotly_chart(fig, use_container_width=True)

# Sección de métricas de ingeniería
st.header("📊 Métricas de Ingeniería y Manufactura")

if st.button("Calcular Modelo Sólido"):
    volumen_total, area_total, total_ramas = calcular_metricas_solido(ramas, ancho_regla, espesor_regla)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fórmulas de Volumen Sólido (Estructura en Cruz):**")
        st.latex(r"B_n = 2 \cdot 2^n")
        st.latex(r"V_{\text{rama}} = L \cdot W \cdot T")
        st.latex(r"V_T = \sum_{n=0}^{N} 2^{n+1} (L_n \cdot W \cdot T)")
        st.latex(r"A_T = \sum_{n=0}^{N} 2^{n+1} \cdot 2(L_n W + L_n T + W T)")

    with col2:
        st.metric(label="Número Total de Ramas", value=f"{total_ramas}")
        st.metric(label="Volumen Total del Sólido", value=f"{volumen_total:.4f} u³")
        st.metric(label="Área Superficial Total", value=f"{area_total:.4f} u²")
        st.success("Cálculo completado. Parámetros listos para análisis de material de impresión.")
