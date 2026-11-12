"""
Genera el informe PDF de la Actividad 8 (Algoritmos Voraces).
Uso (desde la raiz del proyecto):  python docs/generar_informe.py
Requiere: pip install reportlab
"""
import inspect
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

from src.mochila_fraccional import mochila_fraccional
from src.cobertura_antenas import cobertura_antenas

# ----------------------------------------------------------------- datos
ESTUDIANTE = "Rodrigo"
INSTITUCION = "Universidad La Salle - Arequipa"
CURSO = "Análisis de Algoritmos"
SALIDA = os.path.join(os.path.dirname(__file__), "Informe_Actividad8_Greedy.pdf")

# ----------------------------------------------------------------- fuentes
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DV-BI", FD + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFont(TTFont("DVM", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

NAVY = colors.HexColor("#1F3A5F")
TEAL = colors.HexColor("#2A8C8C")
STEEL = colors.HexColor("#E8EEF4")
GRIS = colors.HexColor("#444444")

ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=ss["Normal"], fontName="DV", fontSize=9.5,
                      leading=14, alignment=TA_JUSTIFY, textColor=GRIS, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=BODY, fontName="DV-B", fontSize=16, leading=20,
                    textColor=NAVY, spaceBefore=10, spaceAfter=8, alignment=0, keepWithNext=1)
H2 = ParagraphStyle("h2", parent=BODY, fontName="DV-B", fontSize=12, leading=16,
                    textColor=TEAL, spaceBefore=8, spaceAfter=4, alignment=0, keepWithNext=1)
TITLE = ParagraphStyle("title", parent=H1, fontSize=26, leading=32, spaceAfter=4)
SUB = ParagraphStyle("sub", parent=BODY, fontSize=13, leading=18, alignment=0, textColor=TEAL)
CODE = ParagraphStyle("code", fontName="DVM", fontSize=7.4, leading=9.6, textColor=colors.HexColor("#1a1a1a"))
BODYK = ParagraphStyle("bodyk", parent=BODY, keepWithNext=1)
BUL = ParagraphStyle("bul", parent=BODY, leftIndent=14, bulletIndent=2, spaceAfter=3)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.8, leading=12, alignment=0, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="DV-B", textColor=colors.white)


def p(t, s=BODY):
    return Paragraph(t, s)


def bullets(items):
    return [Paragraph(i, BUL, bulletText="•") for i in items]


def bloque_codigo(texto):
    """Caja gris con codigo monoespaciado."""
    t = Table([[Preformatted(texto, CODE)]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F8")),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C5CFD9")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def tabla(filas, anchos, cabecera=True):
    datos = []
    for i, f in enumerate(filas):
        est = CELLB if (cabecera and i == 0) else CELL
        datos.append([Paragraph(str(c), est) for c in f])
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1 if cabecera else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D0")),
           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if cabecera:
        est.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        for r in range(1, len(filas)):
            if r % 2 == 0:
                est.append(("BACKGROUND", (0, r), (-1, r), STEEL))
    t.setStyle(TableStyle(est))
    return t


def fuente(func):
    return inspect.getsource(func).rstrip()


def leer(nombre):
    with open(os.path.join(os.path.dirname(__file__), nombre), encoding="utf-8") as f:
        return f.read().rstrip()


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.2 * cm, "Actividad 8 - Algoritmos Voraces (Greedy)")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(0.8)
    canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.restoreState()


# ----------------------------------------------------------------- contenido
s = []

# ---- Portada
s += [Spacer(1, 5 * cm),
      p("Actividad 8", SUB),
      p("Algoritmos Voraces (Greedy)", TITLE),
      p("Mochila fraccional y Cobertura de antenas", SUB),
      Spacer(1, 1.2 * cm),
      tabla([["Estudiante", ESTUDIANTE], ["Institución", INSTITUCION], ["Curso", CURSO],
             ["Lenguaje", "Python 3"],
             ["Contenido", "Explicación de la estrategia, análisis de complejidad, ejemplos de ejecución y validación"]],
            [3.5, 13.5], cabecera=False),
      PageBreak()]

