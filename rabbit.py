#/usr/bin/env python

"""
The rabbit class
"""

import os, pygame, math
from pygame.locals import *
import utils

FLOOR_Y = 300
JUMP_SPEED = 10
WALK_SPEED = 1.5

class Rabbit(pygame.sprite.Sprite):
	"""moves a rabbit critter across the screen. it can spin the
	   rabbit when it is punched."""
	def __init__(self, run_path):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = utils.load_image('rabbit.png', run_path, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.width = 10
		self.rect.height = 10
		self.rect.topleft = 10, FLOOR_Y
		self.step = 3
		self.direction = utils.Direction.right
		self.v_x = 0 
		self.v_y = 0
		self.jumping = 0

	def init_y(self):
		self.rect.bottom = FLOOR_Y
		self.v_y = 0
		self.jumping = 0		

	def update(self):
		"walk or jump depending on state"
		if (self.v_x == 0 and self.v_y == 0 and self.rect.bottom > FLOOR_Y):
			self.init_y()
			return

		dt = 1
		dx = 0
		dy = 0

		# needs optimizations badly!
		if (1):#(self.v_y != 0):
			# dx = v0*dt + accel*dt*0.5
			a_y = 1
			self.v_y = self.v_y + a_y*math.pow(dt,2)
			dy = self.v_y*dt

		if (1):#(self.v_x != 0):
			# dx = v0*dt + accel*dt*0.5
			a_x = 0
			self.v_x = self.v_x + a_x*math.pow(dt,2)
			dx = self.v_x*dt
				
		self.rect = self.rect.move((dx, dy))

		if (self.rect.bottom > FLOOR_Y):
			self.init_y()
	
	def start_walk(self, direction):
		if (direction != self.direction):
			#flip image and step
			self.direction = direction
			self.image = pygame.transform.flip(self.image, 1, 0)
			self.step = self.step * -1;
			
		self.v_x = self.step * WALK_SPEED

	# called when keypress ends
	def stop_walk(self, direction):
		self.v_x = 0
		
	def start_jump(self):
		if (self.jumping == 1):
			# don't double jump
			return
		self.jumping = 1	

		# kick rabbit with initial speed (negative val = upwards)
		self.v_y = -1 * JUMP_SPEED
