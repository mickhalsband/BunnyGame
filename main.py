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
    def __init__(self, **kwargs):
        super(Rabbit, self).__init__(**kwargs)


class BunnyGame(FloatLayout):
    movement = {'left': (-10, 0), 'right': (+10, 0), 'up': (0, +10), 'down': (0, -10)}

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
            offsets = self.movement[keycode_]
            self.animate_bunny(offsets)

        elif keycode_ == 'escape' or 'q':
            exit()

        return True

    def animate_bunny(self, (x_offset, y_offset)):
        a = Animation(x=(self.bunny.x + x_offset), y=(self.bunny.y + y_offset), duration=0.1)
        a.start(self.bunny)


class BunnyApp(App):
    def build(self):
        return BunnyGame()


if __name__ == '__main__':
    BunnyApp().run()