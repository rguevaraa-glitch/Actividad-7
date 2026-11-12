# Actividad 8 – Algoritmos Voraces (Greedy)

Solución de dos problemas de optimización con estrategia **Greedy**, implementados en Python 3:

1. **Mochila fraccional** – maximizar el valor transportado pudiendo tomar fracciones de cada objeto.
2. **Cobertura de antenas** – usar la menor cantidad de antenas para cubrir todas las casas de una carretera.

## Requisitos

- Python 3.8 o superior (solo biblioteca estándar, no hay que instalar nada).
- *(Opcional)* `reportlab` si quieres regenerar el informe PDF: `pip install reportlab`.

## Estructura

```
.
├── main.py                      # Programa principal (menú interactivo)
├── src/
│   ├── mochila_fraccional.py    # Problema 1
│   └── cobertura_antenas.py     # Problema 2
├── tests/
│   └── test_greedy.py           # 17 pruebas de validación
└── docs/
    ├── Informe_Actividad8_Greedy.pdf   # Explicación, complejidad y ejemplos
    ├── casos_extra.py                  # Casos propios de ejecución
    ├── generar_informe.py              # Script que genera el PDF
    └── salida_*.txt                    # Salidas reales de las ejecuciones
```

## Cómo ejecutar

Desde la carpeta raíz del proyecto:

```bash
# Menú interactivo (ingresas tus propios datos)
python main.py

# Ejecutar directamente los 4 ejemplos guía de la actividad
python main.py --ejemplos

# Ejecutar las pruebas de validación
python -m unittest discover -v
```

### Formato de entrada en el menú

**Mochila fraccional** (opción 1):
```
Capacidad maxima: 50
Cantidad de objetos: 3
  > A 60 10        <- nombre valor peso
  > B 100 20
  > C 120 30
```

**Cobertura de antenas** (opción 2):
```
Posiciones de las casas: 1 2 7 11 20 21 30     <- espacios o comas
Rango de cobertura R: 5
```

## Resumen de las estrategias

| Problema | Criterio Greedy | Complejidad |
|---|---|---|
| Mochila fraccional | Tomar primero el objeto con mayor valor/peso | O(n log n) |
| Cobertura de antenas | Poner la antena en `primera_casa_sin_cubrir + R` | O(n log n) |

El detalle completo (justificación de optimalidad, Big O y ejemplos) está en `docs/Informe_Actividad8_Greedy.pdf`.
