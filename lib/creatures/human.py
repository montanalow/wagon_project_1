import math
import random

import pygame

#import lib.game as G
from lib.point import Point
from lib.base_object import BaseObject
from lib.painter import Painter

class Human(BaseObject,Painter):
    SPEED = 0.005
    WIDTH = 1
    HEIGHT = 1
    COLOR = (200,200,50)
    all = list()

    def __init__(self, game_map, position):
        # Place a human on the map
        position = Point(position.x, position.y, 5) - (Point(Human.WIDTH / 2, Human.HEIGHT / 2) * game_map._scale)
        self._scale = 16
        surface = pygame.Surface((Human.WIDTH * self._scale, Human.HEIGHT * self._scale)).convert_alpha()
        top = (Human.WIDTH * self._scale / 2, 0)
        left = (0, Human.HEIGHT * self._scale)
        right = (Human.WIDTH * self._scale, Human.HEIGHT * self._scale)
        pygame.draw.polygon(surface, Human.COLOR, (top, left, right), 1)
        
        Painter.__init__(self, game_map, Point(Human.WIDTH, Human.HEIGHT), position, surface)
        Human.all.append(self)
        self._direction = 0
        self._target = None

    def set_target(self, target):
        self._target = target

    def update(self, elapsed):
        Painter.update(self, elapsed)
        self.set_dirty() # always dirty

        # choose steering
        if self._target:
            # steer toward target
            target_direction = math.atan((self._target.x - self._relative_position.x)/(self._target.y - self._relative_position.y))
            if self._target.y < self._relative_position.y:
                target_direction += math.pi
            target_direction %= math.pi * 2
            delta = (target_direction - self._direction)
            if (target_direction > self._direction and delta < math.pi) or (target_direction < self._direction and math.fabs(delta) > math.pi):
                self._direction = (self._direction + 0.1) % (math.pi * 2)
            else:
                self._direction = (self._direction - 0.1) % (math.pi * 2)
        else:
            # wander
            self._direction += (random.random() - 0.5) % (math.pi * 2)

        # update position
        distance = elapsed * Human.SPEED * self._scale
        self.set_relative_position(self._relative_position + Point(math.sin(self._direction) * distance, math.cos(self._direction) * distance))

        self._rotation = self._direction

        
        """
        if self.__path:
            half_cell = G.CELL_SIZE / 2
            for point in self.__path:

                pygame.draw.circle(screen, (255,255,0),
                                   (G.CELL_SIZE * point.x + half_cell,
                                    G.CELL_SIZE * point.y + half_cell),
                                   half_cell / 2)
        """
