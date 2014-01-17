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


class Rabbit(BoxLayout):
    movement = {'left': (-10, 0), 'right': (+10, 0), 'up': (0, +10), 'down': (0, -10)}
    duration = 0.5

    def __init__(self, **kwargs):
        super(Rabbit, self).__init__(**kwargs)

    def animate(self, keycode):
        offsets = self.movement[keycode]
        Animation(x=(self.x + offsets[0]), y=(self.y + offsets[1]), duration=self.duration) \
            .start(self)
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
        keycode_ = keycode[1]
        print 'keycode is ' + keycode_

        if keycode_ in ['up', 'down', 'left', 'right']:
            self.bunny.animate(keycode_)

        elif keycode_ == 'escape' or 'q':
            exit()

        return True


class BunnyApp(App):
    def build(self):
        return BunnyGame()


if __name__ == '__main__':
    BunnyApp().run()