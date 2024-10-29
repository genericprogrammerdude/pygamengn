import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.transform import Transform
from pygamengn.updatable import Updatable


@ClassRegistrar.register("Photo")
class Photo(GameObject):

    def __init__(self, mover, date, focal_point, ttl, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.date = date
        self.focal_point = focal_point
        self.ttl = ttl
        self.max_scale = 1.0
        self.min_scale = 0.1
        self.moving_time = 0
        self.easing_in = True
        self.revolutions = numpy.random.choice([-4, -3, -2, -1, 1, 2, 3, 4])

        # Get maximum scale so that the photo fits the screen
        screen_size = pygame.display.get_surface().get_rect().size
        scale_width = screen_size[0] / self.rect.width
        scale_height = screen_size[1] / self.rect.height
        if scale_width < scale_height:
            self.max_scale = scale_width
            self.min_scale = scale_width / 4.0
        else:
            self.max_scale = scale_height
            self.min_scale = scale_height / 4.0
        self.set_scale(self.min_scale)

    def update(self, delta):
        super().update(delta)

        if self.visible:
            self.position = self.mover.move(delta)
            if self.mover.is_arrived():
                # Exit the screen gracefully
                screen_rect = pygame.display.get_surface().get_rect()
                dest = pygame.Vector2(screen_rect.width, numpy.random.randint(0, screen_rect.height))
                self.mover.set_ori_dest(self.position, dest)

                if not self.easing_in:
                    # I should've exited the screen -> make sure I'm off the screen so I get deleted
                    screen_rect = pygame.display.get_surface().get_rect()
                    self.position.x = screen_rect.width * 4

                self.easing_in = False

            theta = self.moving_time * numpy.pi / self.ttl
            factor = (1.0 - numpy.cos(theta)) / 2.0
            self.set_alpha(factor)
            self.set_scale(self.min_scale + factor * (self.max_scale - self.min_scale))

            theta = self.moving_time * (numpy.pi / 2.0) / self.ttl
            factor = numpy.sin(theta)
            self.heading = 360.0 * self.revolutions * factor

            self.moving_time += delta

    def start_moving(self):
        self.visible = True
        self.transform()


@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(Updatable):
    """Spawns photos in the right order."""

    def __init__(self, images, spawn_freq, photo_time, render_group, photos):
        self.images = images
        self.spawn_freq = spawn_freq
        self.photo_time = photo_time
        self.time_to_next_spawn = 1
        self.render_group = render_group
        self.total_time = 0
        self.photo_index = 0
        self.done = False
        self.photos = photos
        self.skip_indices = [
            111,    # Small resolution (requires scale 2.2) and not a great photo
        ]

        screen_size = pygame.display.get_surface().get_rect().size
        photo_index = 0

    def update(self, delta):
        self.total_time += delta
        self.time_to_next_spawn -= delta

        if self.time_to_next_spawn <= 0 and self.photo_index < len(self.photos):
            self.time_to_next_spawn = self.spawn_freq

            # Activate new photo
            photo = self.photos[self.photo_index]
            screen_rect = pygame.display.get_surface().get_rect()
            pos = pygame.Vector2(-photo.rect.width / 2.0 + 1, numpy.random.randint(0, screen_rect.height))
            photo.mover.set_ori_dest(pos, screen_rect.center)
            photo.position = pos
            photo.start_moving()

            # Increment photo index
            self.photo_index += 1
            while self.photo_index in self.skip_indices:
                self.photo_index += 1

            # If we're out of photos, the Slideshow game will end when the last photo is off the screen
            self.done = self.photo_index >= len(self.images)

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
