import streamlit as st
import numpy as np
import pandas as pd
from fractal import generar_arbol
from matematicas import procesar_resultados_ramas
from visualizacion import graficar_arbol

st.set_page_config(page_title="Fractal 3D Real (Impresión 3D)", layout="wide")

st.title("🌲 Modelado de Árbol Fractal 3D: Prisma Rectangular")
st.markdown("Generación adaptada al modelo real de impresión 3D utilizando listones rectangulares planos con intersección de planos locales.")

st.sidebar.header("Datos de la Regla Sólida")

N = st.sidebar.number_input("Número de iteraciones (N)", min_value=1, max_value=6, value=4, step=1)
L0 = st.sidebar.number_input("Longitud inicial del tronco ($L_0$)", min_value=1.0, value=10.0, step=1.0)
r = st.sidebar.number_input("Factor de reducción de largo ($r$)", min_value=0.1, max_value=0.9, value=0.6, step=0.05)
W = st.sidebar.number_input("Ancho de la Regla ($W$)", min_value=0.1, value=1.2, step=0.1)
T = st.sidebar.number_input("Espesor/Grosor Fijo de la Regla ($T$)", min_value=0.05, value=0.3, step=0.05)

if 'ramas' not in st.session_state:
    st.session_state.ramas = []
if 'resultados' not in st.session_state:
    st.session_state.resultados = pd.DataFrame()

if st.sidebar.button("Calcular Modelo Sólido", type="primary"):
    with st.spinner("Construyendo mallas poligonales..."):
        inicio = np.array([0.0, 0.0, 0.0])
        direccion_inicial = np.array([0.0, 0.0, 1.0])
        
        st.session_state.ramas = generar_arbol(
            inicio=inicio,
            direccion=direccion_inicial,
            longitud=L0,
            nivel_actual=0,
            nivel_max=N,
            r=r
        )
        st.session_state.resultados = procesar_resultados_ramas(st.session_state.ramas, W, T)

if not st.session_state.ramas:
    st.info("👈 Modifica el ancho y espesor de tus listones en la barra lateral y presiona 'Calcular'.")
else:
    st.subheader("Visualización del Sólido Real Imprimible")
    
    nivel_mostrar = st.slider("Crecimiento dinámico por nivel", 
                              min_value=0, 
                              max_value=N, 
                              value=N)
    
    # Pasamos W y T a la gráfica para que ensanche o engrose las reglas
    fig = graficar_arbol(st.session_state.ramas, nivel_mostrar, W, T)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Análisis Matemático del Prisma")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Fórmulas de Volumen Sólido:**")
        st.latex(r"B_n = 4^n")
        st.latex(r"V_{\text{rama}} = L \cdot W \cdot T")
        st.latex(r"V_T = \sum_{n=0}^{N} 4^n (L_n \cdot W \cdot T)")
        st.latex(r"A_T = \sum_{n=0}^{N} 4^n \cdot 2(L_n W + L_n T + W T)")
        
        vol_total = st.session_state.resultados["Volumen_Total_Nivel"].sum()
        area_total = st.session_state.resultados["Área_Total_Nivel"].sum()
        
        st.metric("Volumen de Material Total", f"{vol_total:.2f} u³")
        st.metric("Área Superficial Total", f"{area_total:.2f} u²")

    with col2:
        st.markdown("**Sucesiones Calculadas desde los Objetos:**")
        st.dataframe(
            st.session_state.resultados.style.format({
                "Longitud_Individual": "{:.4f}",
                "Volumen_Total_Nivel": "{:.4f}",
                "Área_Total_Nivel": "{:.4f}"
            }), 
            use_container_width=True
        )
        
        csv = st.session_state.resultados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Reporte Físico (CSV)",
            data=csv,
            file_name='modelo_impresion_3d_fractal.csv',
            mime='text/csv',
        )