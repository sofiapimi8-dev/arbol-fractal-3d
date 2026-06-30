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
    """
    Calcula los vectores ortogonales locales (u, v) para una dirección dada.
    'u' representa el ancho de la regla y 'v' el espesor de la regla.
    """
    if abs(direccion[2]) > 0.999:
        u = np.array([1.0, 0.0, 0.0])
    else:
        z_global = np.array([0.0, 0.0, 1.0])
        u = np.cross(direccion, z_global)
        u = u / np.linalg.norm(u)
        
    v = np.cross(direccion, u)
    v = v / np.linalg.norm(v)
    
    return u, v

def generar_arbol(inicio: np.ndarray, 
                  direccion: np.ndarray, 
                  longitud: float, 
                  nivel_actual: int, 
                  nivel_max: int, 
                  r: float, 
                  lista_ramas: List[Rama] = None) -> List[Rama]:
    """Algoritmo recursivo para generar la estructura del árbol."""
    if lista_ramas is None:
        lista_ramas = []

    fin = inicio + direccion * longitud
    rama_actual = Rama(inicio=inicio, fin=fin, nivel=nivel_actual, longitud=longitud, direccion=direccion)
    lista_ramas.append(rama_actual)

    if nivel_actual == nivel_max:
        return lista_ramas

    u, v = obtener_ejes_locales(direccion)
    theta = np.radians(35)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # Direcciones hijas en los planos locales XZ e YZ
    dir_1 = cos_t * direccion + sin_t * u
    dir_2 = cos_t * direccion - sin_t * u
    dir_3 = cos_t * direccion + sin_t * v
    dir_4 = cos_t * direccion - sin_t * v

    direcciones_hijas = [
        dir_1 / np.linalg.norm(dir_1),
        dir_2 / np.linalg.norm(dir_2),
        dir_3 / np.linalg.norm(dir_3),
        dir_4 / np.linalg.norm(dir_4)
    ]

    nueva_longitud = longitud * r

    for dir_hija in direcciones_hijas:
        generar_arbol(fin, dir_hija, nueva_longitud, nivel_actual + 1, nivel_max, r, lista_ramas)

    return lista_ramas