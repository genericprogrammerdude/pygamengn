import pygame

from animated_texture import AnimatedTexture
from class_registrar import ClassRegistrar
from game_object import GameObject
from mover import MoverVelocity


@ClassRegistrar.register("Projectile")
class Projectile(GameObject):

    def __init__(self, mover, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover

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
