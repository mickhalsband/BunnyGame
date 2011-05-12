#/usr/bin/env python

"""
The rabbit class
"""

import os, pygame, math
from pygame.locals import *
import utils
import pymunk

FLOOR_Y = 300
JUMP_SPEED = 10
WALK_SPEED = 1.5

class Rabbit(pygame.sprite.Sprite):
	"""Moving rabbit."""

	MASS = 50
	HEIGHT = 48
	WIDTH = 33
	def __init__(self, run_path, space):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = utils.load_image('rabbit.png', run_path, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.width = 0
		self.rect.height = 0
		self.rect.topleft = 5, FLOOR_Y
		self.step = 1
		self.direction = utils.Direction.right
		self.jumping = False
		self.walking = False

		inertia = pymunk.moment_for_box(self.MASS, self.WIDTH, self.HEIGHT)
		self.body = pymunk.Body(self.MASS, inertia)
		self.body.position = 5, FLOOR_Y
		vertices = [(0,0), (self.WIDTH,0), (self.WIDTH,self.HEIGHT), (0,self.HEIGHT)]
		shape = pymunk.Poly(self.body, vertices, offset=(0, 0))
		shape.friction = 0.55
		space.add(self.body, shape)

        def _draw_wireframe(self):
		# the b-box debug wireframe
		rect = Rect(self.body.position.x, self.body.position.y+self.HEIGHT, self.WIDTH, self.HEIGHT)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.bottomleft, rect.topleft)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.topleft, rect.topright)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.topright, rect.bottomright)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.bottomright, rect.bottomleft)
                
	def update(self):
		if (self.walking):
			self.body.apply_impulse((750*self.step,0), (0,0))
		self.rect.centerx = self.body.position.x
		self.rect.centery = self.body.position.y+self.HEIGHT
		self._draw_wireframe()

	def start_walk(self, direction):
		if (direction != self.direction):
			#flip image and step
			self.direction = direction
			self.image = pygame.transform.flip(self.image, 1, 0)
			self.step = self.step * -1;
			
		self.walking = True

	# called when keypress ends
	def stop_walk(self, direction):
		self.walking = False
		
	def start_jump(self):
		self.body.apply_impulse((0,-30000), (0,0))
