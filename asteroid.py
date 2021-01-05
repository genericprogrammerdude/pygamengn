import random

import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory
from projectile import Projectile
from render_group import RenderGroup


@GameObjectFactory.register("Asteroid")
class Asteroid(Projectile):

    def __init__(self, images, damage, death_effect, mover, death_spawn):
        super().__init__(random.choice(images), damage, death_effect, mover)
        self.spin_angle = random.randrange(0, 360)
        self.spin_delta_factor = random.choice([-1.0, 1.0])
        self.death_spawn = death_spawn
        self.death_spawn_pos = None
        self.mover.set_velocity(self.mover.velocity * (0.5 + random.random()))

    def update(self, delta):
        spin_delta = (self.mover.angular_velocity * delta) / 1000.0 * self.spin_delta_factor
        self.spin_angle = self.spin_angle + spin_delta
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        self.image = pygame.transform.rotozoom(self.image_original, self.spin_angle, self.scale)
        self.mask = pygame.mask.from_surface(self.image, 16)

        # Translate
        self.rect = self.image.get_rect()
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        self.death_spawn_pos = world_pos
        self.take_damage(self.health)
        # Apply damage to the collided sprite
        gob.take_damage(self.damage)

    def die(self):
        """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
        if self.death_spawn and self.alive():
            for spawn_type in self.death_spawn:
                spawn = GameObjectFactory.create(spawn_type)
                spawn.set_pos(self.death_spawn_pos)
                heading_delta = 90.0 * (random.random() - 0.5)
                spawn.set_heading(self.heading + heading_delta)
        super().die()


@GameObjectFactory.register("AsteroidSpawner")
class AsteroidSpawner(GameObjectBase):
    """Spawns asteroids just to be annoying."""

    def __init__(self, asteroid_types, spawn_freq, render_group):
        self.asteroid_types = asteroid_types
        self.spawn_freq = spawn_freq
        self.time_to_next_spawn = random.randrange(spawn_freq)
        self.render_group = render_group

    def update(self, delta):
        self.time_to_next_spawn -= delta
        if self.time_to_next_spawn <= 0:
            self.time_to_next_spawn = random.randrange(self.spawn_freq)
            asteroid_type = random.choice(self.asteroid_types)
            asteroid = GameObjectFactory.create(asteroid_type)
            asteroid.set_pos(pygame.Vector2(640, 360))
            asteroid.set_heading(random.randrange(0, 360))
            self.render_group.get_world_view_rect()
