"""Casos de ejecucion adicionales (propios) para el informe."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.mochila_fraccional import Objeto, mochila_fraccional, mostrar_resultado as m1
from src.cobertura_antenas import cobertura_antenas, mostrar_resultado as m2

print("MOCHILA - Caso propio 1 (capacidad 15, 7 objetos)")
objs = [Objeto("A",10,2), Objeto("B",5,3), Objeto("C",15,5), Objeto("D",7,7),
        Objeto("E",6,1), Objeto("F",18,4), Objeto("G",3,1)]
m1(*mochila_fraccional(objs, 15))

print()
print("MOCHILA - Caso borde: capacidad 0")
m1(*mochila_fraccional([Objeto("A",10,5)], 0))

print()
print("MOCHILA - Caso borde: capacidad mayor al peso total (capacidad 100)")
m1(*mochila_fraccional([Objeto("A",10,5), Objeto("B",20,5)], 100))

print()
print("ANTENAS - Caso propio 1: casas desordenadas y repetidas, R = 5")
print("Casas: [30,1,2,2,7,11,21,20,50,52]")
m2(cobertura_antenas([30,1,2,2,7,11,21,20,50,52], 5))

print()
print("ANTENAS - Caso borde: R = 0 (una antena por casa distinta)")
print("Casas: [4,4,9,12]")
m2(cobertura_antenas([4,4,9,12], 0))

print()
print("ANTENAS - Caso borde: una sola casa, R = 3")
m2(cobertura_antenas([10], 3))

print()
print("ANTENAS - Caso borde: todas las casas en un solo intervalo de largo 2R")
print("Casas: [10,12,14,16,18,20], R = 5")
m2(cobertura_antenas([10,12,14,16,18,20], 5))
