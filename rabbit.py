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
	'''Base class for an animated sprite'''
	def __init__(self, sprite_filename):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self._images = utils.load_sliced_sprites(self.rect.width, self.rect.height, sprite_filename)
		self._start = pygame.time.get_ticks()
		self._last_update = 0
		self._frame_index = 0
		self._distance = 0
		self.image = self._images[0]
		self.update()
		
	def _draw_wireframe(self):
		'''Draw the bounding-box debug wireframe'''
		pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect, 1)

	def _advance_image(self):
		if self._distance > 10:
			# do update
			self._frame_index = (self._frame_index + 1) % len(self._images)
			self.image = self._images[self._frame_index]
			if (self.direction == utils.Direction.left):
				self.image = pygame.transform.flip(self.image, 1, 0)
			self._distance = 0
	
	def update(self):		
		self._advance_image()
			
		self._draw_wireframe()

class Rabbit(AnimatedSprite):
	'''
	Animated rabbit sprite
	'''

	MASS = 50
	HEIGHT = 48
	WIDTH = 33
	FPS = 10
	def __init__(self, run_path, space, screen):
		self.area = screen.get_rect()
		self.step = 1
		self.direction = utils.Direction.right
		#self.jumping = False
		self.walking = False

		inertia = pymunk.moment_for_box(self.MASS, self.WIDTH, self.HEIGHT)
		self.body = pymunk.Body(self.MASS, inertia)
		self.body.position = 100, FLOOR_Y
		vertices = [(0,0), (self.WIDTH,0), (self.WIDTH,self.HEIGHT), (0,self.HEIGHT)]
		shape = pymunk.Poly(self.body, vertices, offset=(0, 0))
		shape.friction = 0.55
		space.add(self.body, shape)

		self.rect = Rect(self.body.position.x, self.body.position.y, self.WIDTH, self.HEIGHT)
		AnimatedSprite.__init__(self, 'rabbit_sprite.png') #call Sprite intializer

	def update(self):
		if (self.walking):
			self.body.apply_impulse((750*self.step,0), (0,0))		
	
		body_centerx = self.body.position.x + self.WIDTH/2
		self._distance += int(abs(body_centerx - self.rect.centerx))
		
		self.rect.centerx = body_centerx
		self.rect.centery = self.body.position.y+1.5*self.HEIGHT # WTF?! i don't get the locations here
	
		AnimatedSprite.update(self)

	def start_walk(self, direction):
		if (direction != self.direction):
			#flip image and step
			self.step = self.step * -1;
			self.direction = direction
		self.walking = True

	# called when keypress ends
	def stop_walk(self, direction):
		self.walking = False
		
	def jump(self):
		self.body.apply_impulse((0,-30000), (0,0))
