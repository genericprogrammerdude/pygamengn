import pygame


class BlitSurface:
    """Specification for a surface that will be blitted while rendering."""

    def __init__(self, surface: pygame.Surface, topleft: pygame.Vector2, special_flags: int = 0):
        """topleft is in screen coordinates."""
        self.surface = surface
        self.topleft = topleft
        self.special_flags = special_flags
