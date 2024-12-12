from enum import Enum, auto
import random

import pygame
import pygamengn

from debrief_ui import DebriefUI
from hud import Hud
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

        self.pause_menu_ui.set_resume_callback(self.resume_play)
        self.pause_menu_ui.set_main_menu_callback(self.go_to_main_menu)

        self.hud_ui.set_pause_callback(self.pause_game)

        self.debrief_ui.set_continue_callback(self.go_to_main_menu)

        self.mode = Mode.MAIN_MENU
        self.main_menu_ui.set_start_callback(self.start_play)
        self.main_menu_ui.set_exit_callback(self.exit_game)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration)

        # DEBUG #
        # self.start_play(True)
        # DEBUG #

    def update(self, delta):
        """Updates the game."""

        if self.mode == Mode.PLAY:
            self.update_play(delta)

        elif self.mode == Mode.KILLING_ALL:
            self.update_killing(delta)

        super().update(delta)


    def update_play(self, delta):
        # Track round time and score
        if self._player and self._player.alive() and not self._is_paused:
            self.time += delta
            self.score = self._player.score

            if self.hud_ui.touch_joystick_active:
                heading_diff = self.hud_ui.heading - self._player.heading
                heading_diff = (heading_diff + 180) % 360 - 180
                if heading_diff < 0:
                    heading_delta = max(
                        heading_diff,
                        -delta * self._player.mover.angular_velocity / 1000
                    )
                else:
                    heading_delta = min(
                        heading_diff,
                        delta * self._player.mover.angular_velocity / 1000
                    )
                self._player.heading += heading_delta
                if self.hud_ui.joystick_motion:
                    self._player.set_velocity(self._player.mover.max_velocity)

                if self.hud_ui.fire:
                    self._player.fire()

            # Process move keys
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                self._player.heading = self._player.heading + delta * self._player.mover.angular_velocity / 1000
            if pressed_keys[pygame.K_d]:
                self._player.heading = self._player.heading - delta * self._player.mover.angular_velocity / 1000
            if pressed_keys[pygame.K_w]:
                self._player.set_velocity(self._player.mover.max_velocity)
            if pressed_keys[pygame.K_s]:
                self._player.set_velocity(self._player.mover.velocity * 0.8)

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
            self.score = 0
            self.toggle_ui(self.hud_ui, self.ui_fade_duration)


    def start_play(self, touch_input: bool):
        """Prepares the game to start playing."""
        self.mode = Mode.KILLING_ALL
        pygame.mouse.set_visible(False)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration)
        self.hud_ui.set_joystick_state(touch_input)


    def resume_play(self):
        """Resumes PLAY mode from PAUSE_MENU mode."""
        self.mode = Mode.PLAY
        pygame.mouse.set_visible(False)
        self.toggle_pause()
        self.toggle_ui(self.pause_menu_ui, self.ui_fade_duration)


    def go_to_main_menu(self):
        """Goes back to the main menu after showing the debrief UI."""
        pygame.mouse.set_visible(True)
        if self.mode == Mode.DEBRIEF:
            self.toggle_ui(self.debrief_ui, self.ui_fade_duration)
            self.toggle_ui(self.hud_ui, self.ui_fade_duration)
        else:
            assert(self._is_paused)
            self.kill_render_group(1000)
            self.toggle_pause()
            self.toggle_ui(self.pause_menu_ui, self.ui_fade_duration)
            self.toggle_ui(self.hud_ui, self.ui_fade_duration)
        self.toggle_ui(self.main_menu_ui, self.ui_fade_duration * 2)
        self.mode = Mode.MAIN_MENU


    def pause_game(self):
        self.toggle_pause()
        self.toggle_ui(self.pause_menu_ui, self.ui_fade_duration)
        self.mode = Mode.PAUSE_MENU
        pygame.mouse.set_visible(True)


    def handle_event(self, event: pygame.event) -> bool:
        """Reads input and makes things happen."""
        rv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_game()
                rv = True
            elif event.key == pygame.K_SPACE:
                if self._player:
                    self._player.fire()
                    rv = True

        if not rv:
            rv = super().handle_event(event)

        return rv


    def handle_player_death(self):
        """Invoked when the _player dies."""
        if self.mode == Mode.PLAY:
            self.mode = Mode.DEBRIEF
            self.debrief_ui.set_score_data(
                self.score,
                self.time,
                self._player.kills,
                self._player.waypoints,
                self.asteroid_multiplier,
                self.waypoint_multiplier
            )
            self.toggle_ui(self.debrief_ui, self.ui_fade_duration)
            pygame.mouse.set_visible(True)
            self._player = None


    def kill_render_group(self, damage: int = 0):
        god_mode = Ship.god_mode()
        if god_mode:
            Ship.toggle_god_mode()
        [
            sprite.take_damage(random.randint(0, 5) if damage == 0 else damage, None)
            for sprite in self._render_group.sprites()
        ]
        if god_mode:
            Ship.toggle_god_mode()



    def get_time_string(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        return "{:02d}:{:02d}".format(min, sec)
