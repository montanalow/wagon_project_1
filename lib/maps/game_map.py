import logging
import os

import pygame

from lib.point import Point
from lib.base_object import BaseObject
from lib.creatures.human import Human
from lib.maps.pathfinder import AStarPathFinder
from lib.painter import Painter

class Tile(BaseObject):
    __slots__ = ('color', 'blocks_vision', 'blocks_move')
    def __init__(self, pos, color, blocks_vision=False, blocks_move=False):
        BaseObject.__init__(self, pos)

    def __unicode__(self):
        chunks = ["<Tile@%s" % self.position()]
        for k in Tile.__slots__:
            chunks.append(" %s: %s" % (k, getattr(self, k)))
        chunks.append(">")
        return "".join(chunks)
    __repr__ = __unicode__


class Ping(Painter):
    TIMEOUT = 1000
    RADIUS = 100

    def __init__(self, game_map, position):
        """Place a circular notification on the map that will disappear after
        *timeout* milliseconds
        """
        position = Point(position.x, position.y, 1000) - (Point(Ping.RADIUS, Ping.RADIUS) * (float(game_map._scale) / 16))
        Painter.__init__(self, game_map, Point(Ping.RADIUS * 2 / (float(game_map._scale) / 16), Ping.RADIUS * 2 / (float(game_map._scale) / 16)), position)
        self.__age = 0 # in ms

    def expired(self):
        return self.__age > Ping.TIMEOUT

    def update(self, elapsed):
        Painter.update(self, elapsed)
        self.set_dirty()
        self.__age += elapsed
        if self.expired():
            self._parent_painter.remove(self)
        else:
            progress = self.__age / float(Ping.TIMEOUT)
            color = pygame.color.Color(255, 0, 0, 255 - int(255 * progress))
            self._surface.fill(pygame.Color(0,0,0,0))
            pygame.draw.circle(self._surface, color, (Ping.RADIUS, Ping.RADIUS), max(4, int(Ping.RADIUS * progress)), 1)
        self.set_surface(self._surface)


class GameMap(Painter):
    def __init__(self, view_size, parent_painter):
        self._log = logging.getLogger("map")
        print "building mountains"
        terrain = pygame.image.load(os.path.abspath(os.path.join("media", "PerlinNoise2d.png"))).convert()
        self.coordinates = []
        terrain_array = pygame.surfarray.pixels2d(terrain)
        for x in xrange(0, len(terrain_array)):
            self.coordinates.append([])
            for y in xrange(0, len(terrain_array[x])):
                h, s, v, a = terrain.unmap_rgb(terrain_array[x][y]).hsva
                if v < 50: # water
                    self.coordinates[x].append(False)
                    terrain_array[x][y] = terrain.map_rgb(70 - (50 - v), 70 - (50 - v), 100 + v * 2)
                else: # land
                    self.coordinates[x].append(True)
                    terrain_array[x][y] = terrain.map_rgb(70 - v * 0.1, v * 1.5, 40 + v * 0.3)

        print "digging oceans"
        surface = pygame.transform.scale(terrain, (terrain.get_width() * 16, terrain.get_height() * 16))
        Painter.__init__(self, parent_painter, Point(0,0), Point(0,0,0), surface, Point(0,0))

#        self.path_finder = AStarPathFinder(self) # this can be used for all units

#    def tile_at_position(self, pos):
#        if pos.y >= 0 and pos.y < len(self.rows) and pos.x >= 0 and \
#           pos.x < len(self.rows[0]):
#            return self.rows[pos.y][pos.x]
#        return None

    def ping(self, position):
        ping = Ping(self, position)
        for human in Human.all:
            center = Ping.RADIUS * (float(self._scale) / 16)
            human.set_target(ping._relative_position + Point(center, center))
#            human.set_path(self.path_finder.find_path(human.center(), ping.center()))

    def add_human(self, position):
        Human(self, position)


    def update(self, elapsed):
        Painter.update(self, elapsed)
#        self._surface = terrain#.subsurface(self._view)
        # ugly hack to pre-populate the grid
        """
                h,s,v,a = self.height_map.get_at(
                    (min(max_x, x * G.CELL_SIZE),
                     min(max_y, y * G.CELL_SIZE))
                ).hsva
                tile = Tile(Point(x, y), c)
                    tile.blocks_move = True
                    tile.color = (80, 80, 255)
                    tile.color = (64, 64, 255)
                self.rows[y][x] = tile
                        self.a_star.draw(screen)
        """

    def zoom_in(self, position):
        if self._scale < 16:
            self.set_scale(self._scale * 2)
            self._scroll = position - (self.get_size() / 2)
           
    def zoom_out(self, position):
        if self._scale > 1:
            self.set_scale(self._scale / 2)
            self._scroll = position - (self.get_size() / 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.set_scroll_direction(None)
            if event.pos[1] < 10:
                self.set_scroll_direction(Painter.NORTH)
            elif event.pos[1] > self.get_size().y - 10:
                self.set_scroll_direction(Painter.SOUTH)
            if event.pos[0] < 10:
                self.set_scroll_direction(Painter.EAST)
            elif event.pos[0] > self.get_size().x - 10:
                self.set_scroll_direction(Painter.WEST)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                relative_position = Point(*event.pos) + self._scroll
                for i in xrange(5):
                    self.add_human(relative_position)
            elif event.button == 3:
                relative_position = Point(*event.pos) + self._scroll
                self.ping(relative_position)
            elif event.button == 4:
                self.zoom_in(event.pos)
            elif event.button == 5:
                self.zoom_out(event.pos)


#    def screen_to_grid(self, position):
#        grid_x = position[0] / G.CELL_SIZE
#        grid_y = position[1] / G.CELL_SIZE
#        return (grid_x, grid_y)
