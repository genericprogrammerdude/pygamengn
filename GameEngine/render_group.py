import math
import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("RenderGroup")
class RenderGroup(pygame.sprite.LayeredUpdates, GameObjectBase):

    def __init__(
            self,
            world_rect=pygame.Rect(0, 0, 0, 0),
            grid_draw=False,
            grid_color=(100, 100, 100),
            grid_interval=100,
            background=None
        ):
        super().__init__()
        self.target = None
        self.cam = pygame.Vector2(0, 0)
        self.world_rect = world_rect
        self.view_rect = pygame.Rect(0, 0, 0, 0)
        self.grid_draw = grid_draw
        self.grid_color = grid_color
        self.grid_interval = grid_interval
        self.background = background

    def set_target(self, target):
        """Sets the game object to follow."""
        self.target = target
        if self.target:
            self.add(target)

    def update(self, view_size, *args):
        """Updates itself and its sprites."""
        super().update(*args)
        self.view_rect = view_size

        if self.target:
            # Keep the view_rect centered with the target's rect center
            x = -self.target.rect.center[0] + self.view_rect.width / 2.0
            y = -self.target.rect.center[1] + self.view_rect.height / 2.0
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            if self.world_rect.width > 0 and self.world_rect.height > 0:
                # Keep the camera within the world_rect if one was given
                self.cam.x = max(-(self.world_rect.width - self.view_rect.width), min(0, self.cam.x))
                self.cam.y = max(-(self.world_rect.height - self.view_rect.height), min(0, self.cam.y))

    def draw(self, surface):
        """Draws the sprites in the group on the given surface."""
        self.__draw_background(surface)
        if self.grid_draw:
            self.__draw_grid(surface)

        for sprite in self.sprites():
            if sprite.visible:
                transformed_rect = sprite.rect.move(self.cam)
                if not self.view_rect.colliderect(transformed_rect):
                    # Ignore sprites that are outside of the view rectangle
                    if sprite.kill_when_off_screen:
                        self.kill_sprite(sprite)
                else:
                    surface.blit(sprite.image, transformed_rect)

    def __draw_background(self, surface):
        """Tiles the background image across the screen."""
        rect = self.background.get_rect()
        cam_x = round(-self.cam.x)
        cam_y = round(-self.cam.y)
        range_x = range((cam_x // rect.width) * rect.width, cam_x + self.view_rect.width, rect.width)
        range_y = range((cam_y // rect.height) * rect.height, cam_y + self.view_rect.height, rect.height)
        for y in range_y:
            for x in range_x:
                rect.x = x - cam_x
                rect.y = y - cam_y
                surface.blit(self.background, rect)

    def __draw_grid(self, surface):
        """Draws a grid as a background."""
        low_x = int(math.floor(self.cam.x / self.grid_interval)) * self.grid_interval
        hi_x = int(math.ceil(self.cam.x + self.view_rect.width))
        for x in range(int(low_x - self.cam.x), int(hi_x - self.cam.x), self.grid_interval):
            xcor = self.view_rect.width - x
            pygame.draw.line(surface, self.grid_color, (xcor, 0), (xcor, self.view_rect.height))

        low_y = int(math.floor(self.cam.y / self.grid_interval)) * self.grid_interval
        hi_y = int(math.ceil(self.cam.y + self.view_rect.height))
        for y in range(int(low_y - self.cam.y), int(hi_y - self.cam.y), self.grid_interval):
            ycor = self.view_rect.height - y
            pygame.draw.line(surface, self.grid_color, (0, ycor), (self.view_rect.width, ycor))

    def get_world_view_rect(self):
        rv = pygame.Rect(self.view_rect)
        rv.topleft -= self.cam
        return rv

    def kill_sprite(self, sprite):
        """Recursively kills the given sprite and all its attachments."""
        for attachment in sprite.attachments:
            self.kill_sprite(attachment.game_object)
        sprite.attachments.clear()
        sprite.kill()
