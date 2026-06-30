import numpy as np
import pandas as pd
from typing import List
from fractal import Rama

def calcular_volumen_prisma(L: float, W: float, T: float) -> float:
    """Calcula el volumen de una regla rectangular: V = Longitud * Ancho * Espesor"""
    return L * W * T

def calcular_area_prisma(L: float, W: float, T: float) -> float:
    """Calcula el área superficial exterior de un prisma rectangular (sus 6 caras)"""
    return 2 * (L * W + L * T + W * T)

def procesar_resultados_ramas(ramas: List[Rama], W: float, T: float) -> pd.DataFrame:
    """Procesa los datos matemáticos reales basados en los listones planos del árbol."""
    datos = []
    
    for rama in ramas:
        vol = calcular_volumen_prisma(rama.longitud, W, T)
        area = calcular_area_prisma(rama.longitud, W, T)
        datos.append({
            "Nivel": rama.nivel,
            "Longitud": rama.longitud,
            "Volumen": vol,
            "Área": area
        })
        
    df = pd.DataFrame(datos)
    
    resumen = df.groupby("Nivel").agg(
        Número_Ramas=("Nivel", "count"),
        Longitud_Individual=("Longitud", "first"),
        Volumen_Total_Nivel=("Volumen", "sum"),
        Área_Total_Nivel=("Área", "sum")
    ).reset_index()
    
    return resumen