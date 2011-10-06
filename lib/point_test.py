import unittest
from point import Point

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.a = Point(0, 0)

    def test_equality(self):
        self.assertEqual(Point(0,0), Point(0,0))
        self.assertNotEqual(Point(1,0), Point(0,0))
        self.assertNotEqual(Point(0,1), Point(0,0))

    def test_addition(self):
        a = Point(1, 1)
        b = Point(2, 2)
        self.assertEqual(Point(3, 3), a + b)
        self.assertEqual(Point(3, 3), b + a)

    def test_subtraction(self):
        a = Point(1, 1)
        b = Point(2, 2)
        self.assertEqual(Point(1, 1), b - a)
        self.assertEqual(Point(-1, -1), a - b)
        self.assertEqual(a, a - Point(0,0))

    def test_from_tuple(self):
        a = Point(1, 2)
        b = (3, 4)
        self.assertEqual(a + b, Point(4, 6))
        self.assertEqual(b + a, Point(4, 6))
        self.assertEqual(a - b, Point(-2, -2))
        self.assertEqual(b - a, Point(2, 2))

    def test_multiply(self):
        a = Point(1, 0)
        self.assertEqual(a * 10, Point(10, 0))
        self.assertEqual(a * 10.0, Point(10, 0))
        self.assertRaises(ValueError, lambda: a * "not an integer")

    def test_distance(self):
        a = Point(0, 0)
        b = Point(3, 4)
        c = Point(-3, -4)
        d = Point(1, 1)
        self.assertEqual(a.distance(b), 5)
        self.assertEqual(b.distance(a), 5)
        self.assertEqual(a.distance(c), 5)
        self.assertEqual(a.pythagorean_distance_squared(b), 25)
        self.assertAlmostEqual(a.distance(d), 1.414, places=3)

    def test_constrain(self):
        """simulate a boundary which all points must be inside"""
        top_left = Point(0, 0)
        size = Point(20, 20)
        points = {
            # name -> (start, constrained)
            'too_far_left': (Point(-10, 0), Point(0, 0)),
            'too_far_up': (Point(10, -10), Point(10, 0)),
            'too_far_right': (Point(30, 10), Point(20, 10)),
            'too_far_down': (Point(10, 30), Point(10,20)),
            'way_off': (Point(-4000, 4000), Point(0, 20)),
            'ok': (Point(10, 10), Point(10,10))
        }
        for name, point in points.items():
            start, end = point
            start.constrain(top_left, size)
            self.assertEqual(start, end, name)


if __name__ == "__main__":
    unittest.main()

