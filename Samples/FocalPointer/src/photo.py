import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.transform import Transform
from pygamengn.updatable import Updatable


@ClassRegistrar.register("Photo")
class Photo(GameObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Place the photo in the center and fit it to the window
        screen_rect = pygame.display.get_surface().get_rect()
        screen_size = screen_rect.size
        self.position = screen_rect.center
        scale_width = screen_size[0] / self.rect.width
        scale_height = screen_size[1] / self.rect.height
        if scale_width < scale_height:
            self.set_scale(scale_width)
        else:
            self.set_scale(scale_height)

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
