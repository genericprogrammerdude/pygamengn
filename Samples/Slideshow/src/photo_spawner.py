import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.updatable import Updatable

from photo import Photo



@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(Updatable):
    """Spawns photos in the right order."""

    def __init__(self, spawn_freq, photo_time, photos):
        self.spawn_freq = spawn_freq
        self.photo_time = photo_time
        self.photos = photos
        self.time_to_next_spawn = 1
        self.total_time = 0
        self.photo_index = 0
        self.done = False
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
            photo.start_moving(self.photo_time)
            photo.transform()

            # Increment photo index
            self.photo_index += 1
            while self.photo_index in self.skip_indices:
                self.photo_index += 1

            # If we're out of photos, the Slideshow game will end when the last photo is off the screen
            self.done = self.photo_index >= len(self.photos)

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
