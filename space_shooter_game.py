import random

import pygame

from game import BlitSurface
from game import Game
from game_object_factory import GameObjectFactory
from main_menu import MainMenu


@GameObjectFactory.register("SpaceShooterGame")
class SpaceShooterGame(Game):

    def __init__(self, main_menu_ui, score_ui, time_ui, **kwargs):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        self.score_ui = score_ui
        self.time_ui = time_ui
        self.time = 0
        self.score = 0
        self.player = None
        self.cooldown_time = 0
        self.player_is_dead = False
        self.running = True

    def update(self, delta):
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

        if self.player_is_dead:
            self.main_menu_ui.update(screen_rect, delta)
            self.blit_ui(self.main_menu_ui)
            if self.cooldown_time > 0:
                self.cooldown_time -= delta
                if self.cooldown_time < 0:
                    self.cooldown_time = 0
                    # Reset game state
                    self.kill_render_group()
                    self.pause_updatables = True
            else:
                # Keep killing game objects until there's nothing left in render group
                if len(self.render_group.sprites()) > 0:
                    self.kill_render_group()
                else:
                    # Everyone's dead. Reload.
                    self.player_is_dead = False
                    self.level.create_objects(self.render_group)
                    self.set_level(self.level)
                    self.set_player(self.level.player)
                    # Resume updatable updates
                    self.pause_updatables = False
                    self.time = 0

        super().update(delta)

    def handle_input(self):
        """Reads input and makes things happen."""
        if self.player is None:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.fire()
                if event.key == pygame.K_END:
                    self.toggle_pause()

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
        self.player_is_dead = True
        self.cooldown_time = 1000
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
