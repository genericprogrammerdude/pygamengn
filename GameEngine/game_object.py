import pygame


class GameObject(pygame.sprite.Sprite):
    """Basic game object."""

    def __init__(self, image_fname, is_collidable=True):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = pygame.image.load(image_fname).convert()
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()
        self.scale = 1.0
        self.heading = 0.0
        self.pos = pygame.math.Vector2(0.0, 0.0)
        self.dirty_image = True
        self.is_collidable = is_collidable
        self.mask = None  # The mask will be built on the first transform()

    def update(self, delta):
        """Updates the game object. Delta time is in ms."""
        super().update()
        self.transform()

    def transform(self):
        """Transforms the object based on current heading, scale, and position."""
        # Rotate and scale if necessary
        if self.dirty_image:
            self.image = pygame.transform.rotozoom(self.image_original, self.heading, self.scale)
            self.rect = self.image.get_rect()
            if self.is_collidable:
                self.mask = pygame.mask.from_surface(self.image)
            self.dirty_image = False

        # Translate
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

    def set_scale(self, scale):
        """Sets the scale of the sprite."""
        self.dirty_image = (self.scale != scale)
        self.scale = scale

    def set_pos(self, pos):
        """Sets the position of the sprite in the screen so that the sprite's center is at pos."""
        self.pos = pos

    def set_heading(self, heading):
        """Sets the orientation of the game object."""
        self.dirty_image = (self.heading != heading)
        self.heading = heading

    def kill_when_off_screen(self):
        """This can be used by the Sprite Group to know if the object should be killed when it goes off screen."""
        return False
