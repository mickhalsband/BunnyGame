from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
import utils
from bunny import Bunny

__author__ = 'mick'


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