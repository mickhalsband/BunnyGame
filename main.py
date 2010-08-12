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

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def main():
	"""this function is called when the program starts.
	   it initializes everything it needs, then runs in
	   a loop until the function returns."""
#Initialize Everything
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	pygame.display.set_caption('rabbit_sprite Fever')
	pygame.mouse.set_visible(0)

#Create The Backgound
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

#Put Text On The Background, Centered
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("My Game", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=background.get_width()/2)
		background.blit(text, textpos)

#Display The Background
	screen.blit(background, (0, 0))
	pygame.display.flip()

#Prepare Game Objects
	clock = pygame.time.Clock()
	whiff_sound = utils.load_sound('whiff.wav')
	punch_sound = utils.load_sound('punch.wav')
	rabbit_sprite = rabbit.Rabbit()
#	bird = Bird()
	allsprites = pygame.sprite.RenderPlain((rabbit_sprite))

#Main Loop
	while 1:
		clock.tick(60)

	#Handle Input Events
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			# key_to_dir(event.key) != 0 for valid keys
			elif event.type == KEYDOWN and utils.key_to_dir(event.key) != 0:
				rabbit_sprite.start_move(utils.key_to_dir(event.key));
			elif event.type == KEYUP and utils.key_to_dir(event.key) != 0:
				rabbit_sprite.stop_move(utils.key_to_dir(event.key));
			elif event.type == KEYDOWN and event.key == K_SPACE:
				rabbit_sprite.start_jump();
		allsprites.update()

	#Draw Everything
		screen.blit(background, (0, 0))
		allsprites.draw(screen)
		pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
