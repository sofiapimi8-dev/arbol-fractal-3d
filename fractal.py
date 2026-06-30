import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Rama:
    """Clase que representa una rama individual del árbol fractal."""
    inicio: np.ndarray
    fin: np.ndarray
    nivel: int
    longitud: float
    direccion: np.ndarray

def obtener_ejes_locales(direccion: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calcula los vectores ortogonales locales para orientar la regla plana."""
    if abs(direccion[2]) > 0.999:
        u = np.array([1.0, 0.0, 0.0])
    else:
        z_global = np.array([0.0, 0.0, 1.0])
        u = np.cross(direccion, z_global)
        u = u / np.linalg.norm(u)
        
    v = np.cross(direccion, u)
    v = v / np.linalg.norm(v)
    
    return u, v

def generar_ramas_plano(inicio: np.ndarray, 
                        direccion: np.ndarray, 
                        vector_abertura: np.ndarray,
                        longitud: float, 
                        nivel_actual: int, 
                        nivel_max: int, 
                        r: float, 
                        lista_ramas: List[Rama]) -> None:
    """Genera un árbol fractal puramente plano (bifurcación de 2 ramas)."""
    fin = inicio + direccion * longitud
    rama_actual = Rama(inicio=inicio, fin=fin, nivel=nivel_actual, longitud=longitud, direccion=direccion)
    lista_ramas.append(rama_actual)

    if nivel_actual == nivel_max:
        return

    theta = np.radians(35)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # Cada rama se abre en SOLO DOS direcciones dentro de su plano asignado
    dir_1 = cos_t * direccion + sin_t * vector_abertura
    dir_2 = cos_t * direccion - sin_t * vector_abertura

    direcciones_hijas = [
        dir_1 / np.linalg.norm(dir_1),
        dir_2 / np.linalg.norm(dir_2)
    ]

    nueva_longitud = longitud * r

    for dir_hija in direcciones_hijas:
        generar_ramas_plano(fin, dir_hija, vector_abertura, nueva_longitud, nivel_actual + 1, nivel_max, r, lista_ramas)

def generar_arbol(inicio: np.ndarray, 
                  direccion: np.ndarray, 
                  longitud: float, 
                  nivel_actual: int, 
                  nivel_max: int, 
                  r: float) -> List[Rama]:
    """Construye la intersección de dos árboles planos independientes a 90 grados."""
    lista_ramas = []
    
    # Definimos los vectores de apertura para cada plano
    eje_x = np.array([1.0, 0.0, 0.0]) # Plano Frontal
    eje_y = np.array([0.0, 1.0, 0.0]) # Plano Lateral (Rotado 90°)

    # Árbol 1: Bifurcaciones en el plano X (Frontal)
    generar_ramas_plano(inicio, direccion, eje_x, longitud, nivel_actual, nivel_max, r, lista_ramas)
    
    # Árbol 2: Bifurcaciones en el plano Y (Lateral)
    generar_ramas_plano(inicio, direccion, eje_y, longitud, nivel_actual, nivel_max, r, lista_ramas)

    return lista_ramas
