import pygame


def blitRotate(image, pos, originPos, angle):
    """
    Rotates the given image and returns a (new_origin, rotated_image) tuple.
    """
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    return (origin, rotated_image)


class GameObject(pygame.sprite.Sprite):
    """Basic game object."""

    game_objects = pygame.sprite.Group()

    def __init__(self, image_fname):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = pygame.image.load(image_fname)
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()
        self.scale = 1.0
        self.angle = 0.0
        self.pos = pygame.math.Vector2(0.0, 0.0)
        self.velocity = 0.0

        # Add to group of game objects
        GameObject.game_objects.add(self)

    def update(self, delta):
        """Updates the game object. Delta time is in ms."""

        # Scale
#         self.rect = self.image.get_rect()
#         self.image = pygame.transform.scale(self.image_original,
#                                             (round(self.scale * self.rect.width), round(self.scale * self.rect.height)))
#         self.rect = self.image.get_rect()

        # Rotate
        pivot = pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)
        (new_pos, self.image) = blitRotate(self.image_original, (0, 0), pivot, self.angle)

        # Translate
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos - pygame.math.Vector2(self.rect.width / 2.0, self.rect.height / 2.0)

    def set_velocity(self, velocity):
        """Sets the game object's velocity."""
        self.velocity = velocity

    def set_scale(self, scale):
        """Sets the scale of the sprite."""
        self.scale = scale

    def set_pos(self, pos):
        """Sets the position of the sprite in the screen so that the sprite's center is at pos."""
        self.pos = pos

    def set_angle(self, angle):
        """Sets the orientation of the game object."""
        self.angle = angle