# ---- 1. Introducción
s += [p("1. Introducción", H1),
      p("Un <b>algoritmo voraz (greedy)</b> construye la solución paso a paso. En cada paso toma la "
        "decisión que parece mejor en ese momento (la <i>elección local óptima</i>) y nunca la "
        "revisa. No funciona para cualquier problema: solo es correcto cuando el problema cumple dos "
        "propiedades:"),
      *bullets(["<b>Propiedad de elección voraz:</b> existe una solución óptima que contiene la elección "
                "local que hace el algoritmo.",
                "<b>Subestructura óptima:</b> después de hacer esa elección, lo que queda es un problema "
                "más pequeño del mismo tipo, cuya solución óptima se combina con la elección hecha."]),
      p("En esta actividad se resuelven dos problemas que cumplen ambas propiedades. Para cada uno se "
        "explica la estrategia, se justifica por qué es óptima, se analiza su complejidad con notación "
        "Big O y se muestran ejecuciones reales del código incluido en el repositorio."),
      p("Estructura del repositorio", H2),
      bloque_codigo("main.py                    Programa principal (menú interactivo)\n"
                    "src/mochila_fraccional.py  Problema 1\n"
                    "src/cobertura_antenas.py   Problema 2\n"
                    "tests/test_greedy.py       17 pruebas de validación\n"
                    "docs/                      Informe PDF y salidas de ejecución\n"
                    "README.md                  Cómo ejecutar el proyecto")]

# ---- 2. Mochila fraccional
s += [p("2. Problema 1: Mochila fraccional", H1),
      p("2.1 Enunciado resumido", H2),
      p("Se tiene una mochila con capacidad máxima <b>W</b> y <b>n</b> objetos, cada uno con un valor "
        "<i>v<sub>i</sub></i> y un peso <i>w<sub>i</sub></i>. Cada objeto existe una sola vez, pero se "
        "puede tomar una <b>fracción</b> de él. Se debe maximizar el valor total sin superar W."),
      p("2.2 Estrategia Greedy utilizada", H2),
      p("<b>Criterio:</b> la <b>densidad de valor</b> <i>d<sub>i</sub> = v<sub>i</sub> / w<sub>i</sub></i> "
        "(cuánto valor aporta cada unidad de peso). Los objetos se toman de mayor a menor densidad:"),
      *bullets(["Si el objeto cabe completo en el espacio restante, se toma completo.",
                "Si no cabe, se toma solo la fracción que llena exactamente la capacidad restante y el "
                "algoritmo termina, porque la mochila queda llena."]),
      p("Pseudocódigo", H2),
      bloque_codigo("MochilaFraccional(objetos, W):\n"
                    "    ordenar objetos por (valor / peso) de mayor a menor\n"
                    "    restante <- W ; valorTotal <- 0\n"
                    "    para cada objeto o en el orden obtenido:\n"
                    "        si restante = 0: terminar\n"
                    "        tomado <- min(o.peso, restante)\n"
                    "        valorTotal <- valorTotal + o.valor * (tomado / o.peso)\n"
                    "        restante <- restante - tomado\n"
                    "    retornar valorTotal"),
      p("2.3 ¿Por qué es óptimo? (argumento de intercambio)", H2),
      p("Supongamos una solución óptima que deja de usar peso de un objeto <i>A</i> de mayor densidad "
        "mientras usa peso de un objeto <i>B</i> de menor densidad. Se puede mover una pequeña cantidad "
        "ε de peso de <i>B</i> a <i>A</i>. El valor cambia en <i>ε·(d<sub>A</sub> − d<sub>B</sub>) ≥ 0</i>, "
        "es decir, no empeora. Repitiendo este intercambio se llega a la solución que construye el "
        "algoritmo voraz, así que esta también es óptima. Este argumento <b>depende de poder tomar "
        "fracciones</b>."),
      p("<b>Observación:</b> en la mochila 0/1 (sin fracciones) la misma estrategia falla. Con "
        "W = 50 y los objetos A(60, 10), B(100, 20), C(120, 30), el voraz toma A y B y obtiene 160, "
        "pero lo óptimo es B + C = 220. Por eso la versión 0/1 se resuelve con programación dinámica.")]

s += [p("2.4 Código (función principal)", H2),
      bloque_codigo(fuente(mochila_fraccional))]

# Traza ejemplo 1
s += [p("2.5 Traza paso a paso del Ejemplo 1 (capacidad 50)", H2),
      tabla([["Objeto", "Valor", "Peso", "Valor/Peso"],
             ["A", "60", "10", "6"], ["B", "100", "20", "5"], ["C", "120", "30", "4"]],
            [3, 3, 3, 3]),
      Spacer(1, 6),
      tabla([["Paso", "Objeto", "Capacidad restante antes", "Se toma", "Valor acumulado"],
             ["1", "A", "50", "10/10 (completo)", "60"],
             ["2", "B", "40", "20/20 (completo)", "160"],
             ["3", "C", "20", "20/30 (fracción 2/3)", "160 + 120·(20/30) = 240"]],
            [1.5, 2, 4.2, 4.3, 5]),
      Spacer(1, 6),
      p("Con A y B la mochila queda con 20 unidades libres; C pesa 30, así que solo se toma 20/30 de C. "
        "La mochila queda llena y el valor total es 240.")]

