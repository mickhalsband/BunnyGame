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

floor = 300
music_enabled = False


class Game:
    GROUND_COLLISION_TYPE = 3453

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
        self.space.add_collision_handler(rain.Raindrop.COLLISION_TYPE, self.GROUND_COLLISION_TYPE, self.begin_rain_collision_func)

        #Prepare Game Objects
        self.clock = pygame.time.Clock()
        self.rabbit_sprite = rabbit.Rabbit(run_path, self.space, pygame.display.get_surface())
        self.cloud_sprite = rain.Cloud(run_path, self.screen, self.space)
        self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite, self.cloud_sprite))

        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.init_ground()

    def begin_rain_collision_func(space, arbiter, *args, **kwargs):
        #if (arbiter is rain.Raindrop and space is ):
        drop = arbiter.shapes[0]
        # ?!?
#    if drop is rain.Raindrop:
        with drop as rain.Raindrop:
            drop.is_grounded = True
            print arbiter.uid
        return True

    # ground line
    def init_ground(self):
        '''this initializes the ground'''
        correct_floor = utils.flipy(floor)
        self.line1 = pymunk.Segment(self.body, Vec2d(0, correct_floor), Vec2d(400, correct_floor-100), 5.0)
        self.line1.collision_type = self.GROUND_COLLISION_TYPE
        self.line1.friction = 0.99
        # self.space.add_static(self.line)
        self.space.add(self.line1)

        self.line2 = pymunk.Segment(self.body, Vec2d(400, correct_floor-100), Vec2d(800, correct_floor), 5.0)
        self.line2.collision_type = self.GROUND_COLLISION_TYPE
        self.line2.friction = 0.99
        # self.space.add_static(self.line)
        self.space.add(self.line2)

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

            #if (self.rabbit_sprite.body.position.y > self.cloud_sprite.topmost_drop.body.position.y):
            #    self.rabbit_sprite.body.mass = rabbit.Rabbit.MASS * 1.5

            self.print_ground(self.line1)
            self.print_ground(self.line2)

            ### Update physics
            # for some reason 1.0/60.0 crashes like hell :(
            dt = 1.0/60.0
            for x in range(1):
                self.space.step(dt)

            pygame.display.flip()

    def print_ground(self, line):
        pv1 = self.body.position + line.a.rotated(self.body.angle)
        pv2 = self.body.position + line.b.rotated(self.body.angle)
        p1 = pv1.x, utils.flipy(pv1.y)
        p2 = pv2.x, utils.flipy(pv2.y)

        pygame.draw.lines(self.screen, Color(100, 100, 100), False, [p1, p2])

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
