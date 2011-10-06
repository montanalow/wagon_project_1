#STDLIB
import logging
import logging.config
import os
import sys

#3RDPARTY
import pygame

# constants
#CELL_SIZE = 16
WINDOW_SIZE = (640, 480)
MAX_FPS = 60

class GameState(object):
    """The authority on what's going on in the game world
    """
    current_map = None
    clock = None
    main_surface = None
    main_painter = None
    running = False
    max_res = (640, 480)

def setup_logging():
    # ensure we have a log directory we can write to
    log_folder = os.path.join(os.path.curdir, "log")
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    logging.config.fileConfig("etc/logging.cfg")
    main_log = logging.getLogger("main")
    main_log.debug('Starting Wagon Simulator Pro 2010 Extreme Limited Edition')

def setup():
    """Turn on pygame, and setup everything we need to kick-off the main loop
    """
    setup_logging()
    main_log = logging.getLogger("main")
    main_log.debug("Setting up game")
    # imports that may have a circular dependency on game.py are imported here
    from lib.painter import Painter
    from lib.fps_painter import FPSPainter
    from lib.maps.game_map import GameMap

    # certain platforms have better drivers we want to take advantage of if
    # possible
    if 'win' in sys.platform and sys.platform != 'darwin': # windows
        os.environ['SDL_VIDEODRIVER'] = "directx"

    # turn on pygame
    main_log.debug("Initializing pygame")
    pygame.init()
    GameState.clock = pygame.time.Clock()
    print pygame.display.Info()
    driver = pygame.display.Info()
    print "Using SDL driver: %s" % driver
    GameState.max_res = (driver.current_w, driver.current_h)

    main_log.debug("Using SDL driver: %s", pygame.display.get_driver())
    main_log.debug(pygame.display.Info())
    # switch the cursor for the hell of it
    pygame.mouse.set_cursor(*pygame.cursors.diamond)

    # set a window title (also for the hell of it)
    pygame.display.set_caption("WAGONS!")
    from lib.painter import Painter
    from lib.point import Point
    Painter.font = pygame.font.SysFont("impact", 18, bold=False, italic=False)
    GameState.main_surface = pygame.display.set_mode(WINDOW_SIZE)#,(pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF))
    GameState.main_painter = Painter(None, Point(*GameState.main_surface.get_size()))


    GameState.fps_painter = FPSPainter(GameState.main_painter)
    GameState.current_map = GameMap(WINDOW_SIZE, GameState.main_painter)


def go():
    logging.getLogger("main").debug("Main loop starting")
    from lib.maps.game_map import GameMap
    from lib.event import RANDOMIZE_EVENT
    from lib.event import UPDATE_FPS_PAINTER_EVENT
    from lib.painter import Painter
    from lib.point import Point
    
    GameState.running = True
    while GameState.running:
        elapsed = GameState.clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameState.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    flags = GameState.main_surface.get_flags()
                    if flags & pygame.FULLSCREEN:
                        pygame.display.set_mode(WINDOW_SIZE, ~pygame.FULLSCREEN)
                        GameState.current_map.set_size(Point(*GameState.WINDOW_SIZE))
                    else:
                        pygame.display.set_mode(GameState.max_res, pygame.FULLSCREEN)
                        GameState.current_map.set_size(Point(*GameState.max_res))
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                   GameState.running = False
            elif event.type == pygame.MOUSEMOTION:
                GameState.current_map.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                GameState.current_map.handle_event(event)
            elif event.type == UPDATE_FPS_PAINTER_EVENT:
                GameState.fps_painter.update(elapsed)

        GameState.main_surface.fill((0,0,0))
        GameState.main_painter.paint(elapsed)
        pygame.display.flip()
    logging.getLogger("main").debug("Main loop exited")

def cleanup():
    """do any finalization and cleanup work here
    """
    logging.getLogger("main").debug("cleaning up")
    pygame.quit()
