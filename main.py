#!/usr/bin/env python

"""
This simple example is used for the line-by-line tutorial
that comes with pygame. 
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
from pygame.locals import *
from pymunk import Vec2d
import rain


if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

floor = 350
music_enabled = False


class Game:
    def init_game(self, run_path):
        #Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Rainy Bunny v0.1')
        pygame.mouse.set_visible(0)

        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # load background music
        if music_enabled:
            pygame.mixer.music.load('resources/background_music.wav')

        # PHYSICS STUFF
        #pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        #Prepare Game Objects
        self.clock = pygame.time.Clock()
        self.rabbit_sprite = rabbit.Rabbit(run_path, self.space, pygame.display.get_surface())
        self.cloud_sprite = rain.Cloud(run_path, self.screen, self.space)
        self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite, self.cloud_sprite))

        # ground line
        self.line_point1 = Vec2d(0, utils.flipy(floor))
        line_point2 = Vec2d(800, utils.flipy(floor))
        print self.line_point1, line_point2
        body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.line = pymunk.Segment(body, self.line_point1, line_point2, 5.0)
        self.line.friction = 0.99
        # self.space.add_static(self.line)
        self.space.add(self.line)

    # return False to signal quit
    def handle_input_events(self):
        #Handle Input Events
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            # key_to_dir(event.key) != 0 for valid keys
            elif event.type == KEYDOWN and utils.key_to_dir(event.key) != utils.Direction.none:
                self.rabbit_sprite.start_walk(utils.key_to_dir(event.key))
            elif event.type == KEYUP and utils.key_to_dir(event.key) != utils.Direction.none:
                self.rabbit_sprite.stop_walk(utils.key_to_dir(event.key))
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.rabbit_sprite.jump()

        #self.cloud_sprite.rect.left = self.rabbit_sprite.image.rect.left
        self.cloud_sprite.rect.left = self.rabbit_sprite.body.position.x
        return True

    #Main Loop
    def do_main_loop(self):
        #ticks_to_next_raindrop = 10

        # will break out on invalid (quit) events
        while True:
            self.clock.tick(60)

            if (not self.handle_input_events()):
                break

            # check for music
            if (music_enabled and False == pygame.mixer.music.get_busy()):
                # yay! creepy background music!
                pygame.mixer.music.play()

            #Draw Everything
            self.screen.blit(self.background, (0, 0))
            self.allsprites.draw(self.screen)

            # update after draw:
            # some sprite (like cloud) handle their own physics and drawing
            self.allsprites.update()

            # line
            body = self.line.body
            pv1 = body.position + self.line.a.rotated(body.angle)
            pv2 = body.position + self.line.b.rotated(body.angle)
            p1 = pv1.x, utils.flipy(pv1.y)
            p2 = pv2.x, utils.flipy(pv2.y)
            pygame.draw.lines(self.screen, Color(100, 100, 100), False, [p1, p2])

            ### Update physics
            # for some reason 1.0/60.0 crashes like hell :(
            dt = 1.0/60.0
            for x in range(1):
                self.space.step(dt)

            pygame.display.flip()

    def main(self):
        '''this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns.'''

        # pass down base path os that resources could be loaded when relative path is envoked
        run_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.init_game(run_path)
        self.do_main_loop()

    #Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    game = Game()
    game.main()