# ---- Complejidad mochila
s += [p("2.6 Análisis de complejidad", H2),
      tabla([["Parte del algoritmo", "Costo", "Justificación"],
             ["Cálculo de la densidad de cada objeto", "O(n)", "Una división por objeto."],
             ["Ordenamiento por densidad", "O(n log n)",
              "Ordenamiento por comparación (sorted de Python usa Timsort)."],
             ["Recorrido para llenar la mochila", "O(n)",
              "Un solo ciclo; cada objeto se procesa una vez con operaciones O(1)."],
             ["<b>Total (tiempo)</b>", "<b>O(n log n)</b>",
              "O(n) + O(n log n) + O(n) = O(n log n): el ordenamiento domina."],
             ["<b>Espacio</b>", "<b>O(n)</b>", "Lista ordenada y lista de selección."]],
            [5.2, 2.6, 9.2]),
      Spacer(1, 6),
      p("Si los objetos ya vinieran ordenados por densidad, el algoritmo costaría solo O(n). "
        "Con un montículo (heap) también podría hacerse en O(n + k log n) si solo se extraen "
        "los k objetos necesarios, pero el caso general sigue siendo O(n log n).")]

# Ejemplos mochila
s += [p("2.7 Ejemplos de ejecución", H2),
      p("Salida real obtenida con <font name='DVM'>python main.py --ejemplos</font>:", BODYK)]
ej = leer("salida_ejemplos.txt").split("\n\n")
s += [KeepTogether([p("<b>Ejemplo guía 1:</b> capacidad 50; A(60,10), B(100,20), C(120,30)"),
                    bloque_codigo("\n".join(ej[0].split("\n")[3:]))]),
      Spacer(1, 6),
      KeepTogether([p("<b>Ejemplo guía 2:</b> capacidad 25; A(80,20), B(100,10), C(120,30)"),
                    bloque_codigo("\n".join(ej[1].split("\n")[3:])),
                    p("Las densidades son B = 10, A = 4 y C = 4. A y C empatan, pero el resultado "
                      "(160) es el mismo con cualquier orden entre ellos, porque tienen la misma "
                      "densidad.")])]
extra = leer("salida_casos_extra.txt").split("\n\n")
s += [Spacer(1, 6),
      KeepTogether([p("<b>Caso propio:</b> capacidad 15 con 7 objetos "
                      "A(10,2), B(5,3), C(15,5), D(7,7), E(6,1), F(18,4), G(3,1)"),
                    bloque_codigo("\n".join(extra[0].split("\n")[1:])),
                    p("El orden por densidad es E (6), A (5), F (4.5), C (3), G (3), B (1.67), D (1). "
                      "D nunca se usa. B entra a 2/3 y aporta 5·(2/3) = 3.33. Total: "
                      "6 + 10 + 18 + 15 + 3 + 3.33 = 55.33.")]),
      Spacer(1, 6),
      p("<b>Casos borde:</b>", BODYK),
      bloque_codigo("\n\n".join(["\n".join(extra[1].split("\n")),
                                 "\n".join(extra[2].split("\n"))]))]

