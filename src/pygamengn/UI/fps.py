import pygame

from pygamengn.class_registrar import ClassRegistrar

from pygamengn.UI.colour_panel import ColourPanel
from pygamengn.UI.component import Component
from pygamengn.UI.font_asset import FontAsset
from pygamengn.UI.panel import Panel
from pygamengn.UI.root import Root
from pygamengn.UI.text_panel import TextPanel


@ClassRegistrar.register("Fps")
class Fps(Root):

    def __init__(self):
        super().__init__(
            component = Component(
                children = [
                    ColourPanel(
                        colour = (30, 30, 30, 150),
                        size = (0.06, 0.1),
                        horz_align = Panel.HorzAlign.RIGHT,
                        children = [
                            TextPanel(
                                name = "fps",
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                size = (1.0, 0.25),
                                horz_align = Panel.HorzAlign.RIGHT,
                                pos = (0, 0),
                                text = "FPS: 00",
                            ),
                            TextPanel(
                                name = "avg",
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                size = (1.0, 0.25),
                                horz_align = Panel.HorzAlign.RIGHT,
                                pos = (0, 0.25),
                                text = "Avg: 00",
                            ),
                            TextPanel(
                                name = "min",
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                size = (1.0, 0.25),
                                horz_align = Panel.HorzAlign.RIGHT,
                                pos = (0, 0.5),
                                text = "Min: 00",
                            ),
                            TextPanel(
                                name = "max",
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                size = (1.0, 0.25),
                                horz_align = Panel.HorzAlign.RIGHT,
                                pos = (0, 0.75),
                                text = "Max: 00",
                            ),
                        ],
                    ),
                ],
            ),
            update_on_pause = True,
            handles_input = False,
        )
        self._min = 500
        self._max = -500
        self._count = 0
        self._accum = 0
        self.__uniform_font_panels = [self.fps, self.avg, self.min, self.max]


    def update(self, delta: int) -> bool:
        fps = round(1000 / delta)
        if fps < self._min:
            self._min = fps
        if fps > self._max:
            self._max = fps
        self._accum += fps
        self._count += 1

        self.fps.text = f"FPS: {fps:d}"
        self.avg.text = f"Avg: {round(self._accum / self._count):d}"
        self.min.text = f"Min: {self._min}"
        self.max.text = f"Max: {self._max}"

        return super().update(delta)


    def set_parent_rect(self, rect: pygame.Rect):
        super().set_parent_rect(rect)
        self._set_uniform_font_size(self.__uniform_font_panels, 0.9)


    def fade_in(self, duration: int):
        self._min = 500
        self._max = -500
        self._count = 0
        self._accum = 0
        super().fade_in(duration)
