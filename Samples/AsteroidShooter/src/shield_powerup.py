from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.game_object_factory import TypeSpec
from pygamengn.powerup import Powerup


@ClassRegistrar.register("ShieldPowerup")
class ShieldPowerup(Powerup):

    def __init__(self, shield_type: TypeSpec, **kwargs):
        super().__init__(**kwargs)
        self.__shield_type = shield_type

    def gimme_stuff(self, gob: GameObject):
        try:
            shield = gob.shield
            if shield.alive():
                shield.take_damage(-100, None)
            else:
                shield = self.__shield_type.create()
                gob.shield = shield

            self.kill()
        except AttributeError:
            pass
