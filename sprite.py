from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.image import Image

__author__ = 'mick'


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