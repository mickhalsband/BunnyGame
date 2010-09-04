#!/usr/bin/env python

"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""

#Import Modules
import os
import sys
# Added for linux server
# Adds server folders to PYTHONPATH 
# ========================================
basedir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.append(basedir)
# end of linux part
# ========================================

import pygame
import rabbit
import utils
import pymunk
import math
import random
from pygame.locals import *
from pymunk import Vec2d


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600


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
		space.add(self.body, shape)

	def draw(self, screen):
		p = int(self.body.position.x), 600-int(self.body.position.y)
		pygame.draw.circle(screen, self.COLOR , p, int(self.RADIUS), self.RADIUS)	

class Game:

	ticks_to_next_raindrop = 0
	raindrops = []
	static_lines = []

	def init_game(self, run_path):
		#Initialize Everything
		pygame.init()
		self.screen = pygame.display.set_mode((800,600))
		pygame.display.set_caption('Rainy Bunny by Mick v0.1')
		pygame.mouse.set_visible(0)

		#Create The Backgound
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

		#Put Text On The Background, Centered
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("Rainy Bunny", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.background.get_width()/2)
			self.background.blit(text, textpos)

		#Display The Background
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

		#Prepare Game Objects
		self.clock = pygame.time.Clock()
		self.rabbit_sprite = rabbit.Rabbit(run_path)
		self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite))

		# PHYSICS STUFF
		self.space = pymunk.Space()
		self.space.gravity = (0.0, -900.0)

#		line_point1 = Vec2d(30 , flipy(350))        
#		line_point2 = Vec2d(600, flipy(350))
#		body = pymunk.Body(pymunk.inf, pymunk.inf)
#		line= pymunk.Segment(body, line_point1, line_point2, 0.0)
#		line.friction = 0.99
#		self.space.add_static(line)

#		body = line.body
#		pv1 = body.position + line.a.rotated(body.angle)
#		pv2 = body.position + line.b.rotated(body.angle)
#		self.p1 = pv1.x, flipy(pv1.y)
#		self.p2 = pv2.x, flipy(pv2.y)
#		pygame.draw.lines(self.screen, 0, False, [self.p1,self.p2])

		self.line_point1 = None

		if self.line_point1 is None:
			self.line_point1 = Vec2d(30, flipy(350))
		if self.line_point1 is not None:
			line_point2 = Vec2d(600, flipy(350))
			print self.line_point1, line_point2
			body = pymunk.Body(pymunk.inf, pymunk.inf)
			shape= pymunk.Segment(body, self.line_point1, line_point2, 0.0)
			shape.friction = 0.99
			self.space.add_static(shape)
			self.static_lines.append(shape)
			self.line_point1 = None

	def handle_rain(self):  
		self.ticks_to_next_raindrop -= 1
		if self.ticks_to_next_raindrop <= 0:
			self.ticks_to_next_raindrop = 5
			x = self.rabbit_sprite.rect.center[0]; #x is bunny center
			x = random.randint(x-25,x+25) #randomize x
			raindrop = Raindrop(self.space, x)
			self.raindrops.append(raindrop)

		for raindrop in self.raindrops:
			raindrop.draw(self.screen)

	# return False to signal quit
	def handle_input_events(self):
		#Handle Input Events
		for event in pygame.event.get():
			if (event.type == QUIT) \
			or (	event.type == KEYDOWN and event.key == K_ESCAPE):
				return False
			# key_to_dir(event.key) != 0 for valid keys
			elif event.type == KEYDOWN and utils.key_to_dir(event.key) != 0:
				self.rabbit_sprite.start_walk(utils.key_to_dir(event.key));
			elif event.type == KEYUP and utils.key_to_dir(event.key) != 0:
				self.rabbit_sprite.stop_walk(utils.key_to_dir(event.key));
			elif event.type == KEYDOWN and event.key == K_SPACE:
				self.rabbit_sprite.start_jump();
		return True


	#Main Loop
	def do_main_loop(self):
		ticks_to_next_raindrop = 10

		# will break out on invalid (quit) events
		while True:
			self.clock.tick(60)

			if (not self.handle_input_events()):
				break

			self.allsprites.update()

			#Draw Everything
			self.screen.blit(self.background, (0, 0))
			self.allsprites.draw(self.screen)
     
			self.handle_rain()   

			for line in self.static_lines:
				body = line.body
		
				pv1 = body.position + line.a.rotated(body.angle)
				pv2 = body.position + line.b.rotated(body.angle)
				p1 = pv1.x, flipy(pv1.y)
				p2 = pv2.x, flipy(pv2.y)
				pygame.draw.lines(self.screen, Color(100,100,100), False, [p1,p2])

			### Update physics
			# for some reason 1.0/60.0 crashes like hell :(
			dt = 1.0/55.0
			for x in range(1):
				self.space.step(dt)

			pygame.display.flip()


	def main(self):
		"""this function is called when the program starts.
		   it initializes everything it needs, then runs in
		   a loop until the function returns."""

		# pass down base path os that resources could be loaded when relative path is envoked
		run_path = os.path.dirname(os.path.abspath(sys.argv[0]))
		
		self.init_game(run_path)

		self.do_main_loop()

	#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
	game = Game()
	game.main()
