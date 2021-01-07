import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory
import geometry
from transform import Transform


@GameObjectFactory.register("GameObject")
class GameObject(pygame.sprite.Sprite, GameObjectBase):
    """Basic game object."""

    def __init__(self, image, is_collidable=True, scale=1.0, alpha=1.0, visible=True, heading=0):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = image
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()
        self.scale = scale
        self.heading = heading
        self.pos = pygame.math.Vector2(0.0, 0.0)
        self.dirty_image = True
        self.is_collidable = is_collidable
        self.mask = None  # The mask will be built on the first transform()
        self.parent = None
        self.health = 100
        self.attachments = []
        self.alpha = alpha
        self.visible = visible

    def update(self, delta):
        """Updates the game object. Delta time is in ms."""
        super().update()
        self.transform()
        for attachment in self.attachments:
            if attachment.parent_transform:
                t = Transform(self.pos, self.heading)

                attachment_pos = t.apply(attachment.offset)
                attachment.game_object.set_pos(attachment_pos)
                attachment.game_object.set_heading(self.heading)

    def transform(self):
        """Transforms the object based on current heading, scale, and position."""
        # Rotate and scale if necessary
        if self.dirty_image:
            self.image = pygame.transform.rotozoom(self.image_original, self.heading, self.scale)
            if self.alpha != 1.0:
                self.image.set_alpha(self.alpha * 255)
            self.rect = self.image.get_rect()
            if self.is_collidable:
                self.mask = pygame.mask.from_surface(self.image, 16)
            self.dirty_image = False

        # Translate
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

    def set_scale(self, scale):
        """Sets the scale of the sprite."""
        self.dirty_image = self.dirty_image or self.scale != scale
        self.scale = scale

    def set_pos(self, pos):
        """Sets the position of the sprite in the screen so that the sprite's center is at pos."""
        self.pos = pos

    def set_heading(self, heading):
        """Sets the orientation of the game object."""
        self.dirty_image = self.dirty_image or self.heading != heading
        self.heading = geometry.normalize_angle(heading)

    def set_image(self, image):
        """Sets a new image for the game object."""
        self.image = image
        self.image_original = self.image.copy()
        self.dirty_image = True

    def kill_when_off_screen(self):
        """This can be used by the Sprite Group to know if the object should be killed when it goes off screen."""
        return False

    def attach(self, game_object, offset, take_parent_transform):
        """Attaches a game object to this game object at the give offset."""
        self.attachments.append(Attachment(game_object, offset, take_parent_transform))
        game_object.parent = self

    def take_damage(self, damage):
        """Takes damage for this game object."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            for attachment in self.attachments:
                attachment.game_object.take_damage(attachment.game_object.health)
            self.die()

    def die(self):
        self.kill()

    def add_to_groups(self, groups):
        """Adds the game object to the given sprite groups."""
        self.add(groups)

    def set_layer_id(self, layer_id):
        """Sets the layer for rendering."""
        self._layer = layer_id

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        pass


class Attachment():

    def __init__(self, game_object, offset, parent_transform):
        self.game_object = game_object
        self.offset = offset
        self.parent_transform = parent_transform
