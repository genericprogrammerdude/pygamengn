import pygame


class GameObject(pygame.sprite.Sprite):
    """Basic game object."""

    game_objects = pygame.sprite.Group()

    def __init__(self, image_fname):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = pygame.image.load(image_fname)
        self.rect = self.image.get_rect()

        # Add to group of game objects
        GameObject.game_objects.add(self)
