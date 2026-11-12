"""
Actividad 8 - Algoritmos Voraces (Greedy)
Programa principal con menu interactivo.

Uso:
    python main.py            # menu interactivo
    python main.py --ejemplos # ejecuta los ejemplos guia de la actividad
"""

import sys

from src.mochila_fraccional import Objeto, mochila_fraccional
from src.mochila_fraccional import mostrar_resultado as mostrar_mochila
from src.cobertura_antenas import cobertura_antenas
from src.cobertura_antenas import mostrar_resultado as mostrar_antenas


def leer_mochila():
    """Lee capacidad y objetos por teclado y resuelve la mochila fraccional."""
    capacidad = input("Capacidad maxima: ").strip()
    n = int(input("Cantidad de objetos: "))
    objetos = []
    print("Ingresa cada objeto como: nombre valor peso   (ej. A 60 10)")
    for _ in range(n):
        nombre, valor, peso = input("  > ").split()
        objetos.append(Objeto(nombre, valor, peso))
    print()
    seleccion, total = mochila_fraccional(objetos, capacidad)
    mostrar_mochila(seleccion, total)


def leer_antenas():
    """Lee casas y R por teclado y resuelve la cobertura de antenas."""
    texto = input("Posiciones de las casas (separadas por espacios o comas): ")
    casas = [int(t) for t in texto.replace(",", " ").split()]
    R = int(input("Rango de cobertura R: "))
    print()
    mostrar_antenas(cobertura_antenas(casas, R))


def ejemplos_guia():
    """Ejecuta los 4 ejemplos guia del enunciado."""
    print("=" * 50)
    print("MOCHILA FRACCIONAL - Ejemplo 1 (capacidad 50)")
    print("=" * 50)
    objs = [Objeto("A", 60, 10), Objeto("B", 100, 20), Objeto("C", 120, 30)]
    mostrar_mochila(*mochila_fraccional(objs, 50))

    print()
    print("=" * 50)
    print("MOCHILA FRACCIONAL - Ejemplo 2 (capacidad 25)")
    print("=" * 50)
    objs = [Objeto("A", 80, 20), Objeto("B", 100, 10), Objeto("C", 120, 30)]
    mostrar_mochila(*mochila_fraccional(objs, 25))

    print()
    print("=" * 50)
    print("COBERTURA DE ANTENAS - Ejemplo 1")
    print("Casas: [1,2,7,11,20,21,30]  R = 5")
    print("=" * 50)
    mostrar_antenas(cobertura_antenas([1, 2, 7, 11, 20, 21, 30], 5))

    print()
    print("=" * 50)
    print("COBERTURA DE ANTENAS - Ejemplo 2")
    print("Casas: [2,4,8,15,18,22]  R = 3")
    print("=" * 50)
    mostrar_antenas(cobertura_antenas([2, 4, 8, 15, 18, 22], 3))


def menu():
    while True:
        print("\n--- Actividad 8: Algoritmos Greedy ---")
        print("1. Mochila fraccional")
        print("2. Cobertura de antenas")
        print("3. Ejecutar ejemplos guia")
        print("0. Salir")
        opcion = input("Opcion: ").strip()
        try:
            if opcion == "1":
                leer_mochila()
            elif opcion == "2":
                leer_antenas()
            elif opcion == "3":
                ejemplos_guia()
            elif opcion == "0":
                break
            else:
                print("Opcion no valida.")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Entrada invalida: {e}")


if __name__ == "__main__":
    if "--ejemplos" in sys.argv:
        ejemplos_guia()
    else:
        menu()
