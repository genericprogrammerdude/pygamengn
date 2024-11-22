from enum import Enum, auto
import random

import pygame
import pygamengn

from debrief_ui import DebriefUI
from main_menu import MainMenu
from pause_menu import PauseMenu
from shield import Shield
from ship import Ship
from waypoint import Waypoint


class Mode(Enum):
    """The mode of the AsteroidShooterGame defines game behaviour."""
    MAIN_MENU = auto()
    PLAY = auto()
    PAUSE_MENU = auto()
    KILLING_ALL = auto()
    DEBRIEF = auto()


class InputAction(Enum):
    """The input actions the game understands."""
    FORWARD = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    FIRE = auto()


@pygamengn.ClassRegistrar.register("AsteroidShooterGame")
class AsteroidShooterGame(pygamengn.Game):

    def __init__(
            self,
            main_menu_ui,
            pause_menu_ui,
            debrief_ui,
            hud_ui,
            level,
            asteroid_multiplier,
            waypoint_multiplier,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        self.pause_menu_ui = pause_menu_ui
        self.debrief_ui = debrief_ui
        self.hud_ui = hud_ui
        self.level = level
        self.asteroid_multiplier = asteroid_multiplier
        self.waypoint_multiplier = waypoint_multiplier
        self.ui_fade_duration = 200

        self.time = 0
        self.score = 0
        self.mode = Mode.MAIN_MENU

        self.main_menu_ui.set_start_callback(self.start_play)
        self.main_menu_ui.set_exit_callback(self.exit_game)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration)

        self.pause_menu_ui.set_resume_callback(self.resume_play)
        self.pause_menu_ui.set_exit_callback(self.exit_game)

        self.debrief_ui.set_continue_callback(self.go_to_main_menu)

    def update(self, delta):
        """Updates the game."""

        if self.mode == Mode.PLAY:
            self.update_play(delta)

        elif self.mode == Mode.MAIN_MENU:
            pass

        elif self.mode == Mode.PAUSE_MENU:
            pass

        elif self.mode == Mode.KILLING_ALL:
            self.update_killing(delta)

        elif self.mode == Mode.DEBRIEF:
            pass

        super().update(delta)


    def update_play(self, delta):
        # Track round time and score
        if not self._player is None and self._player.alive() and not self._is_paused:
            self.time += delta
            self.score = self._player.score

        # Put time and score text together
        self.hud_ui.score_text.text = f"{self.score}"
        self.hud_ui.time_text.text = f"{self.get_time_string()}"

        self.level.update(delta)


    def update_killing(self, delta):
        """Updates game states when killing all game objects in the render group before starting play mode."""
        self.kill_render_group()
        if len(self._render_group.sprites()) <= 0:
            self.mode = Mode.PLAY
            self.level.create_objects(self._render_group)
            self.set_player(self.level.player)
            self.time = 0


    def start_play(self):
        """Prepares the game to start playing."""
        self.time = 0
        self.score = 0
        self.hud_ui.score_text.text = "0"
        self.hud_ui.time_text.text = "00:00"
        self.mode = Mode.KILLING_ALL
        pygame.mouse.set_visible(False)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration)
        self.toggle_ui(self.hud_ui, self.ui_fade_duration)


    def resume_play(self):
        """Resumes PLAY mode from PAUSE_MENU mode."""
        self.mode = Mode.PLAY
        pygame.mouse.set_visible(False)
        self.toggle_pause()
        self.toggle_ui(self.pause_menu_ui, self.ui_fade_duration)


    def go_to_main_menu(self):
        """Goes back to the main menu after showing the debrief UI."""
        self.mode = Mode.MAIN_MENU
        pygame.mouse.set_visible(True)
        self.toggle_ui(self.debrief_ui, self.ui_fade_duration)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration)
        self.toggle_ui(self.hud_ui, self.ui_fade_duration)


    def handle_event(self, event: pygame.event) -> bool:
        """Reads input and makes things happen."""
        rv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
                self.toggle_ui(self.pause_menu_ui, self.ui_fade_duration)
                self.mode = Mode.PAUSE_MENU
                pygame.mouse.set_visible(True)
                rv = True
            if event.key == pygame.K_SPACE and self._player:
                self._player.fire()
                rv = True
        else:
            rv = super().handle_event(event)

        return rv


    def _process_input(self):
        # Handle input for movement
        super()._process_input()
        if self._player:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                self._player.heading = self._player.heading + self._player.mover.angular_velocity
            if pressed_keys[pygame.K_d]:
                self._player.heading = self._player.heading - self._player.mover.angular_velocity
            if pressed_keys[pygame.K_w]:
                self._player.set_velocity(self._player.mover.max_velocity)
            if pressed_keys[pygame.K_s]:
                self._player.set_velocity(self._player.mover.velocity * 0.8)


    def handle_player_death(self):
        """Invoked when the _player dies."""
        self.mode = Mode.DEBRIEF
        self.debrief_ui.set_score_data(
            self.score,
            self.time,
            self._player.kills,
            self._player.waypoints,
            self.asteroid_multiplier,
            self.waypoint_multiplier
        )
        pygame.mouse.set_visible(True)
        self.toggle_ui(self.debrief_ui, self.ui_fade_duration)
        self._player = None


    def kill_render_group(self):
        gobs = self._render_group.sprites()
        for gob in gobs:
            gob.take_damage(random.randint(0, 5), None)


    def get_time_string(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        return "{:02d}:{:02d}".format(min, sec)
