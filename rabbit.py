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

class AnimatedSprite(pygame.sprite.Sprite):
	"""Base class for an animated sprite"""
	def __init__(self, w, h, sprite_filename):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self._images = utils.load_sliced_sprites(w, h, sprite_filename)
		self._start = pygame.time.get_ticks()
		self._delay = 1000 / self.FPS
		self._last_update = 0
		self._frame = 0
		self.update()

	def update(self):
		t = pygame.time.get_ticks()
		if t - self._last_update > self._delay:
			# do update
			self._frame += 1
			if self._frame >= len(self._images): 
				self._frame = 0
			self.image = self._images[self._frame]
			self._last_update = t
			if (self.direction == utils.Direction.left):
				self.image = pygame.transform.flip(self.image, 1, 0)
			

class Rabbit(AnimatedSprite):
	"""Moving rabbit."""

	MASS = 50
	HEIGHT = 48
	WIDTH = 33
	FPS = 10
	def __init__(self, run_path, space):
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect = Rect(5, FLOOR_Y, self.WIDTH, self.HEIGHT)
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

		AnimatedSprite.__init__(self, self.WIDTH, self.HEIGHT, 'rabbit_sprite.png') #call Sprite intializer
		
	def _draw_wireframe(self):
		# the b-box debug wireframe
		rect = Rect(self.body.position.x, self.body.position.y+self.HEIGHT, self.WIDTH, self.HEIGHT)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.bottomleft, rect.topleft)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.topleft, rect.topright)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.topright, rect.bottomright)
		pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), rect.bottomright, rect.bottomleft)

	def update(self):
		AnimatedSprite.update(self)
		if (self.walking):
			self.body.apply_impulse((750*self.step,0), (0,0))

		self.rect.centerx = self.body.position.x
		self.rect.centery = self.body.position.y+self.HEIGHT
		self._draw_wireframe()

	def start_walk(self, direction):
		if (direction != self.direction):
			#flip image and step
			self.step = self.step * -1;
			self.direction = direction
		self.walking = True

	# called when keypress ends
	def stop_walk(self, direction):
		self.walking = False
		
	def start_jump(self):
		self.body.apply_impulse((0,-30000), (0,0))
