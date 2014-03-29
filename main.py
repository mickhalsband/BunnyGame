'''
Widget animation
================

This is showing an example of a animation creation, and how you can apply yo a
widget.
'''

import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window

kivy.require('1.0.7')

import utils


class Bunny(BoxLayout):
    duration = 0.5
    step_size = 20

    def __init__(self, **kwargs):
        super(Bunny, self).__init__(**kwargs)
        self.direction = utils.Direction.right

    def walk(self, keycode):
        if keycode != self.direction:
            # flip image and step
            self.direction = keycode

        offset = utils.Direction.key2dir[self.direction] * self.step_size

        Animation(x=(self.x + offset), y=self.y, duration=self.duration) \
            .start(self)
        self.sprite.play(duration=self.duration)

    def jump(self):
        # Animation(pos=(self.x, self.y-100)).start(self)
        # self.sprite.play(duration=self.duration)
        Animation(x=self.x + 10, y=self.y + 10).start(self)
        self.sprite.play(duration=self.duration)


class BunnyGame(FloatLayout):

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
