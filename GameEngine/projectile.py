import pygame

from animated_texture import AnimatedTexture
from game_object import GameObject
from game_object_factory import GameObjectFactory
from mover import MoverVelocity


@GameObjectFactory.register("Projectile")
class Projectile(GameObject):

    def __init__(self, image, enemies=None, damage=10, death_effect=None, velocity=0):
        super().__init__(image)
        self.mover = MoverVelocity(1.0, velocity)
        self.enemies = enemies
        self.damage = damage
        self.death_effect = death_effect

    def kill_when_off_screen(self):
        """This can be used by the Sprite Group to know if the object should be killed when it goes off screen."""
        return True

    def update(self, delta):
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        super().update(delta)
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

    def sprites_collided(self, a, b):
        """Checks whether sprites a and b collide."""
        if a == b:
            return False
        if not (a.is_collidable and b.is_collidable):
            return False
        if (a.parent and a.parent == b) or (b.parent and b.parent == a):
            return False
        return pygame.sprite.collide_rect(a, b)

    def die(self):
        """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
        if self.death_effect and self.alive():
            effect = GameObjectFactory.create(self.death_effect)
            group = self.groups()[0]
            group.add(effect)
            group.move_to_front(effect)
            effect.set_pos(self.pos)
            effect.play()
        super().die()

    def set_velocity(self, velocity):
        self.mover.set_velocity(velocity)
