"""Pruebas de validacion de ambos algoritmos Greedy."""

import itertools
import random
import unittest
from fractions import Fraction

from src.mochila_fraccional import Objeto, mochila_fraccional
from src.cobertura_antenas import cobertura_antenas


def cubre_todo(casas, antenas, R):
    """Verifica que cada casa este a distancia <= R de alguna antena."""
    return all(any(abs(c - a) <= R for a in antenas) for c in casas)


def minimo_bruto(casas, R):
    """Fuerza bruta: menor cantidad de antenas probando todas las combinaciones."""
    candidatas = range(min(casas) - R, max(casas) + R + 1)
    for k in range(1, len(casas) + 1):
        for combo in itertools.combinations(candidatas, k):
            if cubre_todo(casas, combo, R):
                return k


class TestMochila(unittest.TestCase):
    def test_ejemplo_1(self):
        objs = [Objeto("A", 60, 10), Objeto("B", 100, 20), Objeto("C", 120, 30)]
        sel, total = mochila_fraccional(objs, 50)
        self.assertEqual(total, 240)
        self.assertEqual([(o.nombre, t) for o, t in sel],
                         [("A", 10), ("B", 20), ("C", 20)])

    def test_ejemplo_2(self):
        objs = [Objeto("A", 80, 20), Objeto("B", 100, 10), Objeto("C", 120, 30)]
        sel, total = mochila_fraccional(objs, 25)
        self.assertEqual(total, 160)
        self.assertEqual([(o.nombre, t) for o, t in sel], [("B", 10), ("A", 15)])

    def test_capacidad_cero(self):
        sel, total = mochila_fraccional([Objeto("A", 10, 5)], 0)
        self.assertEqual((sel, total), ([], 0))

    def test_capacidad_mayor_que_todo(self):
        objs = [Objeto("A", 10, 5), Objeto("B", 20, 5)]
        sel, total = mochila_fraccional(objs, 100)
        self.assertEqual(total, 30)
        self.assertEqual(len(sel), 2)

    def test_sin_objetos(self):
        self.assertEqual(mochila_fraccional([], 10), ([], 0))

    def test_decimales(self):
        sel, total = mochila_fraccional([Objeto("A", 10, 4)], 1.5)
        self.assertEqual(total, Fraction(15, 4))

    def test_peso_invalido(self):
        with self.assertRaises(ValueError):
            Objeto("X", 10, 0)

    def test_capacidad_negativa(self):
        with self.assertRaises(ValueError):
            mochila_fraccional([Objeto("A", 1, 1)], -5)

    def test_nunca_excede_capacidad(self):
        random.seed(1)
        for _ in range(200):
            objs = [Objeto(i, random.randint(1, 50), random.randint(1, 30))
                    for i in range(random.randint(1, 8))]
            cap = random.randint(0, 100)
            sel, _ = mochila_fraccional(objs, cap)
            self.assertLessEqual(sum(t for _, t in sel), cap)


class TestAntenas(unittest.TestCase):
    def test_ejemplo_1(self):
        self.assertEqual(cobertura_antenas([1, 2, 7, 11, 20, 21, 30], 5), [6, 25])

    def test_ejemplo_2(self):
        self.assertEqual(cobertura_antenas([2, 4, 8, 15, 18, 22], 3), [5, 18, 25])

    def test_sin_casas(self):
        self.assertEqual(cobertura_antenas([], 5), [])

    def test_una_casa(self):
        self.assertEqual(cobertura_antenas([10], 0), [10])

    def test_desordenadas_y_repetidas(self):
        self.assertEqual(cobertura_antenas([30, 1, 2, 2, 7, 11, 21, 20], 5), [6, 25])

    def test_R_cero(self):
        self.assertEqual(len(cobertura_antenas([1, 2, 3], 0)), 3)

    def test_R_negativo(self):
        with self.assertRaises(ValueError):
            cobertura_antenas([1, 2], -1)

    def test_optimalidad_vs_fuerza_bruta(self):
        """Compara con fuerza bruta en 300 casos aleatorios pequenos."""
        random.seed(7)
        for _ in range(300):
            casas = [random.randint(0, 14) for _ in range(random.randint(1, 6))]
            R = random.randint(0, 4)
            antenas = cobertura_antenas(casas, R)
            self.assertTrue(cubre_todo(casas, antenas, R))
            self.assertEqual(len(antenas), minimo_bruto(casas, R))


if __name__ == "__main__":
    unittest.main()