# ---- 3. Antenas
s += [p("3. Problema 2: Cobertura de antenas", H1),
      p("3.1 Enunciado resumido", H2),
      p("Hay <b>n</b> casas en posiciones enteras sobre una línea recta. Una antena colocada en "
        "<i>x</i> cubre el intervalo <b>[x − R, x + R]</b>. Se debe colocar la <b>menor cantidad</b> "
        "de antenas de modo que todas las casas queden cubiertas."),
      p("3.2 Estrategia Greedy utilizada", H2),
      p("<b>Criterio:</b> procesar las casas de izquierda a derecha y, para la primera casa aún sin "
        "cubrir, poner la antena <b>lo más a la derecha posible</b> sin dejar esa casa fuera: en "
        "<b>x = casa + R</b>. Esa antena cubre desde la casa hasta <i>casa + 2R</i>. Se saltan las casas "
        "cubiertas y se repite."),
      p("La idea es que la casa más a la izquierda sin cubrir <i>tiene</i> que ser cubierta por alguna "
        "antena. Entre todas las posiciones que la cubren, la de casa + R es la que llega más lejos "
        "hacia la derecha, así que cubre al menos tantas casas como cualquier otra opción."),
      p("Pseudocódigo", H2),
      bloque_codigo("CoberturaAntenas(casas, R):\n"
                    "    ordenar casas y quitar repetidas\n"
                    "    antenas <- lista vacía ; i <- 0\n"
                    "    mientras i < n:\n"
                    "        x <- casas[i] + R            // antena lo más a la derecha posible\n"
                    "        agregar x a antenas\n"
                    "        mientras i < n y casas[i] <= x + R:\n"
                    "            i <- i + 1               // saltar casas ya cubiertas\n"
                    "    retornar antenas"),
      p("3.3 ¿Por qué es óptimo? (el voraz \"va por delante\")", H2),
      p("Sean <i>g<sub>1</sub> &lt; g<sub>2</sub> &lt; … &lt; g<sub>k</sub></i> las antenas del voraz y "
        "<i>o<sub>1</sub> &lt; … &lt; o<sub>m</sub></i> las de cualquier solución válida. Se demuestra por "
        "inducción que <b>el alcance derecho de las primeras j antenas del voraz es mayor o igual que el de "
        "las primeras j antenas de cualquier otra solución</b>:"),
      *bullets(["<b>Base:</b> la primera casa p<sub>1</sub> debe ser cubierta por alguna antena "
                "<i>o<sub>1</sub> ≤ p<sub>1</sub> + R</i>, por lo que su alcance es a lo sumo "
                "<i>p<sub>1</sub> + 2R</i>, que es justo el de <i>g<sub>1</sub></i>.",
                "<b>Paso:</b> la primera casa que queda fuera del alcance de las j antenas del voraz "
                "también queda fuera del de la otra solución, que necesita otra antena para ella; esa "
                "antena no llega más lejos que la elegida por el voraz."]),
      p("Entonces el voraz nunca necesita más antenas que cualquier otra solución, es decir, "
        "<i>k ≤ m</i>, y por lo tanto es óptimo. Además, las pruebas incluyen una comparación contra "
        "fuerza bruta (sección 4).")]

s += [p("3.4 Código (función principal)", H2),
      bloque_codigo(fuente(cobertura_antenas))]

s += [p("3.5 Traza paso a paso del Ejemplo 1 (R = 5)", H2),
      p("Casas ordenadas: [1, 2, 7, 11, 20, 21, 30]"),
      tabla([["Paso", "Primera casa sin cubrir", "Antena en (casa + R)", "Cobertura [x − R, x + R]",
              "Casas cubiertas"],
             ["1", "1", "6", "[1, 11]", "1, 2, 7, 11"],
             ["2", "20", "25", "[20, 30]", "20, 21, 30"]],
            [1.4, 3.8, 3.8, 4, 4]),
      Spacer(1, 6),
      p("Resultado: antenas en 6 y 25, cantidad total = 2.")]

s += [p("3.6 Análisis de complejidad", H2),
      tabla([["Parte del algoritmo", "Costo", "Justificación"],
             ["Eliminar repetidas (set)", "O(n)", "Cada casa se inserta una vez en la tabla hash."],
             ["Ordenamiento de las posiciones", "O(n log n)", "Ordenamiento por comparación."],
             ["Ciclo principal (while + while interno)", "O(n)",
              "El índice i solo avanza y nunca retrocede. Cada casa se visita exactamente una vez, "
              "aunque haya dos ciclos anidados (análisis amortizado). Colocar una antena es O(1)."],
             ["<b>Total (tiempo)</b>", "<b>O(n log n)</b>", "O(n) + O(n log n) + O(n): el ordenamiento domina."],
             ["<b>Espacio</b>", "<b>O(n)</b>", "Lista ordenada de posiciones y lista de antenas."]],
            [5.2, 2.6, 9.2]),
      Spacer(1, 6),
      p("Aunque el ciclo interno está dentro del externo, no es O(n²): el número total de incrementos "
        "de <i>i</i> entre ambos ciclos es n. Si la entrada ya estuviera ordenada, el costo bajaría a O(n).")]

