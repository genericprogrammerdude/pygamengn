import pygame

from game_object_factory import GameObjectFactory
from projectile import Projectile


@GameObjectFactory.register("Asteroid")
class Asteroid(Projectile):

    def __init__(self, image, enemies, damage, death_effect, mover, death_spawn):
        super().__init__(image, enemies, damage, death_effect, mover)
        self.spin_angle = 0
        self.death_spawn = death_spawn

    def update(self, delta):
        self.spin_angle = (self.spin_angle + 1) % 360
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        print(self.heading)
        self.image = pygame.transform.rotozoom(self.image_original, self.spin_angle, self.scale)
        self.mask = pygame.mask.from_surface(self.image, 16)

        # Translate
        self.rect = self.image.get_rect()
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

        self.handle_collisions()

    def handle_collisions(self):
        """Checks for collisions."""
        if self.enemies:
            collisions = pygame.sprite.spritecollide(self, self.enemies, False, self.sprites_collided)
            for sprite in collisions:
                collision = pygame.sprite.collide_mask(sprite, self)
                if collision:
                    # Set own position to the collision point so the explosion will play there when self dies
                    self.set_pos(pygame.Vector2(sprite.rect.topleft) + collision)
                    self.take_damage(self.health)
                    # Apply damage to the collided sprite
                    sprite.take_damage(self.damage)

#     def die(self):
#         """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
#         if self.death_spawn and self.alive():
#             effect = GameObjectFactory.create(self.death_effect)
#             group = self.groups()[0]
#             group.add(effect)
#             group.move_to_front(effect)
#             effect.set_pos(self.pos)
#             effect.play()
#         super().die()
