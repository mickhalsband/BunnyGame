import pygame
from pygame.locals import Color
import pymunk

__author__ = 'mick'

# TODO : add expiration date on rain
# TODO2: Maybe unite drops...


class Raindrop:
    MASS = 0.1
    RADIUS = 1
    COLOR = Color(0, 0, 255)

    def __init__(self, space, x, y):
        inertia = pymunk.moment_for_circle(Raindrop.MASS, 0, Raindrop.RADIUS)
        self.body = pymunk.Body(Raindrop.MASS, inertia)
        self.body.position = x, y
        shape = pymunk.Circle(self.body, Raindrop.RADIUS)
        shape.friction = 0.5
        space.add(self.body, shape)

    def draw(self, screen):
        p = int(self.body.position.x), 600-int(self.body.position.y)
        pygame.draw.circle(screen, Raindrop.COLOR, p, int(Raindrop.RADIUS), Raindrop.RADIUS)

    def update(self, screen):
        # TODO: check for drop freshness timeout
        self.draw(screen)