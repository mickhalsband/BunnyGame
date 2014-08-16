from kivy.animation import Animation
from kivy.properties import OptionProperty
from sprite import Sprite
import utils

__author__ = 'mick'


class Bunny(Sprite):
    direction = OptionProperty('right', options=('right', 'left'))

    def __init__(self, **kwargs):
        super(Bunny, self).__init__(**kwargs)
        self.resource = self.direction

    def walk(self, keycode):
        if keycode != self.direction:
            # flip image and step
            self.direction = keycode
        self.animate(self.direction)
        offset = utils.Direction.key2dir[self.direction] * self.step_size
        Animation.cancel_all(self)
        Animation(x=(self.x + offset), y=self.y, d=self.duration).start(self)

    def jump(self):
        self.animate(self.direction)
        Animation.cancel_all(self)
        dir_sign = utils.Direction.key2dir[self.direction]
        anim = Animation(x=self.x + (15 * dir_sign), y=self.y + 25, d=self.duration / 2, t='in_sine') + \
               Animation(x=self.x + (30 * dir_sign), y=self.y, d=self.duration / 2, t='out_sine')
        anim.start(self)