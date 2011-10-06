import pygame

from lib.game import GameState
from lib.painter import Painter
from lib.point import Point
from lib.event import UPDATE_FPS_PAINTER_EVENT

class FPSPainter(Painter):
    def __init__(self, parent_painter, size = Point(0, 0), relative_position = Point(0, 0, 1000), surface = None):
        Painter.__init__(self, parent_painter, size, relative_position, surface)
        pygame.time.set_timer(UPDATE_FPS_PAINTER_EVENT, 1000)

    def update(self, elapsed):
        Painter.update(self, elapsed)
        self.set_surface(Painter.font.render("FPS: %0.2f" % GameState.clock.get_fps(), True, (255,255,255)))
