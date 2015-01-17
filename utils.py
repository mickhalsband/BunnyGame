import os
import pygame
from pygame.locals import *

RESOURCE_DIR = 'resources'


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


#functions to create our resources
def load_image(name, run_path, colorkey=None):
    basepath = os.path.join(run_path, RESOURCE_DIR)
    fullname = os.path.join(basepath, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(name, run_path):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    basepath = os.path.join(run_path, RESOURCE_DIR)
    fullname = os.path.join(basepath, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound


class Direction:
    none = ''
    left = 'left'
    right = 'right'

    key2dir = {left: -1, right: 1}