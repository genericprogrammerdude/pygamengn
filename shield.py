from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Shield")
class Shield(GameObject):

    def __init__(self, images, damage):
        super().__init__(images[0])
        self.images = images
        self.image_index = 0
        self.damage = damage

    def take_damage(self, damage):
        super().take_damage(damage)

        # Change shield image if necessary
        n = len(self.images)
        d = 100.0 / n
        index = n - int(self.health / d) - 1
        if index < 0:
            index = 0
        if index != self.image_index:
            self.image_index = index
            self.set_image(self.images[index])

    def handle_collision(self, gob, *_):
        """Reacts to collision against game object gob."""
        # Apply damage to the collided sprite
        gob.take_damage(self.damage)
