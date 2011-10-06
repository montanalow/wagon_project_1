import pygame

RANDOMIZE_EVENT = pygame.USEREVENT + 1
MOVE_EVENT = RANDOMIZE_EVENT + 1
UPDATE_FPS_PAINTER_EVENT = MOVE_EVENT + 1

#class Event(pygame.event.Event):
#class UpdatePainterEvent(Event):
#    def __init__(self, painter):
#        pygame.event.Event.__init__(UPDATE_PAINTER, {painter: painter})


