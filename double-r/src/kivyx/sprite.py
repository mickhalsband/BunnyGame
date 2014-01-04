from functools import partial

from kivy.uix.image import Image
from kivy.resources import resource_find
from kivy.clock import Clock


class Sprite(Image):
    def __init__(self, sheet, **kwargs):
        Image.__init__(self, **kwargs)
        self.sheet = sheet
        self._frame = None
        self.frame = 0
        self.dt = None
        self.loop_fnc = None
        self.register_event_type("on_finish")
        
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, i):
        if self._frame != i:
            self.texture = self.sheet[i]
            self._frame = i

    def play(self, duration=1.0, start_frame=0):
        self.frame = start_frame
        self.dt = float(duration) / len(self.sheet)
        self.resume()

    def resume(self):
        Clock.schedule_interval(self.advance, self.dt)

    def pause(self):
        Clock.unschedule(self.advance)

    def advance(self, dt=None):
        if self._frame == len(self.sheet) - 1:
            self.pause()
            self.dispatch("on_finish")
        else:
            self.frame = self._frame + 1

    def loop(self, duration=1.0, start_frame=0, times=None):
        if self.loop_fnc is not None:
            raise Exception("sprite is already looping")
        self.loop_fnc = partial(Sprite._loop, duration=duration,
                                start_frame=start_frame, times=times)
        self.loop_fnc(self)
        self.bind(on_finish=self.loop_fnc)

    def _loop(self, duration, start_frame, times):
        if times == 0:
            self.break_loop()
        else:
            if times is not None:
                self.loop_fnc.keywords["times"] = times - 1
            self.play(duration, start_frame)

    def break_loop(self):
        self.unbind(on_finish=self.loop_fnc)
        self.loop_fnc = None

    def on_finish(self):
        """Default event handler for 'on_finish' (this is required by kivy...)"""


class SpriteSheet(object):
    def __init__(self, source, rows=1, cols=1):
        if isinstance(source, str):
            source = Image(source=resource_find(source))
        self.texture = source.texture
        self.frame_width = self.texture.width / cols
        self.frame_height = self.texture.height / rows
        self.frames = [None] * (rows * cols)
        self.rows = rows
        self.cols = cols

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, i):
        frame = self.frames[i]
        if frame is None:
            y, x = divmod(i, self.cols)
            w, h = self.frame_width, self.frame_height
            frame = self.texture.get_region(x * w, y * h, w, h)
            self.frames[i] = frame
        return frame

    def __setitem__(self, i, texture):
        self.frames[i] = texture

    def append(self, texture):
        self.frames.append(texture)


Sprite.Sheet = SpriteSheet
