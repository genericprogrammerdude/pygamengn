import pygame

from pygamengn.UI.colour_panel import ColourPanel
from pygamengn.UI.component import Component
from pygamengn.UI.font_asset import FontAsset
from pygamengn.UI.root import Root
from pygamengn.UI.text_panel import TextPanel


class Console(Root):

    def __init__(self, hide_callback, size = (1.0 , 0.5), line_count = 20):
        line_height = 1 / line_count
        super().__init__(
            component = Component(
                size = size,
                children = [
                    ColourPanel(
                        colour = (30, 30, 30, 150),
                        children = [
                            TextPanel(
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                auto_font_size = True,
                                auto_font_size_factor = 0.9,
                                name = f"line_{i:0d}",
                                pos = (0.01, line_height * i),
                                size = (0.99, line_height),
                                text = "> line with more text than the other IILLL1gj P" if i == 0 else "> line {i}",
                            ) for i in range(line_count)
                        ],
                    ),
                ],
            ),
            handles_input = True,
            update_on_pause = True,
        )
        self.restore_pause_state = False
        self._hide_callback = hide_callback


    def handle_event(self, event: pygame.event.Event) -> bool:
        rv = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKQUOTE:
                self._hide_callback()
                rv = True

        if not rv:
            rv = super().handle_event(event)

        return rv
