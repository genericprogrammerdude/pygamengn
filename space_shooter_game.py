import random

import pygame

from game import BlitSurface
from game import Game
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("SpaceShooterGame")
class SpaceShooterGame(Game):

    def __init__(self, font, text_colour, **kwargs):
        super().__init__(**kwargs)
        self.font = font
        self.text_colour = text_colour
        self.time = 0
        self.score = 0
        self.player = None
        self.cooldown_time = 0
        self.player_is_dead = False
        self.running = True

        # Assign biggest rectangle for time and score text
        s = "00:00"
        surface = self.font.font.render(s, True, self.text_colour)
        self.time_text_width = surface.get_rect().width
        s = "0000"
        surface = self.font.font.render(s, True, self.text_colour)
        self.score_text_width = surface.get_rect().width

    def update(self, delta):
        self.handle_input()

        # Track round time and score
        if not self.player is None and self.player.alive() and not self.is_paused:
            self.time += delta
            self.score = self.player.score

        # Put time and score text together
        time_surface = self.build_time_text_surface()
        score_surface = self.build_score_text_surface()
        self.add_blit_surface(BlitSurface(time_surface, (self.screen.get_rect().width - self.time_text_width, 0)))
        self.add_blit_surface(BlitSurface(score_surface, (self.score_text_width - score_surface.get_rect().width, 0)))

        if self.player_is_dead:
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

    def build_time_text_surface(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        surface = self.font.font.render("{:02d}:{:02d}".format(min, sec), True, self.text_colour)
        return surface

    def build_score_text_surface(self):
        surface = self.font.font.render("{:03d}".format(self.score), True, self.text_colour)
        return surface
