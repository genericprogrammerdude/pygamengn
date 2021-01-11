import pygame

from animated_texture import AnimatedTexture
from game_object import GameObject
from game_object_factory import GameObjectFactory
from mover import MoverVelocity


@GameObjectFactory.register("Projectile")
class Projectile(GameObject):

    def __init__(self, image, damage, death_effect, mover, **kwargs):
        super().__init__(image, **kwargs)
        self.mover = mover
        self.damage = damage
        self.death_effect = death_effect

    def kill_when_off_screen(self):
        """This can be used by the Sprite Group to know if the object should be killed when it goes off screen."""
        return True

    def update(self, delta):
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        super().update(delta)

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        # Set own position to the collision point so the explosion will play there when self dies
        self.set_pos(world_pos)
        instigator = GameObject.get_root_parent(gob)
        self.take_damage(self.health, instigator)
        # Apply damage to the collided sprite
        super().handle_collision(gob, world_pos)
