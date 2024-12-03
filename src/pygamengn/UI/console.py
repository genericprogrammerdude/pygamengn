import pygame

from pygamengn.UI.colour_panel import ColourPanel
from pygamengn.UI.component import Component
from pygamengn.UI.font_asset import FontAsset
from pygamengn.UI.root import Root
from pygamengn.UI.text_panel import TextPanel


class Console(Root):

    __CURSOR_LINE = ">"
    __CURSOR_BLINK_TIME = 800
    __CURSOR_CHARACTER = "[]"


    def __init__(self, hide_callback, size = (1.0 , 0.5), line_count = 15):
        line_height = 1 / line_count
        super().__init__(
            component = Component(
                size = size,
                children = [
                    ColourPanel(
                        name = "lines_panel",
                        colour = (30, 30, 30, 150),
                        children = [
                            TextPanel(
                                name = self._get_line_panel_name(i),
                                font_asset = FontAsset.monospace(),
                                text_colour = (0xFF, 0xBF, 0, 255),
                                auto_font_size = True,
                                auto_font_size_factor = 0.9,
                                pos = (0.01, line_height * i),
                                size = (0.99, line_height),
                                text = self.__CURSOR_LINE if i == 0 else "",
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
        self._cursor_line_index = 0
        self._line_count = line_count
        self._cursor_time = self.__CURSOR_BLINK_TIME
        self._show_cursor = False


    def update(self, delta: int) -> bool:
        self._cursor_time -= delta
        if self._cursor_time < 0:
            self._cursor_time = self.__CURSOR_BLINK_TIME
            self._show_cursor = not self._show_cursor
            lp = self._lp(self._cursor_line_index)
            if self._show_cursor:
                lp.text = lp.text + self.__CURSOR_CHARACTER
            else:
                if lp.text[-len(self.__CURSOR_CHARACTER):] == self.__CURSOR_CHARACTER:
                    lp.text = lp.text[:-len(self.__CURSOR_CHARACTER)]

        return super().update(delta)


    def handle_event(self, event: pygame.event.Event) -> bool:
        rv = False

        lp = self._lp(self._cursor_line_index)
        if self._show_cursor:
            # Get rid of the cursor before it causes confusion
            if lp.text[-len(self.__CURSOR_CHARACTER):] == self.__CURSOR_CHARACTER:
                lp.text = lp.text[:-len(self.__CURSOR_CHARACTER)]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKQUOTE:
                self._hide_callback()
                rv = True

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if lp.text[len(self.__CURSOR_LINE):] != "":
                    self._execute_command(lp.text[len(self.__CURSOR_LINE):])
                    self._increment_line_index()
                    rv = True

            elif event.key == pygame.K_BACKSPACE:
                if lp.text[len(self.__CURSOR_LINE):] != "":
                    lp.text = lp.text[:-1]
                    rv = True

            elif event.key == pygame.K_SPACE:
                lp.text = lp.text + " "
                rv = True

            else:
                key_name = pygame.key.name(event.key)
                if len(key_name) == 1:
                    lp.text = lp.text + key_name
                    rv = True

        if not rv:
            rv = super().handle_event(event)

        if self._show_cursor:
            # Add cursor again if appropriate. _cursor_line_index may have changed, so get the new line panel first
            lp = self._lp(self._cursor_line_index)
            lp.text = lp.text + self.__CURSOR_CHARACTER

        return rv


    def _execute_command(self, command: str):
        print(f"IMPLEMENT ME! Execute command `{command}`")


    def _increment_line_index(self):
        self._cursor_line_index += 1
        if self._cursor_line_index == self._line_count:
            prev_text = self._lp(0)
            for i in range(1, self._cursor_line_index):
                new_text = self._lp(i)
                prev_text.text = new_text.text
                prev_text = new_text
            self._cursor_line_index -= 1

        self._lp(self._cursor_line_index).text = self.__CURSOR_LINE


    def _lp(self, i: int) -> TextPanel:
        return self.__dict__.get(self._get_line_panel_name(i))


    def _get_line_panel_name(self, i: int) -> str:
        return f"line_{i:03d}"
