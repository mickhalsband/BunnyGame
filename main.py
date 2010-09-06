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
import rain


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600


class Game:

	ticks_to_next_raindrop = 0
	raindrops = []

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
		self.cloud_sprite = rain.Cloud(run_path)
		self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite, self.cloud_sprite))

		# PHYSICS STUFF
		pymunk.init_pymunk()
		self.space = pymunk.Space()
		self.space.gravity = (0.0, -900.0)

		# ground line
		self.line_point1 = Vec2d(0, flipy(350))
		line_point2 = Vec2d(800, flipy(350))
		print self.line_point1, line_point2
		body = pymunk.Body(pymunk.inf, pymunk.inf)
		self.line = pymunk.Segment(body, self.line_point1, line_point2, 5.0)
		self.line.friction = 0.99
		self.space.add_static(self.line)

	def handle_rain(self):  
		self.ticks_to_next_raindrop -= 1
		if self.ticks_to_next_raindrop <= 0:
			self.ticks_to_next_raindrop = 5
			x = self.rabbit_sprite.rect.center[0]; #x is bunny center
			x = random.randint(x-25,x+25) #randomize x
			raindrop = rain.Raindrop(self.space, x)
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

			# line
			body = self.line.body	
			pv1 = body.position + self.line.a.rotated(body.angle)
			pv2 = body.position + self.line.b.rotated(body.angle)
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
