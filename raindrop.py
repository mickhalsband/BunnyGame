import pygame
from pygame.locals import *
import pymunk


class Raindrop:
    MASS = 0.06
    RADIUS = 5
    COLOR = Color(0, 0, 255)
    COLLISION_TYPE = 3142
    FRICTION = 0.3
    uid = 0

    def __init__(self, space, x, y):
        inertia = pymunk.moment_for_circle(Raindrop.MASS, 0, Raindrop.RADIUS)
        self.body = pymunk.Body(Raindrop.MASS, inertia)
        self.body.position = x, y
        shape = pymunk.Circle(self.body, Raindrop.RADIUS)
        shape.collision_type = self.COLLISION_TYPE
        shape.friction = self.FRICTION
        space.add(self.body, shape)
        self.is_grounded = False
        self.uid = Raindrop.uid
        Raindrop.uid += 1

    def draw(self, screen):
        p = int(self.body.position.x), 600-int(self.body.position.y)
        pygame.draw.circle(screen, Raindrop.COLOR, p, int(Raindrop.RADIUS), Raindrop.RADIUS)

    def update(self, screen):
        # TODO: check for drop freshness timeout
        self.draw(screen)
