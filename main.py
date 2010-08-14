#/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *
import rabbit, utils
import pymunk


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class Game:

	def init_game(self):
		#Initialize Everything
		pygame.init()
		self.screen = pygame.display.set_mode((800,600))
		pygame.display.set_caption('rabbit_sprite Fever')
		pygame.mouse.set_visible(0)

		#Create The Backgound
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

		#Put Text On The Background, Centered
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("My Game", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.background.get_width()/2)
			self.background.blit(text, textpos)

		#Display The Background
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

		#Prepare Game Objects
		self.clock = pygame.time.Clock()
		#whiff_sound = utils.load_sound('whiff.wav')
		#punch_sound = utils.load_sound('punch.wav')
		self.rabbit_sprite = rabbit.Rabbit()
		#	bird = Bird()
		self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite))

	def do_main_loop(self):
		#Main Loop
		balls = []
		ticks_to_next_ball = 10
		while 1:
			self.clock.tick(60)

			#Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				# key_to_dir(event.key) != 0 for valid keys
				elif event.type == KEYDOWN and utils.key_to_dir(event.key) != 0:
					self.rabbit_sprite.start_walk(utils.key_to_dir(event.key));
				elif event.type == KEYUP and utils.key_to_dir(event.key) != 0:
					self.rabbit_sprite.stop_walk(utils.key_to_dir(event.key));
				elif event.type == KEYDOWN and event.key == K_SPACE:
					self.rabbit_sprite.start_jump();
			self.allsprites.update()

			#Draw Everything
			self.screen.blit(self.background, (0, 0))
			self.allsprites.draw(self.screen)

###        
			ticks_to_next_ball -= 1
			if ticks_to_next_ball <= 0:
				ticks_to_next_ball = 25
				ball_shape = self.add_ball(self.space)
				balls.append(ball_shape)

			for ball in balls:
				self.draw_ball(self.screen, ball)

			# Physics step
			self.space.step(1/50.0)

			pygame.display.flip()


	def add_ball(self, space):
		mass = 1
		radius = 14
		inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
		body = pymunk.Body(mass, inertia) # 2
		x = self.rabbit_sprite.rect.x
		body.position = x, 550 # 3
		shape = pymunk.Circle(body, radius) # 4
		self.space.add(body, shape) # 5
		return shape

	def draw_ball(self, screen, ball):
		p = int(ball.body.position.x), 600-int(ball.body.position.y)
		pygame.draw.circle(screen, Color(0,0,1), p, int(ball.radius), 2)

	def main(self):
		"""this function is called when the program starts.
		   it initializes everything it needs, then runs in
		   a loop until the function returns."""
		self.init_game()

		pymunk.init_pymunk()
		self.space = pymunk.Space()
		self.space.gravity = (0.0, -900.0)

		self.do_main_loop()

	#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
	game = Game()
	game.main()
