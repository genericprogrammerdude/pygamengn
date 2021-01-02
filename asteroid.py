import pygame

from game_object_factory import GameObjectFactory
from projectile import Projectile


@GameObjectFactory.register("Asteroid")
class Asteroid(Projectile):

    def __init__(self, image, enemies, damage, death_effect, mover):
        super().__init__(image, enemies, damage, death_effect, mover)
        self.spin_angle = 0

    def update(self, delta):
        self.spin_angle = (self.spin_angle + 1) % 360
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        self.image = pygame.transform.rotozoom(self.image_original, self.spin_angle, self.scale)
        self.mask = pygame.mask.from_surface(self.image, 16)

        # Translate
        self.rect = self.image.get_rect()
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

        self.handle_collisions()
