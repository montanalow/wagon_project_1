from lib.point import Point
#import lib.game as G

class BaseObject(object):
    __slots__ = ('__id', '__pos', '__dirty', '__name')
    NEXT_ID = 0
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, position):
        self.__id = BaseObject.NEXT_ID
        BaseObject.NEXT_ID += 1

        self.__pos = position
        self.__dirty = True # so it gets drawn on the first frame
        self.__name = "BASEOBJECT"

    def name(self):
        return self.__name

    def is_dirty(self):
        return self.__dirty

    def position(self):
        return self.__pos

    def set_position(self, point):
        self.__dirty = True
        self.__pos = point

    def move(self, delta):
        # this move does not respect map tiles, used for cursors, notes etc...
        # mark ourselves as updated
        self.__dirty = True
        new_pos = self.__pos + delta
        #new_pos.constrain(Point(1, 1), Point(G.state.level().w - 3,
        #                                     G.state.level().h - 3))
        self.__pos = new_pos

    def draw(self, screen):
        self.__dirty = False
        # just draw a 10x10 red rect
        pygame.draw.rect(screen, (255,0,0), (self.__pos, (10,10)))

    def clear(self, con):
        """erase the character that represents this object"""
        self.__dirty = True

    def update(self, elapsed):
        """Anything that isn't drawing"""
        pass
