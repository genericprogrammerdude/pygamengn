from enum import Enum, auto
import random

import pygame

from game import BlitSurface
from game import Game
from game_object_factory import GameObjectFactory
from level import Level
from main_menu import MainMenu
from shield import Shield
from ship import Ship
from sprite_group import SpriteGroup


class Mode(Enum):
    """The mode of the SpaceShooterGame defines game behaviour."""
    MAIN_MENU = auto()
    PLAY = auto()


@GameObjectFactory.register("SpaceShooterGame")
class SpaceShooterGame(Game):

    def __init__(self, main_menu_ui, score_ui, time_ui, level, **kwargs):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        self.score_ui = score_ui
        self.time_ui = time_ui
        self.level = level
        self.time = 0
        self.score = 0
        self.running = True
        self.mode = Mode.MAIN_MENU

    def update(self, delta):
        """Updates the game."""

        if self.mode == Mode.PLAY:
            self.update_play(delta)

        elif self.mode == Mode.MAIN_MENU:
            self.update_main_menu(delta)

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

    def update_main_menu(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.mode = Mode.PLAY
                self.level.create_objects(self.render_group)
                self.set_player(self.level.player)
                self.time = 0

        self.main_menu_ui.update(self.screen.get_rect(), delta)
        self.blit_ui(self.main_menu_ui)

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE and self.player:
                    self.player.fire()
                if event.key == pygame.K_END:
                    self.toggle_pause()

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
        self.killing = True
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
