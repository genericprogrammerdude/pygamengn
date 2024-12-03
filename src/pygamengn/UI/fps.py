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
                        size = (0.06, 0.06),
                        horz_align = Panel.HorzAlign.RIGHT,
                        children = [
                            TextPanel(
                                name = "fps",
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                auto_font_size = True,
                                auto_font_size_factor = 0.9,
                                horz_align = Panel.HorzAlign.RIGHT,
                                vert_align = Panel.VertAlign.CENTRE,
                            ),
                        ],
                    ),
                ],
            ),
            update_on_pause = True,
            handles_input = False,
        )


    def update(self, delta: int) -> bool:
        self.fps.text = f"{round(1000 / delta):d}"
        return super().update(delta)
