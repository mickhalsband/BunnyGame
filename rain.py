import pygame
from pygame.locals import *
import pymunk

class Raindrop:
	MASS = 1
	RADIUS = 2
	START_HEIGHT = 550
	COLOR = Color(0,0,255)
	def __init__(self, space, x):
		inertia = pymunk.moment_for_circle(self.MASS, 0, self.RADIUS) 
		self.body = pymunk.Body(self.MASS, inertia)
		self.body.position = x, self.START_HEIGHT 
		shape = pymunk.Circle(self.body, self.RADIUS)
		shape.friction = 0.5
		space.add(self.body, shape)

	def draw(self, screen):
		p = int(self.body.position.x), 600-int(self.body.position.y)
		pygame.draw.circle(screen, self.COLOR , p, int(self.RADIUS), self.RADIUS)	

