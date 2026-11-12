"""
Problema 1: Mochila Fraccional (Fractional Knapsack)
====================================================

Estrategia Greedy
-----------------
Se ordenan los objetos por su "densidad de valor" (valor / peso) de mayor a
menor. Luego se recorren en ese orden:

  * Si el objeto cabe completo, se toma completo.
  * Si no cabe, se toma solo la fraccion que llena la capacidad restante
    y se termina (la mochila queda llena).

Como se permiten fracciones, esta eleccion local (el mejor valor por unidad de
peso) siempre conduce a la solucion global optima.

Complejidad: O(n log n) en tiempo (por el ordenamiento) y O(n) en espacio.
"""

from fractions import Fraction


class Objeto:
    """Representa un objeto con nombre, valor y peso."""

    def __init__(self, nombre, valor, peso):
        # Fraction(str(x)) permite trabajar con enteros y decimales sin
        # errores de redondeo (ej. 0.1 + 0.2).
        self.nombre = str(nombre)
        self.valor = Fraction(str(valor))
        self.peso = Fraction(str(peso))

        if self.peso <= 0:
            raise ValueError(f"El peso del objeto '{nombre}' debe ser mayor que 0.")
        if self.valor < 0:
            raise ValueError(f"El valor del objeto '{nombre}' no puede ser negativo.")

    @property
    def densidad(self):
        """Valor por unidad de peso: el criterio Greedy."""
        return self.valor / self.peso


def formatear(numero):
    """Muestra un Fraction como entero si es exacto, o como decimal si no."""
    if numero.denominator == 1:
        return str(numero.numerator)
    return f"{float(numero):.2f}".rstrip("0").rstrip(".")


def mochila_fraccional(objetos, capacidad):
    """
    Resuelve la mochila fraccional con estrategia Greedy.

    Parametros:
        objetos   -- lista de Objeto
        capacidad -- capacidad maxima de la mochila (>= 0)

    Retorna:
        (seleccion, valor_total) donde seleccion es una lista de tuplas
        (objeto, peso_tomado) en el orden en que fueron elegidos.
    """
    capacidad = Fraction(str(capacidad))
    if capacidad < 0:
        raise ValueError("La capacidad no puede ser negativa.")

    # PASO 1: ordenar por densidad descendente -> O(n log n).
    # sorted() es estable: ante empates se respeta el orden de entrada.
    ordenados = sorted(objetos, key=lambda o: o.densidad, reverse=True)

    seleccion = []
    valor_total = Fraction(0)
    restante = capacidad

    # PASO 2: recorrer los objetos en orden de densidad -> O(n).
    for obj in ordenados:
        if restante == 0:
            break  # mochila llena, no hay nada mas que hacer

        if obj.peso <= restante:
            # El objeto cabe completo: tomarlo entero.
            tomado = obj.peso
        else:
            # Solo cabe una parte: tomar la fraccion que llena la mochila.
            tomado = restante

        valor_total += obj.valor * tomado / obj.peso
        restante -= tomado
        seleccion.append((obj, tomado))

    return seleccion, valor_total


def mostrar_resultado(seleccion, valor_total):
    """Imprime el resultado con el formato pedido en la actividad."""
    print("Objetos seleccionados:")
    if not seleccion:
        print("  (ninguno)")
    for obj, tomado in seleccion:
        if tomado == obj.peso:
            print(f"  {obj.nombre} completo")
        else:
            print(f"  {formatear(tomado)}/{formatear(obj.peso)} "
                  f"Parte del objeto {obj.nombre}")
    print(f"Valor total obtenido: {formatear(valor_total)}")
