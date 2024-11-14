import pygame


class BlitSurface:
    """Specification for a surface that will be blitted while rendering."""

    def __init__(self, surface: pygame.Surface, topleft: tuple[int]):
        """topleft is in screen coordinates."""
        self.surface = surface
        self.topleft = topleft