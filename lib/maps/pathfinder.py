import heapq

import pygame

import lib.game as G
from lib.point import Point

class AStarNode(object):
    __slots__ = ('x', 'y', 'coord', 'f', 'g', 'h', 'parent', 'blocks_move')
    def __init__(self, tile):
        p = tile.position()
        self.x = p.x
        self.y = p.y
        self.coord = (self.x, self.y)
        self.blocks_move = tile.blocks_move
        self.reset_scores()

    def __unicode__(self):
        return u'<NODE %d %d>' % (self.x, self.y)
    __repr__ = __unicode__

    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def reset_scores(self):
        self.f = self.g = self.h = 0
        self.parent = None

class AStarPathFinder(object):
    def __init__(self, game_map):
        self._searched_nodes = set()

        # build a copy of our map as nodes
        self._nodes = []
        for row in game_map.rows:
            r = []
            for cell in row:
                r.append(AStarNode(cell))
            self._nodes.append(r)
        self._reset()

    def _reset(self):
        self._most_recent_path = []
        self._open = [] # heap queue storing nodes sorted by 'f' value
        self._closed_set = set() # to contain node coordinates only
        for node in self._searched_nodes:
            node.reset_scores()
        self._searched_nodes = set()

    def _heuristic(self, node_a, node_b):
        p_a = Point(node_a.x, node_a.y)
        return p_a.diagnol_distance(node_b)

    def _adjacency_list(self, pos):
        """find up to 8 tiles adjacent to the cell position passed in
        """
        adj = []
        #print "finding 8 adjacent for:", pos
        for row_num in range(pos.y - 1, pos.y + 2):
            for col_num in range(pos.x - 1, pos.x + 2):
                if row_num >= 0 and row_num < len(self._nodes) \
                   and col_num >= 0 and col_num < len(self._nodes[0]):
                    if row_num == pos.y and col_num == pos.x:
                        continue # don't count ourselves as adjacent
                    #print col_num, row_num
                    adj.append(self._nodes[row_num][col_num])
        return adj

    def _inspect_adjacent(self, node):
        pos = Point(node.x, node.y)
        for neighbor in self._adjacency_list(pos):
            new_g = node.g + pos.diagnol_distance(neighbor)

            if neighbor.blocks_move:
                continue

            self._searched_nodes.add(neighbor)
            if new_g < neighbor.g:
                # this path is better
                if neighbor in self._open:
                    # new path is better, take it out of open
                    self._open.remove(neighbor)
                    #self._open_set.discard(neighbor.coord)
                if neighbor.coord in self._closed_set:
                    self._closed_set.add(neighbor.coord)

            if neighbor not in self._open and \
               neighbor.coord not in self._closed_set:
                neighbor.g = new_g
                neighbor.h = self._heuristic(neighbor, self.target_node)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = node
                heapq.heappush(self._open, neighbor)
                #self._open_set.add(neighbor.coord)

    def find_path(self, start_pos, end_pos):
        self._reset()

        start = self._nodes[start_pos.y][start_pos.x]
        self.target_node = self._nodes[end_pos.y][end_pos.x]

        start.g = 0
        start.h = self._heuristic(start, self.target_node)
        start.f = start.h
        heapq.heappush(self._open, start)

        for i in xrange(2000):
            node = heapq.heappop(self._open)
            #self._searched_nodes.add(node)
            if node is self.target_node:
                print "found path", len(self._searched_nodes), "nodes checked"
                return self._reconstruct_path(node)

            self._closed_set.add(node.coord)
            self._inspect_adjacent(node)

        print "No path found!"
        return None

    def _reconstruct_path(self, current_node, path=None):
        path = []
        while current_node.parent is not None:
            path.append(Point(current_node.x, current_node.y))
            current_node = current_node.parent
        path.append(Point(current_node.x, current_node.y))
        path.reverse() # in-place
        self._most_recent_path = path
        return path

    def draw(self, screen):
        """ for debugging, draw useful hints on the screen
        """
        if not self._most_recent_path:
            return
        max_h = max([node.h for node in self._searched_nodes])
        max_f = max([node.f for node in self._searched_nodes])

        #print "max_h", max_h
        #print "max_f", max_f
        for node in self._searched_nodes:
            f_scale = node.f / max_f
            h_scale = node.h / max_h
            color = (255 * h_scale, 255 * h_scale, 255 * f_scale)
            r = pygame.rect.Rect(G.CELL_SIZE * node.x, G.CELL_SIZE * node.y,
                                 G.CELL_SIZE, G.CELL_SIZE)
            pygame.draw.rect(screen, color, r, 1)





