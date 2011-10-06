import math

class Point(object):
    # we're going to have a lot of these, so don't let the VM make an attribute
    # dict for each one (use __slots__)
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __unicode__(self):
        return "<Point: x:%d y:%d z:%d>" % (self.x, self.y, self.z)

    def __list__(self):
        return (self.x, self.y, self.z)

    __repr__ = __unicode__

    def __add__(self, other):
        if isinstance(other, (tuple, list)) and len(other) > 1 and len(other) < 4:
            return self + Point(*other)
        elif isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Point objects can only be added to 2 or 3 element "
                            "tuples or other point objects!")
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (tuple,list)) and len(other) > 1 and len(other) < 4:
            return self - Point(*other)
        elif isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Point objects can only be subtracted from 2 or 3 "
                            "element tuples or other point objects!")

    def __rsub__(self, other):
        if isinstance(other, (tuple,list)) and len(other) > 1 and len(other) < 4:
            return Point(*other) - self
        elif isinstance(other, Point):
            return Point(other.x - self.x, other.y - self.y, other.z - self.z)
        else:
            raise TypeError("Point objects can only be subtracted from 2 "
                            "element tuples or other point objects!")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    __req__ = __eq__

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        return Point(self.x / other, self.y / other, self.z / other)

    def pythagorean_distance_squared(self, other):
        abs_dif = Point(abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z))
        return pow(abs_dif.x, 2) + pow(abs_dif.y, 2) + pow(abs_dif.z, 2)

    def pythagorean_distance(self, other):
        return math.sqrt(self.pythagorean_distance_squared(other))

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def diagnol_distance(self, other):
        diag = min(abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z))
        manh = self.manhattan_distance(other)
        return 1.41 * diag + (manh - (2 * diag))

    def distance(self, other):
        return self.pythagorean_distance(other)

    def constrain(self, top_left, size):
        self.x = max(self.x, top_left.x)
        self.x = min(self.x, top_left.x + size.x)
        self.y = max(self.y, top_left.y)
        self.y = min(self.y, top_left.y + size.y)
        self.z = max(self.z, top_left.z)
        self.z = min(self.z, top_left.z + size.z)

    def list(self):
        return (self.x, self.y, self.z)

    def to_vector2(self):
        return (self.x, self.y)
