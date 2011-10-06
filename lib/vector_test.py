import unittest
from vector import Vector2, Vector3

class TestVector2(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector2(0, 0)
        self.v2 = Vector2(1, 1)
        self.v3 = Vector2(-1, -1)
        self.v4 = Vector2(1.5, 1.5)
        self.v5 = Vector2(14, -6)

    def test_equality(self):
        self.assertTrue(self.v1 == self.v1)
        self.assertTrue(self.v1 != self.v3)
        self.assertTrue(self.v1 == Vector2(0,0))
        self.assertTrue(self.v1 == 0)

    def test_addition(self):
        self.assertEqual(self.v2, self.v1 + self.v2)
        self.assertEqual(self.v2, self.v2 + self.v1)
        self.v1 += self.v2
        self.assertEqual(self.v2, self.v1)
        self.assertEqual(self.v2, self.v1 + 1)
        self.assertEqual(self.v4, self.v2 + 0.5)

    def test_subtraction(self):
        self.assertEqual(self.v2, self.v2 - self.v1)
        self.assertEqual(self.v3, self.v1 - self.v2)
        self.v1 -= self.v2
        self.assertEqual(self.v3, self.v1)
        self.assertEqual(self.v1, self.v2 - 1)
        self.assertEqual(self.v2, self.v4 - 0.5)

    def test_multiplication(self):
        self.assertEqual(self.v1, self.v1 * 1)
        self.assertEqual(self.v1, self.v1 * 1.0)
        self.assertEqual(self.v1, self.v2 * 0)
        self.assertEqual(self.v1, self.v3 * 0)
        self.assertEqual(Vector2(2.25, 2.25), 1.5 * self.v4)
        self.assertEqual(Vector2(-70, 30), self.v5 * -5)
        self.assertEqual(self.v1, self.v1 * self.v1)
        self.assertEqual(self.v5, self.v5 * self.v2)

    def test_division(self):
        self.assertEqual(self.v1, self.v1 / 1)
        self.assertEqual(self.v1, self.v1 / 1.0)
        self.assertEqual(self.v2, self.v3 / 1.5)

    def test_modulo(self):
        self.assertEqual(Vector2(2, -1), self.v5 % 5)


class TestVector3(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector3(0, 0, 0)
        self.v2 = Vector3(1, 1, 1)
        self.v3 = Vector3(-1, -1, -1)
        self.v4 = Vector3(1.5, 1.5, 1.5)
        self.v5 = Vector3(14, -6, 33)

    def test_equality(self):
        self.assertTrue(self.v1 == self.v1)
        self.assertTrue(self.v1 != self.v3)
        self.assertTrue(self.v1 == Vector3(0,0,0))
        self.assertTrue(self.v1 == 0)

    def test_addition(self):
        self.assertEqual(self.v2, self.v1 + self.v2)
        self.assertEqual(self.v2, self.v2 + self.v1)
        self.v1 += self.v2
        self.assertEqual(self.v2, self.v1)
        self.assertEqual(self.v2, self.v1 + 1)
        self.assertEqual(self.v4, self.v2 + 0.5)

    def test_subtraction(self):
        self.assertEqual(self.v2, self.v2 - self.v1)
        self.assertEqual(self.v3, self.v1 - self.v2)
        self.v1 -= self.v2
        self.assertEqual(self.v3, self.v1)
        self.assertEqual(self.v1, self.v2 - 1)
        self.assertEqual(self.v2, self.v4 - 0.5)

    def test_multiplication(self):
        self.assertEqual(self.v1, self.v1 * 1)
        self.assertEqual(self.v1, self.v1 * 1.0)
        self.assertEqual(self.v1, self.v2 * 0)
        self.assertEqual(self.v1, self.v3 * 0)
        self.assertEqual(Vector3(2.25, 2.25, 2.25), 1.5 * self.v4)
        self.assertEqual(Vector3(-70, 30, -165), self.v5 * -5)
        self.assertEqual(self.v1, self.v1 * self.v1)
        self.assertEqual(self.v5, self.v5 * self.v2)

    def test_division(self):
        self.assertEqual(self.v1, self.v1 / 1)
        self.assertEqual(self.v1, self.v1 / 1.0)
        self.assertEqual(self.v2, self.v3 / 1.5)

    def test_modulo(self):
        self.assertEqual(Vector3(2, -1, 6), self.v5 % 5)

    def test_to_Vector2(self):
        self.assertEqual(Vector2(14, -6), self.v5.to_Vector2())
