import pygame


class GameObject(pygame.sprite.Sprite):
    """Basic game object."""

    def __init__(self, image_fname):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = pygame.image.load(image_fname).convert()
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()
        self.scale = 1.0
        self.angle = 0.0
        self.pos = pygame.math.Vector2(0.0, 0.0)

    def update(self, delta):
        """Updates the game object. Delta time is in ms."""

        super().update()

        # Rotate and scale
        self.image = pygame.transform.rotozoom(self.image_original, self.angle, self.scale)
        self.rect = self.image.get_rect()

        # Translate
        topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        self.rect.topleft = pygame.Vector2(round(topleft.x), round(topleft.y))

    def set_scale(self, scale):
        """Sets the scale of the sprite."""
        self.scale = scale

    def set_pos(self, pos):
        """Sets the position of the sprite in the screen so that the sprite's center is at pos."""
        self.pos = pos

    def set_angle(self, angle):
        """Sets the orientation of the game object."""
        self.angle = angle
