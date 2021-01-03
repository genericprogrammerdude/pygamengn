import random

import pygame

from game_object_factory import GameObjectFactory
from projectile import Projectile


@GameObjectFactory.register("Asteroid")
class Asteroid(Projectile):

    def __init__(self, image, damage, death_effect, mover, death_spawn):
        super().__init__(image, damage, death_effect, mover)
        self.spin_angle = 0
        self.death_spawn = death_spawn

    def update(self, delta):
        self.spin_angle = (self.spin_angle + 1) % 360
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        self.image = pygame.transform.rotozoom(self.image_original, self.spin_angle, self.scale)
        self.mask = pygame.mask.from_surface(self.image, 16)

        # Translate
        self.rect = self.image.get_rect()
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        self.take_damage(self.health)
        # Apply damage to the collided sprite
        gob.take_damage(self.damage)

    def die(self):
        """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
        if self.death_spawn and self.alive():
            for spawn_type in self.death_spawn:
                spawn = GameObjectFactory.create(spawn_type)
                spawn.add_to_groups(self.groups())
                spawn.set_pos(pygame.Vector2(640, 370))
                heading_delta = 60.0 * (random.random() - 0.5)
                spawn.set_heading(self.heading + heading_delta)
                velocity = self.mover.velocity * (0.5 + random.random())
                spawn.mover.set_velocity(velocity)
                spawn.transform()
        super().die()
