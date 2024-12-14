from abc import abstractmethod
import random

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.trigger import Trigger


@ClassRegistrar.register("Powerup")
class Powerup(Trigger):

    def __init__(self, distance, angular_velocity, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance
        self.angular_velocity = angular_velocity * random.choice([-1, 1]) * (random.random() + 0.5)
        self.set_enter_callback(self.gimme_stuff)

    def update(self, delta):
        heading = self.heading + delta * self.angular_velocity / 1000.0
        self.heading = heading
        super().update(delta)

    @abstractmethod
    def gimme_stuff(self, gob: GameObject):
        pass


@ClassRegistrar.register("HealthPowerup")
class HealthPowerup(Powerup):

    def gimme_stuff(self, gob: GameObject):
        gob.take_damage(-100, None)
        self.kill()
