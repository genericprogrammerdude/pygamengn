from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject


@ClassRegistrar.register("Shield")
class Shield(GameObject):

    def __init__(self, images, damage):
        super().__init__(images[0])
        self.images = images
        self.image_index = 0
        self.damage = damage

    def take_damage(self, damage, instigator):
        super().take_damage(damage, instigator)

        # Change shield image if necessary
        n = len(self.images)
        d = 100.0 / n
        index = n - int(self.health / d) - 1
        if index < 0:
            index = 0
        if index != self.image_index:
            self.image_index = index
            self.set_image(self.images[index])
