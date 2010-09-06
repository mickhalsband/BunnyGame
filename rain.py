import pygame
from pygame.locals import *
import pymunk
import utils

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


class Cloud(pygame.sprite.Sprite):
	START_HEIGHT = 10
	def __init__(self, run_path):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image, self.rect = utils.load_image('cloud.png', run_path, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.width = 10
		self.rect.height = 10
		self.rect.topleft = 10, self.START_HEIGHT	
