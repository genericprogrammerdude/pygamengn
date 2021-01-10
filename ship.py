from asteroid import Asteroid
from game_object import GameObject
from game_object_factory import GameObjectFactory
from health_bar import HealthBar
from mover import MoverVelocity
from projectile import Projectile


@GameObjectFactory.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image, projectile_type, fire_freq, mover, death_effect, damage, **kwargs):
        super().__init__(image, **kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq
        self.death_effect = death_effect
        self.damage = damage

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)
        self.time_since_last_fire += delta

    def set_velocity(self, velocity):
        """Sets the ship's velocity."""
        self.mover.set_velocity(velocity)

    def fire(self):
        """Fires a Projectile at the target."""
        if self.time_since_last_fire > self.fire_freq and self.alive():
            projectile = GameObjectFactory.create(self.projectile_type)
            projectile.set_pos(self.pos)
            projectile.set_heading(self.heading)
            projectile.transform()

            group = self.groups()[0]
            group.add(projectile)

            self.time_since_last_fire = 0

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        # Apply damage to the collided sprite
        gob.take_damage(self.damage)

    def die(self):
        """Die."""
        if self.alive() and self.death_effect:
            effect = GameObjectFactory.create(self.death_effect)
            effect.set_pos(self.pos)
            effect.play()

        super().die()
