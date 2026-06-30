import streamlit as st
import numpy as np
import plotly.graph_objects as go
from fractal import generar_arbol

st.set_page_config(page_title="Visualizador de Árbol Fractal 3D", layout="wide")

st.title("Gráfico de Árbol Fractal 3D")
st.write("Estructura basada en la intersección de dos planos fractales puros a 90°(planos xz, yz)")

# Barra lateral para los controles
st.sidebar.header("Parámetros del fractal")
N = st.sidebar.slider("Niveles de recursión (N)", min_value=1, max_value=10, value=4)
r = st.sidebar.slider("Factor de reducción de longitud (r)", min_value=0.4, max_value=0.8, value=0.65, step=0.05)
L0 = st.sidebar.slider("Longitud del tronco inicial (L0)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

st.sidebar.header("Dimensiones físicas del sólido")
ancho_regla = st.sidebar.slider("Ancho del sólido (W)", min_value=0.1, max_value=1.0, value=0.3, step=0.05)
espesor_regla = st.sidebar.slider("Espesor del sólido (T)", min_value=0.02, max_value=0.20, value=0.05, step=0.01)

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

# Paleta de colores llamativos por nivel (Tronco marrón -> Ramas degradadas hasta cian/fosforescente)
COLORES_NIVEL = {
    0: '#5C4033',  # Marrón Oscuro (Tronco)
    1: '#CD7F32',  # Bronce / Madera clara
    2: '#2E8B57',  # Verde Mar
    3: '#3CB371',  # Verde Esmeralda
    4: '#20B2AA',  # Verde Azulado Claro
    5: '#00FFFF',  # Cian brillante
    6: '#ADFF2F',  # Verde Lima
    7: '#FFD700',  # Dorado
    8: '#FF8C00',  # Naranja Oscuro
    9: '#FF4500',  # Rojo Anaranjado
    10: '#FF00FF'  # Magenta (Puntas finales)
}
# Renderizado de la gráfica interactiva con colores por nivel y sin leyendas repetidas
fig = go.Figure()
for rama in ramas:
    color_rama = COLORES_NIVEL.get(rama.nivel, '#3CB371') # Asegura obtener el color del diccionario
    fig.add_trace(go.Scatter3d(
        x=[rama.inicio[0], rama.fin[0]],
        y=[rama.inicio[1], rama.fin[1]],
        z=[rama.inicio[2], rama.fin[2]],
        mode='lines',
        line=dict(color=color_rama, width=max(2, 8 - rama.nivel * 1.2)),
        showlegend=False # ¡Esto borra los "trace 0, trace 1..." de la pantalla!
    ))

fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='data'
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# Sección de métricas de ingeniería
st.header("Cálculos")

if st.button("Calcular modelo sólido"):
    # Cálculo directo dentro de la app para evitar ImportErrors
    total_ramas = len(ramas)
    volumen_total = 0.0
    area_total = 0.0
    
    for rama in ramas:
        L = rama.longitud
        W = ancho_regla
        T = espesor_regla
        
        volumen_total += (L * W * T)
        area_total += 2 * (L * W + L * T + W * T)
        
    col1, col2 = st.columns(2)
    # ==========================================

tab1, tab2 = st.tabs(["Cálculos del modelo sólido visualizado", "Cálculo modelo teórico (sin límites)"])

with tab1:
    total_ramas = len(ramas)
    volumen_total = sum(r.longitud * ancho_regla * espesor_regla for r in ramas)
    area_total = sum(2 * (r.longitud * ancho_regla + r.longitud * espesor_regla + ancho_regla * espesor_regla) for r in ramas)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Ecuaciones del modelo:**")
        st.latex(r"V_T = \sum_{n=0}^{N} 2^{n+1} (L_n \cdot W \cdot T)")
    with col_f2:
        st.metric(label="Ramas graficadas", value=f"{total_ramas}")
        st.metric(label="Volumen del sólido", value=f"{volumen_total:.4f} u³")
        st.metric(label="Área superficial", value=f"{area_total:.4f} u²")

with tab2:
    st.write("### Simulación de datos a gran escala")
    st.write("Escribe el nivel de iteración exacto que deseas evaluar:")
    
    # Caja de entrada libre (puedes teclear 50, 100, 500...)
    N_masivo = st.number_input("Ingresa el nivel de iteración (N)", min_value=1, max_value=1000000, value=50, step=1)
    
    W = ancho_regla
    T = espesor_regla
    
    # Cálculos puros directos usando álgebra de series (milisegundos)
    total_ramas_masivo = 2 * (2**(N_masivo + 1) - 1)
    
    if abs(2 * r - 1.0) < 1e-9:
        volumen_masivo = 2 * (L0 * W * T) * (N_masivo + 1)
        area_masiva = 2 * 2 * (L0 * W + L0 * T + W * T) * (N_masivo + 1)
    else:
        volumen_masivo = 2 * (L0 * W * T) * ((1 - (2 * r)**(N_masivo + 1)) / (1 - 2 * r))
        
        suma_areas = 0.0
        for n in range(N_masivo + 1):
            Ln = L0 * (r**n)
            cantidad_ramas_nivel = 2 * (2**n)
            suma_areas += cantidad_ramas_nivel * 2 * (Ln * W + Ln * T + W * T)
        area_masiva = suma_areas

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("**Fórmulas de crecimiento geométrico:**")
        st.latex(r"B_{\text{total}} = 2 \cdot (2^{N+1} - 1)")
        st.latex(r"V_N = 2 \cdot L_0 W T \left( \frac{1 - (2r)^{N+1}}{1 - 2r} \right)")
        
        if r < 0.5:
            vol_infinito = 2 * (L0 * W * T) / (1 - 2 * r)
            st.markdown("**Límite teórico verdadero si $N \\to \\infty$:**")
            st.latex(r"V_{\infty} = \frac{2 L_0 W T}{1 - 2r}")
            st.info(f"Volumen máximo absoluto en el infinito: **{vol_infinito:.4f} u³**")
        else:
            st.warning("**Nota:** Con r ≥ 0.5 el volumen diverge en el infinito físico")

    with col_m2:
        st.subheader("Resultados")
        st.metric(label=f"Ramas Totales en N={N_masivo}", value=f"{total_ramas_masivo:,}")
        st.metric(label=f"Volumen", value=f"{volumen_masivo:.4f} u³")
        st.metric(label=f"Área Superficial Estimada", value=f"{area_masiva:.4f} u²")
