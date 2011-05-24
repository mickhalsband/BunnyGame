import pygame
from pygame.locals import *
import pymunk
import utils
import random

#TODO : add expiration date on rain
#TODO2: Maybe unite drops...
class Raindrop:
	MASS = 0.1
	RADIUS = 1
	COLOR = Color(0,0,255)
	def __init__(self, space, x, y):
		inertia = pymunk.moment_for_circle(Raindrop.MASS, 0, Raindrop.RADIUS) 
		self.body = pymunk.Body(Raindrop.MASS, inertia)
		self.body.position = x, y 
		shape = pymunk.Circle(self.body, Raindrop.RADIUS)
		shape.friction = 0.5
		space.add(self.body, shape)

	def draw(self, screen):
		p = int(self.body.position.x), 600-int(self.body.position.y)
		pygame.draw.circle(screen, Raindrop.COLOR , p, int(Raindrop.RADIUS), Raindrop.RADIUS)	

	def update(self, screen):
		# TODO: check for drop freshness timeout
		self.draw(screen)

class Cloud(pygame.sprite.Sprite):
	TICKS_TILL_NEXT_DROP = 5
	raindrop_ticks = 0 # timeout counter till next raindrop
	raindrops = []

	START_HEIGHT = 10
	def __init__(self, run_path, screen, space):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image = utils.load_image('cloud.png', run_path, -1)
		self.rect = self.image.get_rect()
		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()
		self.rect.topleft = 300, self.START_HEIGHT
		self.space = space

	def handle_rain(self): 
		self.raindrop_ticks -= 1
		if self.raindrop_ticks <= 0:
			self.raindrop_ticks = Cloud.TICKS_TILL_NEXT_DROP
			x = random.randint(self.rect.left,self.rect.right) #randomize x
			raindrop = Raindrop(self.space, x, utils.flipy(self.rect.bottom))
			self.raindrops.append(raindrop)

		for raindrop in self.raindrops:
			raindrop.update(self.screen)

	def update(self):
		self.handle_rain()

