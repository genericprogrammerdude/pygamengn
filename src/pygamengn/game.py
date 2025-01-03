import logging

import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.console_registrar import ConsoleRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.input_handler import InputHandler, DefaultInputHandler

from pygamengn.UI.console import Console
from pygamengn.UI.fps import Fps
from pygamengn.UI.root import Root


@ClassRegistrar.register("Game")
class Game(DefaultInputHandler):
    """Highest level entity to manage game state."""

    # Game administration functions
    def __init__(self, render_group, collision_manager, screen, replication_manager = None, **kwargs):
        super().__init__(**kwargs)
        self._render_group = render_group
        self._collision_manager = collision_manager
        self._replication_manager = replication_manager
        self._screen = screen
        self._is_paused = False
        self._running = True
        self._blit_surfaces = []
        self._player = None
        self._uis = []
        self._input_stack = [self]
        self._fps_ui = Fps()
        self._console_ui = Console(self.toggle_console)
        ConsoleRegistrar.register("fps", lambda: self.toggle_ui(self._fps_ui, 300))


    def update(self, delta):
        """Updates the game."""

        # Process input
        self._process_input()

        if self._is_paused:
            real_delta = delta
            delta = 0

        # Update game objects for rendering
        self._render_group.update(self._screen.get_rect(), delta)

        # Do collision detection and notification
        self._collision_manager.do_collisions()

        # Do data replication as appropriate
        if self._replication_manager:
            self._replication_manager.update(delta)

        # Update any active UI screens
        i = 0
        while i < len(self._uis):
            ui = self._uis[i]
            if not ui.update(real_delta if self._is_paused and ui.update_on_pause else delta):
                self._uis.pop(i)
            else:
                i += 1

        # Draw things on the screen
        self._render_group.draw(self._screen)
        self.direct_draw()
        self._screen.blits(
            [(bs.surface, bs.topleft, None, pygame.BLEND_ALPHA_SDL2) for bs in self._blit_surfaces],
            doreturn = False
        )
        for ui in self._uis:
            ui.blit_to_surface(self._screen)
        pygame.display.flip()
        self._blit_surfaces.clear()


    @property
    def running(self) -> bool:
        return self._running



    # Input functions
    def _process_input(self):
        """
        Processes input.

        Input events are forwarded to the InputHandler at the top of the stack. Any events that the handler ignores
        will fall through and Game may choose to handle them (e.g., pygame.QUIT should always be handled). This
        simplistic input handling scheme makes it so that only one handler can be active at any given time.
        """
        for event in pygame.event.get():
            if not self._input_stack[-1].handle_event(event):
                processed = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f and event.mod & pygame.KMOD_CTRL:
                        self.toggle_ui(self._fps_ui)
                        processed = True
                if not processed:
                    self.handle_event(event)


    def push_input_handler(self, input_handler: InputHandler):
        """
        Pushes the given InputHandler to the input stack.  The given handler will own input while it remains at the
        top.
        """
        self._input_stack[-1].deactivate()
        self._input_stack.append(input_handler)
        input_handler.activate()
        logging.info(f"Pushed {input_handler}")


    def pop_input_handler(self, input_handler: InputHandler):
        assert(self._input_stack[-1] == input_handler)
        input_handler.deactivate()
        self._input_stack.pop()
        self._input_stack[-1].activate()
        logging.info(f"Popped {input_handler}")


    def exit_game(self):
        """Flags that the game is ready to stop execution and exit the application."""
        self._running = False


    def resize_window(self, rect: pygame.Rect):
        for ui in self._uis:
            ui.set_parent_rect(rect)


    def toggle_console(self):
        showing_console = self.toggle_ui(self._console_ui, 300)
        if showing_console:
            self._console_ui.restore_pause_state = self._is_paused
            self._is_paused = True
        else:
            self._is_paused = self._console_ui.restore_pause_state



    # Gameplay functions
    def set_player(self, player):
        """Tells the updateables which game object is the player."""
        self._player = player
        self._player.die_callback(self.handle_player_death)

    def toggle_pause(self):
        self._is_paused = not self._is_paused

    def handle_player_death(self):
        """Invoked when the player dies."""
        pass


    # Drawing functions
    def direct_draw(self):
        """Invoked after drawing render_group to the screen. Implement this for any direct-drawing needs."""
        pass

    def add_blit_surface(self, blit_surface):
        """Adds a surface to blit when rendering. The list gets cleared after every game update."""
        self._blit_surfaces.append(blit_surface)


    # UI management functions
    def show_ui(self, ui: Root, fade_in_ms: int = 0):
        """
        Shows the specified ui, fading it into the screen during fade_in_ms number of ms.

        After a UI Root is shown, its update() method will be invoked as part of Game's update loop until the UI
        is hidden.
        """
        if ui not in self._uis:
            self._uis.append(ui)
        ui.set_parent_rect(self._screen.get_rect())
        ui.fade_in(fade_in_ms)
        if ui.handles_input:
            self.push_input_handler(ui)


    def hide_ui(self, ui: Root, fade_out_ms: int = 0):
        """Hides the specified ui, fading it into the screen during fade_in_ms number of ms."""
        if ui in self._uis:
            ui.fade_out(fade_out_ms)
            if ui.handles_input:
                self.pop_input_handler(ui)


    def toggle_ui(self, ui: Root, fade_ms: int = 0) -> bool:
        """Shows or hides a UI, depending on whether it's currently being shown."""
        if ui in self._uis:
            self.hide_ui(ui, fade_ms)
            return False
        else:
            self.show_ui(ui, fade_ms)
            return True
