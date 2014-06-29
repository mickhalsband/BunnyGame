'''
Widget animation
================

This is showing an example of a animation creation, and how you can apply yo a
widget.
'''

import kivy

from kivy.app import App
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
    direction = OptionProperty('right', options=('right', 'left'))
    frame = NumericProperty(1)  # maybe specify min/max
    duration = 0.5

    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.atlas = self.__class__.__name__.lower()

    def animate(self, keycode):
        if keycode != self.direction:
            # flip image and step
            self.direction = keycode

        offset = utils.Direction.key2dir[self.direction] * self.step_size
        Animation.cancel_all(self)
        self.frame = 1
        Animation(x=(self.x + offset), y=self.y, frame=5, d=self.duration).start(self)
#
#     def jump(self):
#         anim = Animation(x=self.x + 15, y=self.y + 25, d=self.duration, t='in_sine') + \
#                Animation(x=self.x + 30, y=self.y, d=self.duration, t='out_sine')
#         anim.start(self)
#         self.sprite.play(duration=self.duration)


class Bunny(Sprite):
    def __init__(self, **kwargs):
        super(Bunny, self).__init__(**kwargs)

    def walk(self, keycode):
        self.animate(keycode)


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
