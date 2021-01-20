from enum import Enum, auto
import random

import numpy
import pygame

from game import BlitSurface
from game import Game
from game_object_factory import GameObjectFactory
from level import Level
from main_menu import MainMenu
from pause_menu import PauseMenu
from shield import Shield
from ship import Ship
from sprite_group import SpriteGroup
from waypoint import Waypoint


class Mode(Enum):
    """The mode of the SpaceShooterGame defines game behaviour."""
    MAIN_MENU = auto()
    PLAY = auto()
    PAUSE_MENU = auto()
    KILLING_ALL = auto()


@GameObjectFactory.register("SpaceShooterGame")
class SpaceShooterGame(Game):

    def __init__(self, main_menu_ui, pause_menu_ui, score_ui, time_ui, level, waypoint_type, **kwargs):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        self.pause_menu_ui = pause_menu_ui
        self.score_ui = score_ui
        self.time_ui = time_ui
        self.level = level
        self.waypoint_type = waypoint_type
        self.waypoint = None
        self.time = 0
        self.score = 0
        self.running = True
        self.mode = Mode.MAIN_MENU
        self.main_menu_ui.set_start_callback(self.start_play)
        self.main_menu_ui.set_exit_callback(self.exit_game)
        self.pause_menu_ui.set_resume_callback(self.resume_play)
        self.pause_menu_ui.set_exit_callback(self.exit_game)

    def update(self, delta):
        """Updates the game."""

        if self.mode == Mode.PLAY:
            pygame.mouse.set_visible(False)
            self.update_play(delta)

        elif self.mode == Mode.MAIN_MENU:
            self.update_ui(delta, self.main_menu_ui)

        elif self.mode == Mode.PAUSE_MENU:
            self.update_ui(delta, self.pause_menu_ui)

        elif self.mode == Mode.KILLING_ALL:
            pygame.mouse.set_visible(False)
            self.update_killing(delta)

        super().update(delta)

    def update_play(self, delta):
        self.handle_input()

        # Track round time and score
        if not self.player is None and self.player.alive() and not self.is_paused:
            self.time += delta
            self.score = self.player.score

        # Put time and score text together
        screen_rect = self.screen.get_rect()
        self.score_ui.children[0].set_text(str(self.score))
        self.time_ui.children[0].set_text(self.get_time_string())
        self.score_ui.update(screen_rect, delta)
        self.time_ui.update(screen_rect, delta)
        self.blit_ui(self.score_ui)
        self.blit_ui(self.time_ui)

        self.level.update(delta)

    def update_ui(self, delta, ui):
        """Updates the given UI component."""
        pygame.mouse.set_visible(True)
        if self.time > 0:
            self.blit_ui(self.score_ui)
            self.blit_ui(self.time_ui)
        ui.update(self.screen.get_rect(), delta)
        self.blit_ui(ui)

    def update_killing(self, delta):
        """Updates game states when killing all game objects in the render group before starting play mode."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.kill_render_group()
        if len(self.render_group.sprites()) <= 0:
            self.mode = Mode.PLAY
            self.level.create_objects(self.render_group)
            self.set_player(self.level.player)
            self.time = 0
            self.create_waypoint()

    def create_waypoint(self, gob=None):
        """Creates a new waypoint."""
        if self.waypoint:
            self.waypoint.die(self.player)
        angle = numpy.deg2rad(random.randrange(0, 360))
        self.waypoint = GameObjectFactory.create(self.waypoint_type)
        pos = self.player.pos + self.waypoint.distance * pygame.Vector2(numpy.cos(angle), numpy.sin(angle))
        self.waypoint.set_pos(pos)
        self.waypoint.set_enter_callback(self.create_waypoint)
        if gob:
            # The presence of a valid gob indicates we're here as a result of a collision
            self.player.increment_waypoint_count()
        self.player.set_waypoint(self.waypoint)

    def start_play(self):
        """Prepares the game to start playing."""
        self.mode = Mode.KILLING_ALL

    def resume_play(self):
        """Resumes PLAY mode from PAUSE_MENU mode."""
        self.mode = Mode.PLAY
        self.toggle_pause()

    def exit_game(self):
        """Exits the application."""
        self.running = False

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                    self.mode = Mode.PAUSE_MENU
                if event.key == pygame.K_SPACE and self.player:
                    self.player.fire()

        if self.player is None:
            return

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.player.set_heading(self.player.heading + self.player.mover.angular_velocity)
        if pressed_keys[pygame.K_d]:
            self.player.set_heading(self.player.heading - self.player.mover.angular_velocity)
        if pressed_keys[pygame.K_w]:
            self.player.set_velocity(self.player.mover.max_velocity)
        if pressed_keys[pygame.K_s]:
            self.player.set_velocity(self.player.mover.velocity * 0.8)

    def handle_player_death(self):
        """Invoked when the player dies."""
        self.mode = Mode.MAIN_MENU
        self.player = None

    def kill_render_group(self):
        gobs = self.render_group.sprites()
        for gob in gobs:
            gob.take_damage(random.randint(0, 5), None)

    def get_time_string(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        return "{:02d}:{:02d}".format(min, sec)

    def blit_ui(self, ui):
        self.add_blit_surface(BlitSurface(ui.image, ui.rect))
        for child in ui.children:
            self.blit_ui(child)
