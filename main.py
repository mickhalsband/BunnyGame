'''
Widget animation
================

This is showing an example of a animation creation, and how you can apply yo a
widget.
'''

import kivy

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import OptionProperty, NumericProperty, StringProperty
from kivy.uix.image import Image

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout

kivy.require('1.0.7')

import utils


class Sprite(Image):
    step_size = 20
    atlas = StringProperty('')
    frame = NumericProperty(1)  # maybe specify min/max
    resource = StringProperty()
    duration = 0.5
    frame_count = 5

    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.atlas = self.__class__.__name__.lower()

    def _schedule_frame(self):
        Clock.schedule_once(self._advance_frame, self.duration / self.frame_count)

    def _advance_frame(self, *args):
        self.frame += 1
        if self.frame < self.frame_count:
            self._schedule_frame()

    def animate(self, resource):
        self.resource = resource
        Clock.unschedule(self._advance_frame)
        self.frame = 1
        self._schedule_frame()


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
        self.animate('right')
        Animation.cancel_all(self)
        anim = Animation(x=self.x + 15, y=self.y + 25, d=self.duration/2, t='in_sine') + \
               Animation(x=self.x + 30, y=self.y, d=self.duration/2, t='out_sine')
        anim.start(self)


class BunnyGame(RelativeLayout):
    def __init__(self, **kwargs):
        super(BunnyGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        curr_keycode = keycode[1]
        print 'keycode is ' + curr_keycode

        if curr_keycode in [utils.Direction.left, utils.Direction.right]:
            self.bunny.walk(curr_keycode)

        elif curr_keycode in ['up', 'spacebar']:
            self.bunny.jump()

        elif curr_keycode == 'escape' or 'q':
            exit()

        else:
            pass

        return True


class BunnyApp(App):
    def build(self):
        return BunnyGame()


if __name__ == '__main__':
    BunnyApp().run()