# Ejemplos antenas
s += [p("3.7 Ejemplos de ejecución", H2),
      KeepTogether([p("<b>Ejemplo guía 1:</b> casas [1,2,7,11,20,21,30], R = 5"),
                    bloque_codigo("\n".join(ej[2].split("\n")[4:]))]),
      Spacer(1, 6),
      KeepTogether([p("<b>Ejemplo guía 2:</b> casas [2,4,8,15,18,22], R = 3"),
                    bloque_codigo("\n".join(ej[3].split("\n")[4:])),
                    p("Traza: 2 → antena en 5 (cubre [2, 8]: casas 2, 4, 8); 15 → antena en 18 "
                      "(cubre [15, 21]: casas 15, 18); 22 → antena en 25 (cubre [22, 28]). Total: 3.")]),
      Spacer(1, 6),
      KeepTogether([p("<b>Caso propio:</b> casas desordenadas y con repetidas "
                      "[30,1,2,2,7,11,21,20,50,52], R = 5"),
                    bloque_codigo("\n".join(extra[3].split("\n")[2:])),
                    p("Al ordenar y quitar repetidas queda [1, 2, 7, 11, 20, 21, 30, 50, 52]. Las dos "
                      "primeras antenas son las mismas del ejemplo guía 1 y las casas 50 y 52 necesitan "
                      "una tercera antena, en 55.")]),
      Spacer(1, 6),
      p("<b>Casos borde:</b>", BODYK),
      bloque_codigo("\n\n".join(["\n".join(extra[4].split("\n")),
                                 "\n".join(extra[5].split("\n")),
                                 "\n".join(extra[6].split("\n"))]))]

# ---- 4. Validación
s += [p("4. Validación de casos", H1),
      p("Las pruebas están en <font name='DVM'>tests/test_greedy.py</font> y se ejecutan con "
        "<font name='DVM'>python -m unittest discover -v</font>. Resultado: <b>17 pruebas, todas "
        "aprobadas</b>."),
      tabla([["Problema", "Caso validado", "Qué comprueba"],
             ["Mochila", "Ejemplos 1 y 2 de la guía", "Valor 240 y 160 y el orden de selección."],
             ["Mochila", "Capacidad 0", "No se selecciona nada; valor 0."],
             ["Mochila", "Capacidad mayor que el peso total", "Se toman todos los objetos completos."],
             ["Mochila", "Lista de objetos vacía", "Retorna selección vacía y valor 0."],
             ["Mochila", "Pesos y capacidad decimales", "Cálculo exacto con fracciones."],
             ["Mochila", "Peso ≤ 0 o capacidad negativa", "Lanza ValueError (entrada inválida)."],
             ["Mochila", "200 casos aleatorios", "Nunca se excede la capacidad."],
             ["Antenas", "Ejemplos 1 y 2 de la guía", "Posiciones [6, 25] y [5, 18, 25]."],
             ["Antenas", "Sin casas / una sola casa", "Lista vacía / una antena."],
             ["Antenas", "Casas desordenadas y repetidas", "El resultado no depende del orden de entrada."],
             ["Antenas", "R = 0", "Una antena por cada posición distinta."],
             ["Antenas", "R negativo", "Lanza ValueError."],
             ["Antenas", "300 casos aleatorios vs. fuerza bruta",
              "Todas las casas quedan cubiertas y la cantidad de antenas es igual al mínimo real."]],
            [2.3, 6.2, 8.5]),
      Spacer(1, 8),
      p("Salida de la ejecución de las pruebas", H2),
      bloque_codigo(leer("salida_pruebas.txt").replace("\n\n", "\n"))]

# ---- 5. Cómo ejecutar
s += [p("5. Cómo ejecutar el proyecto", H1),
      bloque_codigo("python main.py              # menú interactivo\n"
                    "python main.py --ejemplos   # ejemplos guía de la actividad\n"
                    "python -m unittest discover -v   # pruebas de validación"),
      p("Solo se usa la biblioteca estándar de Python 3.8 o superior. En el menú, la mochila se ingresa "
        "como <font name='DVM'>nombre valor peso</font> (uno por línea) y las casas como una lista de "
        "enteros separados por espacios o comas.")]

# ---- 6. Conclusiones
s += [p("6. Conclusiones", H1),
      *bullets(["Ambos problemas cumplen la propiedad de elección voraz, por eso una decisión local "
                "(mayor valor/peso; antena lo más a la derecha posible) lleva a la solución global óptima.",
                "En los dos casos el ordenamiento domina el costo y ambos algoritmos son "
                "<b>O(n log n)</b> en tiempo y <b>O(n)</b> en espacio.",
                "La mochila fraccional es óptima con greedy solo porque se permiten fracciones; en la "
                "versión 0/1 hay que usar programación dinámica.",
                "Se validaron los resultados con los ejemplos de la guía, casos borde y una comparación "
                "contra fuerza bruta."])]

doc = SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=2 * cm, bottomMargin=2.2 * cm,
                        title="Actividad 8 - Algoritmos Voraces (Greedy)", author=ESTUDIANTE)
doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=pie)
print("PDF generado:", SALIDA)
