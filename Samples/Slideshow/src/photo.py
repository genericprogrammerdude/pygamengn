import random

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.transform import Transform
from pygamengn.updatable import Updatable


@ClassRegistrar.register("Photo")
class Photo(GameObject):

    def __init__(self, mover, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.max_scale = 1.0

        # Get maximum scale so that the photo fits the screen
        screen_size = pygame.display.get_surface().get_rect().size
        scale_width = screen_size[0] / self.rect.width
        scale_height = screen_size[1] / self.rect.height
        if scale_width < scale_height:
            self.max_scale = scale_width
        else:
            self.max_scale = scale_height
        self.set_scale(self.max_scale / 2.0)

    def update(self, delta):
        if self.visible:
            super().update(delta)
            self.position = self.position + self.mover.move(delta)


@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(Updatable):
    """Spawns photos in the right order."""

    def __init__(self, images, photo_type_spec, spawn_freq, render_group):
        self.images = images
        self.photo_type_spec = photo_type_spec
        self.spawn_freq = spawn_freq
        self.time_to_next_spawn = 1
        self.render_group = render_group
        self.total_time = 0
        self.photo_index = 0
        self.done = False
        self.skip_indices = [
            111,    # Small resolution (requires scale 2.2) and not a great photo
        ]

        screen_size = pygame.display.get_surface().get_rect().size
        self.photos = []
        photo_index = 0
        for image in self.images:
            photo = self.photo_type_spec.create(image_asset = image)
            if photo.max_scale > 1.0:
                print(f"*** Small photo! {photo.max_scale:.1f} {photo_index:03}")
            photo_index += 1
            self.photos.append(photo)

    def update(self, delta):
        self.total_time += delta
        self.time_to_next_spawn -= delta

        if self.time_to_next_spawn <= 0:
            self.time_to_next_spawn = self.spawn_freq

            # Activate new photo
            photo = self.photos[self.photo_index]
            photo.visible = True
            # photo = self.photo_type_spec.create(image_asset = self.images[self.photo_index])
            pos, direction = self.get_random_pos_dir(self.render_group.get_world_view_rect())
            photo.mover.set_direction(direction)
            photo.position = pos
            photo.transform()

            # Increment photo index
            self.photo_index += 1
            while self.photo_index in self.skip_indices:
                self.photo_index += 1

            # If we're out of photos, the Slideshow game will end when the last photo is off the screen
            self.done = self.photo_index >= len(self.images)

    def get_random_pos_dir(self, world_view_rect):
        # Aim roughly to the center of the screen
        dest = pygame.Vector2(world_view_rect.center)
        range_x = round(world_view_rect.width / 3)
        dest.x += random.randint(-range_x, range_x)
        range_y = round(world_view_rect.height / 3)
        dest.y += random.randint(-range_y, range_y)
        origin = self.get_random_point(world_view_rect)
        direction = (dest - origin).normalize()
        return origin, direction

    def get_random_point(self, world_view_rect):
        point = ()
        axis = random.randint(0, 1)
        if axis == 0:
            # Select random value along x axis and one of the two values of y for the top and bottom edges of the screen
            point = pygame.Vector2(
                random.randint(world_view_rect.topleft[0], world_view_rect.topright[0]),
                random.choice([world_view_rect.topleft[1], world_view_rect.bottomleft[1]])
            )
        else:
            # Select random value along y axis and one of the two values of x for the left and right edges of the screen
            point = pygame.Vector2(
                random.choice([world_view_rect.topleft[0], world_view_rect.topright[0]]),
                random.randint(world_view_rect.topleft[1], world_view_rect.bottomleft[1])
            )
        return point

# Small photos
# *** Small photo! 1.2 095
# *** Small photo! 1.0 098
# *** Small photo! 1.1 102
# *** Small photo! 2.2 111
# *** Small photo! 1.8 112
# *** Small photo! 1.2 118
# *** Small photo! 1.1 122
# *** Small photo! 1.4 134
# *** Small photo! 1.6 145
# *** Small photo! 1.0 168
# *** Small photo! 1.0 169
# *** Small photo! 1.4 177
# *** Small photo! 1.8 178
# *** Small photo! 1.8 179
# *** Small photo! 1.8 180
# *** Small photo! 1.8 181
# *** Small photo! 1.8 182
# *** Small photo! 1.8 183
# *** Small photo! 1.8 184
# *** Small photo! 1.8 185
# *** Small photo! 1.8 186
# *** Small photo! 1.8 187
# *** Small photo! 1.8 188
# *** Small photo! 1.3 189
# *** Small photo! 1.8 190
# *** Small photo! 1.4 191
# *** Small photo! 1.8 192
# *** Small photo! 1.4 193
# *** Small photo! 1.3 194
# *** Small photo! 1.4 195
# *** Small photo! 1.8 196
# *** Small photo! 1.4 197
# *** Small photo! 1.4 198
# *** Small photo! 1.7 199
# *** Small photo! 1.4 202
# *** Small photo! 1.5 203
# *** Small photo! 1.4 204
# *** Small photo! 1.0 216
# *** Small photo! 1.7 223
# *** Small photo! 1.5 226

    def set_player(self, player):
        pass
