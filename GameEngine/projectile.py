import pygame

from animated_texture import AnimatedTexture
from game_object import GameObject
from game_object_factory import GameObjectFactory
from mover import MoverVelocity


@GameObjectFactory.register("Projectile")
class Projectile(GameObject):

    def __init__(self, image, damage, death_effect, mover):
        super().__init__(image)
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
        self.take_damage(self.health)
        # Apply damage to the collided sprite
        gob.take_damage(self.damage)

    def die(self):
        """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
        if self.death_effect and self.alive():
            effect = GameObjectFactory.create(self.death_effect)
            group = self.groups()[0]
            group.add(effect)
            effect.set_pos(self.pos)
            effect.play()
        super().die()
