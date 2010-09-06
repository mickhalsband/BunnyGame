import pygame
from pygame.locals import *
import pymunk
import utils
import random

class Raindrop:
	MASS = 1
	RADIUS = 2
	COLOR = Color(0,0,255)
	def __init__(self, space, x, y):
		inertia = pymunk.moment_for_circle(self.MASS, 0, self.RADIUS) 
		self.body = pymunk.Body(self.MASS, inertia)
		self.body.position = x, y 
		shape = pymunk.Circle(self.body, self.RADIUS)
		shape.friction = 0.5
		space.add(self.body, shape)

	def draw(self, screen):
		p = int(self.body.position.x), 600-int(self.body.position.y)
		pygame.draw.circle(screen, self.COLOR , p, int(self.RADIUS), self.RADIUS)	


class Cloud(pygame.sprite.Sprite):
	raindrop_ticks = 0
	raindrops = []

	START_HEIGHT = 10
	def __init__(self, run_path, screen, space):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = utils.load_image('cloud.png', run_path, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 300, self.START_HEIGHT
		self.screen = screen
		self.space = space

	def handle_rain(self): 
		self.raindrop_ticks -= 1
		if self.raindrop_ticks <= 0:
			self.raindrop_ticks = 5
			x = random.randint(self.rect.left,self.rect.right) #randomize x
			raindrop = Raindrop(self.space, x, utils.flipy(self.rect.bottom))
			self.raindrops.append(raindrop)

		for raindrop in self.raindrops:
			raindrop.draw(self.screen)

	def update(self):
		self.handle_rain()

