import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.UI.panel import Panel



@ClassRegistrar.register("TexturePanel")
class TexturePanel(Panel):
    """
    Basic UI panel that shows an image.

    TODO: Setting an angle different than 0 rotates the TexturePanel's blit surface, but it doesn't correct the
          component's rectangle or its children's. The feature only works if both these conditions are true:

            1. The component has no children.
            2. The component's rectangle is only used internally by itself. Mouse interactions rely on the component's
               rectangle accurately representing its shape and orientation; those will behave badly.
    """

    def __init__(
        self,
        image_asset,
        scale_texture_to_rect = True,
        angle = 0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._image_asset = image_asset
        self._scale_texture_to_rect = scale_texture_to_rect
        self._angle = angle
        self._angle_changed = True


    def _draw_surface(self):
        super()._draw_surface()
        if self._scale_texture_to_rect:
            # Fit the texture to the Component's rect, keeping original texture aspect ratio if required
            image_asset_rect = self._image_asset.surface.get_rect()
            self._surface = pygame.transform.rotozoom(
                self._image_asset.surface,
                self._angle,
                min(
                    self.rect.width / image_asset_rect.width,
                    self.rect.height / image_asset_rect.height
                )
            )
        else:
            self._surface = pygame.transform.rotate(self._image_asset.surface, self._angle)


    def _adjust_rect(self):
        self._draw_surface()
        surface_rect = self._surface.get_rect()
        self._rect.update(self._rect.topleft, (surface_rect.width, surface_rect.height))
        self._align()
        self._reset_redraw_flags()


    @property
    def angle(self) -> float:
        return self._angle


    @angle.setter
    def angle(self, theta: float):
        if theta != self._angle:
            self._angle = theta
            self._angle_changed = True


    @property
    def _needs_redraw(self) -> bool:
        """Spinner redraws its surface on every frame."""
        return super()._needs_redraw or self._angle_changed


    def _reset_redraw_flags(self):
        super()._reset_redraw_flags()
        self._angle_changed = False
