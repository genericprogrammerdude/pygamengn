import math
import pygame


class CameraAwareGroup(pygame.sprite.LayeredUpdates):

    def __init__(self, target, world_rect, view_rect, grid_draw=False, grid_color=(100, 100, 100), grid_interval=100):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_rect = world_rect
        self.view_rect = view_rect
        self.grid_draw = grid_draw
        self.grid_color = grid_color
        self.grid_interval = grid_interval
        if self.target:
            self.add(target)

    def update(self, *args):
        """Updates itself and its sprites."""
        super().update(*args)
        self.handle_collisions()

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
        if self.grid_draw:
            self.__draw_grid(surface)

        for sprite in self.sprites():
            cam = pygame.Vector2(round(self.cam.x), round(self.cam.y))
            transformed_rect = sprite.rect.move(cam)
            if not self.view_rect.colliderect(transformed_rect):
                # Ignore sprites that are outside of the view rectangle
                if sprite.kill_when_off_screen():
                    sprite.kill()
            else:
                surface.blit(sprite.image, transformed_rect)

    def handle_collisions(self):
        """Checks for collisions."""
        if self.target:
            collisions = pygame.sprite.spritecollide(self.target, self, False, self.sprites_collided)
            for sprite in collisions:
                collision = pygame.sprite.collide_mask(self.target, sprite)
                if collision:
                    self.target.collide(pygame.Vector2(self.target.rect.topleft) + collision)
                    sprite.kill()

    def sprites_collided(self, a, b):
        """Checks whether sprites a and b should have collision detection run between the two."""
        if a == b:
            return False
        if not (a.is_collidable and b.is_collidable):
            return False
        return True

    def __draw_grid(self, surface):
        """Draws a grid as a background."""
        low_x = int(math.floor(self.cam.x / self.grid_interval)) * 100
        hi_x = int(math.ceil(self.cam.x + self.view_rect.width))
        for x in range(int(low_x - self.cam.x), int(hi_x - self.cam.x), self.grid_interval):
            xcor = self.view_rect.width - x
            pygame.draw.line(surface, self.grid_color, (xcor, 0), (xcor, self.view_rect.height))

        low_y = int(math.floor(self.cam.y / self.grid_interval)) * 100
        hi_y = int(math.ceil(self.cam.y + self.view_rect.height))
        for y in range(int(low_y - self.cam.y), int(hi_y - self.cam.y), self.grid_interval):
            ycor = self.view_rect.height - y
            pygame.draw.line(surface, self.grid_color, (0, ycor), (self.view_rect.width, ycor))
