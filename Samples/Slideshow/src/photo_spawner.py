import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.interpolator import Interpolator
from pygamengn.updatable import Updatable

from photo import Photo, State
from inventory import image_index_start



@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(Updatable):
    """Spawns photos in the right order."""

    def __init__(self, photos, durations):
        self.photos = photos
        self.durations = durations
        self.total_time = 0
        self.photo_index = -1
        self.__show_info_panel = True
        self.done = False
        self.photo = None
        self.year_panel = None
        self.bar_panel = None
        self.info_panel = None
        self.interpolator = None
        self.skip_indices = []

    def update(self, delta):
        self.year_panel.set_position(pygame.Vector2(self.interpolator.get(self.total_time), self.year_panel.pos.y))
        self.total_time += delta
        if self.photo_index >= len(self.photos) or self.photo_index < 0:
            self.done = self.photo.state == State.INACTIVE
        if self.__show_info_panel:
            self.info_panel.photo_scale_text.set_text(f"Scale: {self.photo.scale:.2f}/{self.photo.display_max_scale:.2f}")

    def set_year_panel(self, year_panel, bar_panel):
        self.year_panel = year_panel
        self.bar_panel = bar_panel
        self.interpolator = Interpolator(
            duration = (
                (self.durations["on_display"] + self.durations["flying_in"]) * len(self.photos) +
                self.durations["flying_out"]
            ),
            from_value = 0,
            to_value = 1.0 - self.year_panel.size[0]
        )

    def set_info_panel(self, info_panel):
        self.info_panel = info_panel

    def move_to_next_photo(self):
        self.photo_index += 1
        while self.photo_index in self.skip_indices:
            self.photo_index += 1
        self.__show_new_photo()

        # If we're out of photos, the Slideshow game will end when the last photo is off the screen
        if self.photo_index >= len(self.photos):
            self.year_panel.fade_out(1500)
            self.bar_panel.fade_out(1500)

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
            if self.__show_info_panel:
                self.__set_info_panel_data()
            self.total_time = self.photo_index * (self.durations["on_display"] + self.durations["flying_in"])

    @property
    def show_info_panel(self) -> bool:
        return self.__show_info_panel

    @show_info_panel.setter
    def show_info_panel(self, show: bool):
        self.__show_info_panel = show
        if show:
            self.__set_info_panel_data()

    def __set_info_panel_data(self):
        self.info_panel.photo_name_text.set_text(f"Name: Photo_{self.photo_index + image_index_start:03}")
        self.info_panel.photo_date_text.set_text(f"Date: {self.photo.date}")
        self.info_panel.photo_focal_point_text.set_text(
            f"Focal point: ({self.photo.focal_point.x:.2f}, {self.photo.focal_point.y:.2f})"
        )
        self.info_panel.photo_scale_text.set_text(f"Scale: {self.photo.scale:.2f}")

    def set_player(self, player):
        pass
