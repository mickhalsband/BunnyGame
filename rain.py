import pygame
from pygame.locals import *
import pymunk
import utils
import random

#TODO : add expiration date on rain
#TODO2: Maybe unite drops...


class Raindrop:
    MASS = 0.06
    RADIUS = 5
    COLOR = Color(0, 0, 255)
    COLLISION_TYPE = 3142
    FRICTION = 0.3
    uid = 0

    def __init__(self, space, x, y):
        inertia = pymunk.moment_for_circle(Raindrop.MASS, 0, Raindrop.RADIUS)
        self.body = pymunk.Body(Raindrop.MASS, inertia)
        self.body.position = x, y
        shape = pymunk.Circle(self.body, Raindrop.RADIUS)
        shape.collision_type = self.COLLISION_TYPE
        shape.friction = self.FRICTION
        space.add(self.body, shape)
        self.is_grounded = False
        self.uid = Raindrop.uid
        Raindrop.uid += 1

    def draw(self, screen):
        p = int(self.body.position.x), 600-int(self.body.position.y)
        pygame.draw.circle(screen, Raindrop.COLOR, p, int(Raindrop.RADIUS), Raindrop.RADIUS)

    def update(self, screen):
        # TODO: check for drop freshness timeout
        self.draw(screen)


class Cloud(pygame.sprite.Sprite):
    TICKS_TILL_NEXT_DROP = 5
    RAIN_CREATION_THRESHOLD = 550
    raindrop_ticks = 0  # timeout counter till next raindrop
    raindrops = []

    START_HEIGHT = 10

    def __init__(self, run_path, screen, space):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = utils.load_image('cloud.png', run_path, -1)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.topleft = 300, self.START_HEIGHT
        self.space = space
        self.topmost_drop = None

    def handle_rain(self, topmost_drop):
        self.raindrop_ticks -= 1
        if self.raindrop_ticks <= 0:
            self.drop_next_drop()

        raindrops_pending_delete = []
        for raindrop in self.raindrops:
            if (raindrop.body.position.y < self.RAIN_CREATION_THRESHOLD):
                raindrop.is_grounded = True

            if (raindrop.is_grounded is False):
                continue

            if (raindrop.body.position.y < 0):
                raindrops_pending_delete.append(raindrop)

            if (topmost_drop is None):
                topmost_drop = raindrop

            # again y is reversed for some weird reason
            if (topmost_drop.body.position.y < raindrop.body.position.y):
                topmost_drop = raindrop
                print ('top most drop y = %0.0f' % topmost_drop.body.position.y)

            raindrop.update(self.screen)

        self.handle_raindrop_delete(raindrops_pending_delete)

        return topmost_drop

    def handle_raindrop_delete(self, raindrops_pending_delete):
        if (len(raindrops_pending_delete) == 0):
            return

        print "length is %d" % len(raindrops_pending_delete)
        for raindrop in raindrops_pending_delete:
            print "removing raindrop %s" % raindrop
            self.raindrops.remove(raindrop)
            self.space.remove(raindrop.body)


    def drop_next_drop(self):
        self.raindrop_ticks = Cloud.TICKS_TILL_NEXT_DROP
        x = random.randint(self.rect.left, self.rect.right)  # randomize x
        raindrop = Raindrop(self.space, x, utils.flipy(self.rect.bottom))
        self.raindrops.append(raindrop)

    def update(self):
        self.topmost_drop = self.handle_rain(self.topmost_drop)
