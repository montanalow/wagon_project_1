import math

import pygame

from lib.game import GameState
from lib.point import Point

class Painter(object):
    # flags

    # scroll_direction
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8

    SCROLL_SPEED = 1

    font = None
    
    def __init__(self, parent_painter, size = Point(0, 0), relative_position = Point(0, 0, 0), surface = None, scroll = None):
        if parent_painter and size == Point(0, 0):
            size = parent_painter.get_size()
        if surface is None:
            surface = pygame.Surface(size.to_vector2()).convert_alpha()
        self._scale = 16
        if parent_painter:
            self._scale = parent_painter._scale
        self._parent_painter = parent_painter
        self._surface = surface
        self._scaled_surfaces = {}
        self._scaled_surfaces[self._scale] = self._surface
        self._size = size
        self._scroll = scroll
        self._relative_position = relative_position

        self.__set_absolute_position()
        self.__set_scaled_position()
        self._rotation = None

        self._index = dict()

        self.set_scale(self._scale)
        self.set_relative_position(relative_position)


        self._scroll_direction = 0
        self._dirty = True
        if self._parent_painter:
            self._parent_painter.append(self)

    def set_size(self, size):
        self._size = Point(size)

    def get_size(self):
        return self._size

    def set_surface(self, surface):
        self._surface = surface
        self._scaled_surfaces = dict()
        self.set_scale(self._scale)

    def set_scale(self, scale):
        self._relative_position /= self._scale
        self._scale = scale
        if self._relative_position:
            self.set_relative_position(self._relative_position * self._scale)
        if self._scale not in self._scaled_surfaces:
            self._scaled_surfaces[self._scale] = pygame.transform.scale(self._surface, (self._surface.get_width() * self._scale / 16, self._surface.get_height() * self._scale / 16))
        self.__set_scaled_position()
        self.__bound_check_scroll()
        self.__set_viewable_surface()
        self.set_dirty()
        for z in sorted(self._index.iterkeys()):
            for y in sorted(self._index[z].iterkeys()):
                for x in sorted(self._index[z][y].iterkeys()):
                    for painter in self._index[z][y][x]:
                        painter.set_scale(scale)


    def set_relative_position(self, relative_position):
        self._relative_position = relative_position
        self.__set_absolute_position()
        self.__set_scaled_position()
        self.__set_viewable_surface()

    def __set_scaled_position(self):
#        if self._parent_painter and self._scaled_position:
#            self._parent_painter.remove(self)
        self._scaled_position = Point(
            self._relative_position.x / self._scale,
            self._relative_position.y / self._scale,
            self._relative_position.z / self._scale
        )
#        if self._parent_painter:
#            self._parent_painter.append(self)

    def __set_absolute_position(self):
        if self._parent_painter:
            self._absolute_position = self._parent_painter._absolute_position + self._relative_position
            if self._parent_painter._scroll:
                self._absolute_position -= self._parent_painter._scroll
        else:
            self._absolute_position = Point(0, 0, 0)

    def __set_viewable_surface(self):
        if self._scale in self._scaled_surfaces:
            self.__viewable_surface = self._scaled_surfaces[self._scale]
        else:
            self.__viewable_surface = self._surface.copy()
        self.__set_absolute_position()
        if self._rotation:
            self.__viewable_surface = pygame.transform.rotate(self.__viewable_surface, self._rotation * 180 / math.pi % 360)
        if self._scroll:
            viewable_area = pygame.Rect(self._scroll.to_vector2(), self.get_size().to_vector2()).clamp(self.__viewable_surface.get_rect()).clip(self.__viewable_surface.get_rect())
            self.__viewable_surface = self.__viewable_surface.subsurface(viewable_area)

    def append(self, painter):
        if painter._scaled_position.x not in self._index:
            self._index[painter._scaled_position.x] = dict()
        if painter._scaled_position.y not in self._index[painter._scaled_position.x]:
            self._index[painter._scaled_position.x][painter._scaled_position.y] = dict()
        if painter._scaled_position.z not in self._index[painter._scaled_position.x][painter._scaled_position.y]:
            self._index[painter._scaled_position.x][painter._scaled_position.y][painter._scaled_position.z] = list()
        self._index[painter._scaled_position.x][painter._scaled_position.y][painter._scaled_position.z].append(painter)

    def remove(self, painter):
        self._index[painter._scaled_position.x][painter._scaled_position.y][painter._scaled_position.z].remove(painter)

    def update(self, elapsed):
        self._dirty = False
        self.scroll(elapsed)
        self.__set_viewable_surface()
    
    def paint(self, elapsed):
        if self._dirty:
            self.update(elapsed)
        GameState.main_surface.blit(self.__viewable_surface, self._absolute_position.to_vector2())
        for z in sorted(self._index.iterkeys()):
            for y in sorted(self._index[z].iterkeys()):
                for x in sorted(self._index[z][y].iterkeys()):
                    for painter in self._index[z][y][x]:
                        painter.paint(elapsed)

    def set_size(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_scroll_direction(self, direction):
        if direction:
            self._scroll_direction |= direction
        else:
            self._scroll_direction = 0
        self.set_dirty() # is this really necessary?

    def scroll(self, elapsed):
        if self._scroll_direction:
            distance = elapsed * Painter.SCROLL_SPEED
            if self._scroll_direction & Painter.NORTH:
                self._scroll_north(distance)
            elif self._scroll_direction & Painter.SOUTH:
                self._scroll_south(distance)
            if self._scroll_direction & Painter.EAST:
                self._scroll_east(distance)
            elif self._scroll_direction & Painter.WEST:
                self._scroll_west(distance)
            self.__bound_check_scroll()
            self.set_dirty()

    def _scroll_north(self, distance):
        self._scroll -= (0, distance)

    def _scroll_south(self, distance):
        self._scroll += (0, distance)

    def _scroll_east(self, distance):
        self._scroll -= (distance, 0)

    def _scroll_west(self, distance):
        self._scroll += (distance, 0)

    def __bound_check_scroll(self):
        if self._scroll:
            limit = self._scaled_surfaces[self._scale].get_size() - self.get_size()
            limit.constrain(Point(0, 0), Point(*self._scaled_surfaces[self._scale].get_size()))
            self._scroll.constrain(Point(0, 0), limit)

    def set_dirty(self, dirty = True):
        self._dirty = dirty
