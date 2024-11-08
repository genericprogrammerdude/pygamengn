import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.interpolator import Interpolator
from pygamengn.updatable import Updatable

from photo import Photo, State



@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(Updatable):
    """Spawns photos in the right order."""

    def __init__(self, photos, durations):
        self.photos = photos
        self.durations = durations
        self.total_time = 0
        self.photo_index = -1
        self.done = False
        self.photo = None
        self.year_panel = None
        self.interpolator = None
        self.skip_indices = [
            111,    # Small resolution (requires scale 2.2) and not a great photo
        ]

    def update(self, delta):
        self.year_panel.set_position(pygame.Vector2(self.interpolator.get(self.total_time), self.year_panel.pos.y))
        self.total_time += delta

    def set_year_panel(self, year_panel):
        self.year_panel = year_panel
        self.interpolator = Interpolator(
            duration = (
                (self.durations["on_display"] + self.durations["flying_in"]) * len(self.photos) +
                self.durations["flying_out"]
            ),
            from_value = 0,
            to_value = 1.0 - self.year_panel.size[1]
        )

    def move_to_next_photo(self):
        self.photo_index += 1
        while self.photo_index in self.skip_indices:
            self.photo_index += 1
        self.__show_new_photo()

        # If we're out of photos, the Slideshow game will end when the last photo is off the screen
        self.done = self.photo_index >= len(self.photos)
        if self.done:
            self.year_panel.fade_out(1500)

    def move_to_prev_photo(self):
        self.photo_index -= 1
        while self.photo_index in self.skip_indices:
            self.photo_index -= 1
        self.__show_new_photo()

    def __show_new_photo(self):
        if self.photo_index < len(self.photos) and self.photo_index >= 0:
            if self.photo and self.photo.state != State.FLYING_OUT:
                self.photo.state_transition(State.FLYING_OUT)
            self.photo = self.photos[self.photo_index]
            self.photo.start_moving(self.durations, self.move_to_next_photo)
            self.photo.transform()
            self.year_panel.year_text.set_text(self.photo.date[:4])


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
