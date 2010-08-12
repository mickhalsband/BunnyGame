
import os, pygame
from pygame.locals import *

#functions to create our resources
def load_image(name, colorkey=None):
	fullname = os.path.join('resources', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('Cannot load image:', fullname)
		raise SystemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join('resources', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error as message:
		print('Cannot load sound:', fullname)
		raise SystemExit(message)
	return sound

def key_to_dir(key):
	if (key == K_RIGHT):
		return Direction.right
	elif (key == K_LEFT):
		return Direction.left
	else:
		return Direction.none
		
class Direction:
	none=0
	left=1
	right=2
