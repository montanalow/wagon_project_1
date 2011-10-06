import math
import operator

class Vector2(tuple):
    __slots__ = ()
    _fields = ('x', 'y')
    x = property(operator.itemgetter(0), doc='X coordinate')
    y = property(operator.itemgetter(1), doc='Y coordinate')

    def __new__(_cls, x, y):
        return tuple.__new__(_cls, (x, y))

    def __unicode__(self):
        return "<Vector2: x:%d y:%d>" % (self.x, self.y)
    __str__ = __unicode__
    __repr__ = __unicode__

    def __scalar_operation(self, operation, scalar):
        return Vector2(operation(self.x, scalar),
                       operation(self.y, scalar))

    def __vector_operation(self, operation, other):
        return Vector2(operation(self.x, other.x),
                       operation(self.y, other.y))

    def __get_call(self, operation, other):
        """given a binary operator, determine whether to do a scalar or vector
        application of the operator and this object.
        """
        # default to doing vector operations with other vectors
        call = self.__vector_operation
        if isinstance(other, (int,float,long,complex)):
            # if a numeric type came in, do a scalar operation on each element
            call = self.__scalar_operation
        return call(operation, other)

    """
    OPERATORS
    """
    def __add__(self, other):
        return self.__get_call(operator.add, other)

    def __sub__(self, other):
        return self.__get_call(operator.sub, other)

    def __mul__(self, other):
        return self.__get_call(operator.mul, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self.__get_call(operator.div, other)

    def __mod__(self, other):
        return self.__get_call(operator.mod, other)

    def __eq__(self, other):
        return self.__get_call(operator.eq, other)
    __req__ = __eq__


class Vector3(Vector2):
    __slots__ = ()
    _fields = ('x', 'y', 'z')
    z = property(operator.itemgetter(2), doc='Z coordinate')

    def __new__(_cls, x, y, z):
        return tuple.__new__(_cls, (x, y, z))

    def __unicode__(self):
        return "<Vector3: x:%d y:%d z:%d>" % (self.x, self.y, self.z)
    __str__ = __unicode__
    __repr__ = __unicode__

    def __scalar_operation(self, operation, scalar):
        return Vector3(operation(self.x, scalar),
                       operation(self.y, scalar),
                       operation(self.z, scalar))

    def __vector_operation(self, operation, other):
        return Vector3(operation(self.x, other.x),
                       operation(self.y, other.y),
                       operation(self.z, other.z))

    """
    PUBLIC INTERFACE
    """
    def to_Vector2(self):
        return Vector2(self.x, self.y)

if __name__ == "__main__":
    def vector2_fun():
        for i in xrange(10000):
            v = Vector2(i,i)
            v2 = Vector2(-i,i)
            v2 *= v
            v2 == v
            
    def vector3_fun():
        for i in xrange(10000):
            v = Vector3(i,i,i)
            v2 = Vector3(-i,-i,-i)
            v2 *= v
            v2 == v


    try:
        import cProfile as prof
    except ImportError:
        import profile as prof
    import pstats
    prof.run('vector2_fun()', 'vector2_prof')
    prof.run('vector3_fun()', 'vector3_prof')
    
    p = pstats.Stats('vector2_prof')
    p.strip_dirs().sort_stats('cumulative').print_stats()
    
    p = pstats.Stats('vector3_prof')
    p.strip_dirs().sort_stats('cumulative').print_stats()
