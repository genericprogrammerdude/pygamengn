import pygame

from pygamengn.UI.root import Root
from pygamengn.UI.component import Component
from pygamengn.UI.colour_panel import ColourPanel


class Console(Root):

    def __init__(self, hide_callback):
        super().__init__(
            component = Component(
                size = (1.0, 0.3),
                children = [
                    ColourPanel(
                        colour = (30, 30, 30, 150),
                        border_width = 0.01,
                        border_colour = (0xFF, 0xBF, 0, 255),
                    )
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
