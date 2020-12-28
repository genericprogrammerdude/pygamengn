import pygame

from ship import Ship


class Projectile(Ship):

    def __init__(self, image, explosion_atlas=None, velocity_decay_factor=1.0, enemies=None):
        super().__init__(image, explosion_atlas, velocity_decay_factor)
        self.enemies = enemies

    def kill_when_off_screen(self):
        """This can be used by the Sprite Group to know if the object should be killed when it goes off screen."""
        return True

    def update(self, delta):
        super().update(delta)
        self.handle_collisions()

    def handle_collisions(self):
        """Checks for collisions."""
        if self.enemies:
            collisions = pygame.sprite.spritecollide(self, self.enemies, False, self.sprites_collided)
            for sprite in collisions:
                collision = pygame.sprite.collide_mask(sprite, self)
                if collision:
                    collision_handler = sprite.parent if sprite.parent else sprite
                    collision_handler.collide(pygame.Vector2(sprite.rect.topleft) + collision)
                    self.kill()

    def sprites_collided(self, a, b):
        """Checks whether sprites a and b collide."""
        if a == b:
            return False
        if not (a.is_collidable and b.is_collidable):
            return False
        if (a.parent and a.parent == b) or (b.parent and b.parent == a):
            return False
        return pygame.sprite.collide_rect(a, b)
