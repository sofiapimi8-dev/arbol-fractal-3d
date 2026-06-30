import plotly.graph_objects as go
import numpy as np
from typing import List
from fractal import Rama, obtener_ejes_locales

def obtener_color_nivel(nivel: int) -> str:
    colores = {
        0: "#4A2E15", # Tronco marrón oscuro
        1: "#704214", # Ramas marrón
        2: "#145A32", # Verde oscuro
        3: "#229954", # Verde
    }
    return colores.get(nivel, "#82E0AA")

def graficar_arbol(ramas: List[Rama], nivel_max_mostrar: int, W: float, T: float) -> go.Figure:
    """Dibuja el árbol utilizando mallas 3D (Mesh3d) con forma de reglas planas."""
    fig = go.Figure()
    
    ramas_filtradas = [r for r in ramas if r.nivel <= nivel_max_mostrar]
    niveles_presentes = set(r.nivel for r in ramas_filtradas)
    
    for nivel in niveles_presentes:
        ramas_nivel = [r for r in ramas_filtradas if r.nivel == nivel]
        
        # Listas para colapsar todos los vértices de este nivel en una sola malla flotante
        x_all, y_all, z_all = [], [], []
        i_all, j_all, k_all = [], [], []
        
        v_offset = 0  # Desplazamiento de los índices para no mezclar las reglas
        
        for rama in ramas_nivel:
            u, v = obtener_ejes_locales(rama.direccion)
            
            # Calcular las 8 esquinas de la regla rectangular plana
            # Base de la regla
            p0 = rama.inicio + (W/2)*u + (T/2)*v
            p1 = rama.inicio - (W/2)*u + (T/2)*v
            p2 = rama.inicio - (W/2)*u - (T/2)*v
            p3 = rama.inicio + (W/2)*u - (T/2)*v
            # Punta de la regla
            p4 = rama.fin + (W/2)*u + (T/2)*v
            p5 = rama.fin - (W/2)*u + (T/2)*v
            p6 = rama.fin - (W/2)*u - (T/2)*v
            p7 = rama.fin + (W/2)*u - (T/2)*v
            
            # Guardar coordenadas de vértices
            for p in [p0, p1, p2, p3, p4, p5, p6, p7]:
                x_all.append(p[0])
                y_all.append(p[1])
                z_all.append(p[2])
            
            # Triangulación de las 6 caras del prisma rectangular (12 triángulos en total)
            i_box = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
            j_box = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 0, 4]
            k_box = [2, 3, 6, 7, 5, 4, 6, 5, 7, 6, 4, 7]
            
            # Ajustar los índices con el offset del vértice actual
            i_all.extend([idx + v_offset for idx in i_box])
            j_all.extend([idx + v_offset for idx in j_box])
            k_all.extend([idx + v_offset for idx in k_box])
            
            v_offset += 8 # Cada regla aporta 8 vértices nuevos
            
        color = obtener_color_nivel(nivel)
        
        # Añadir la malla sólida tridimensional a Plotly
        fig.add_trace(go.Mesh3d(
            x=x_all, y=y_all, z=z_all,
            i=i_all, j=j_all, k=k_all,
            color=color,
            name=f'Nivel {nivel}',
            flatshading=True, # Hace que las esquinas y caras planas se vean súper nítidas
            opacity=1.0,
            showlegend=True
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig