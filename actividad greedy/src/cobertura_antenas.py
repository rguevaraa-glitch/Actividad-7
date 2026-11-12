"""
Problema 2: Cobertura de antenas
================================

Estrategia Greedy
-----------------
Se ordenan las casas de izquierda a derecha. Se toma la primera casa que
todavia NO esta cubierta (la mas a la izquierda) y se coloca una antena lo mas
a la derecha posible sin dejarla fuera de cobertura, es decir, en la posicion
    x = casa + R
Esa antena cubre el intervalo [casa, casa + 2R]. Se saltan todas las casas
dentro de ese intervalo y se repite con la siguiente casa sin cubrir.

Por que es optimo: la casa mas a la izquierda sin cubrir debe ser cubierta por
alguna antena; entre todas las antenas que la cubren, la que esta en casa + R
alcanza mas casas hacia la derecha, asi que nunca es peor que otra opcion.

Complejidad: O(n log n) en tiempo (ordenamiento) y O(n) en espacio.
"""


def cobertura_antenas(casas, R):
    """
    Calcula la menor cantidad de antenas para cubrir todas las casas.

    Parametros:
        casas -- lista de posiciones enteras de las casas
        R     -- rango de cobertura de cada antena (R >= 0)

    Retorna:
        Lista con las posiciones de las antenas colocadas.
    """
    if R < 0:
        raise ValueError("El rango de cobertura R no puede ser negativo.")

    # PASO 1: ordenar y eliminar duplicados (dos casas en la misma posicion
    # se cubren juntas) -> O(n log n).
    posiciones = sorted(set(casas))

    antenas = []
    i = 0
    n = len(posiciones)

    # PASO 2: un solo recorrido; cada casa se visita una vez -> O(n).
    while i < n:
        primera_sin_cubrir = posiciones[i]

        # Eleccion Greedy: antena lo mas a la derecha posible.
        x = primera_sin_cubrir + R
        antenas.append(x)

        # Esta antena cubre [x - R, x + R]. Saltar todas las casas cubiertas.
        limite = x + R
        while i < n and posiciones[i] <= limite:
            i += 1

    return antenas


def mostrar_resultado(antenas):
    """Imprime el resultado con el formato pedido en la actividad."""
    print("Antenas colocadas aproximadamente en:")
    if not antenas:
        print("  (ninguna)")
    for x in antenas:
        print(f"  {x}")
    print(f"Cantidad total: {len(antenas)}")
