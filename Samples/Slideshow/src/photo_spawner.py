import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.interpolator import Interpolator
from pygamengn.updatable import Updatable
from pygamengn.game_object_base import GameObjectBase

from photo import Photo, State
from inventory import image_index_start



@ClassRegistrar.register("PhotoSpawner")
class PhotoSpawner(GameObjectBase):
    """Spawns photos in the right order."""

    def __init__(self, photos, durations):
        self.photos = photos
        self.durations = durations
        self.total_time = 0
        self.photo_index = -1
        self.__show_info_ui = False
        self.done = False
        self.photo = None
        self.slideshow_ui = None
        self.info_ui = None
        self.interpolator = None
        self.skip_indices = [
            111,
            146,
        ]

    def update(self, delta):
        self.slideshow_ui.year_panel.normalized_pos = pygame.Vector2(
            self.interpolator.get(self.total_time),
            self.slideshow_ui.year_panel.normalized_pos.y
        )
        self.total_time += delta
        if self.photo_index >= len(self.photos) or self.photo_index < 0:
            self.done = self.photo.state == State.INACTIVE
        if self.__show_info_ui:
            self.info_ui.photo_scale_text.text = f"Scale: {self.photo.scale:.2f}/{self.photo.display_max_scale:.2f}"

    def set_slideshow_ui(self, slideshow_ui):
        self.slideshow_ui = slideshow_ui
        self.interpolator = Interpolator(
            duration = (
                (self.durations["on_display"] + self.durations["flying_in"]) * len(self.photos) +
                self.durations["flying_out"]
            ),
            from_value = 0,
            to_value = 1.0 - self.slideshow_ui.year_panel.normalized_size.x
        )

    def set_info_ui(self, info_ui):
        self.info_ui = info_ui

    def move_to_next_photo(self):
        self.photo_index += 1
        while self.photo_index + image_index_start in self.skip_indices:
            self.photo_index += 1
        self.__show_new_photo()

        # If we're out of photos, the Slideshow game will end when the last photo is off the screen
        if self.photo_index >= len(self.photos):
            self.slideshow_ui.fade_out(1500)

    def move_to_prev_photo(self):
        self.photo_index -= 1
        while self.photo_index + image_index_start in self.skip_indices:
            self.photo_index -= 1
        self.__show_new_photo()

    def __show_new_photo(self):
        if self.photo_index < len(self.photos) and self.photo_index >= 0:
            if self.photo and self.photo.state != State.FLYING_OUT:
                self.photo.state_transition(State.FLYING_OUT)
            self.photo = self.photos[self.photo_index]
            self.photo.start_moving(self.durations, self.move_to_next_photo)
            self.photo.transform()
            self.slideshow_ui.year_text.text = self.photo.date[:4]
            if self.__show_info_ui:
                self.__set_info_ui_data()
            self.total_time = self.photo_index * (self.durations["on_display"] + self.durations["flying_in"])

    @property
    def show_info_ui(self) -> bool:
        return self.__show_info_ui

    @show_info_ui.setter
    def show_info_ui(self, show: bool):
        self.__show_info_ui = show
        if show:
            self.__set_info_ui_data()

    def __set_info_ui_data(self):
        self.info_ui.photo_name_text.text = f"Name: Photo_{self.photo_index + image_index_start:03}"
        self.info_ui.photo_date_text.text = f"Date: {self.photo.date}"
        self.info_ui.photo_focal_point_text.text = (
            f"Focal point: ({self.photo.focal_point.x:.2f}, {self.photo.focal_point.y:.2f})"
        )
        self.info_ui.photo_scale_text.text = f"Scale: {self.photo.scale:.2f}"
