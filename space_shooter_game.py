from game import BlitSurface
from game import Game
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("SpaceShooterGame")
class SpaceShooterGame(Game):

    def __init__(self, font, text_colour, **kwargs):
        super().__init__(**kwargs)
        self.font = font
        self.text_colour = text_colour
        self.time = 0
        self.score = 0
        self.player = None

        # Assign biggest rectangle for time and score text
        s = "00:00"
        surface = self.font.font.render(s, True, self.text_colour)
        self.time_text_width = surface.get_rect().width
        s = "0000"
        surface = self.font.font.render(s, True, self.text_colour)
        self.score_text_width = surface.get_rect().width

    def update(self, delta):
        # Track round time and score
        if not self.player is None and self.player.alive() and not self.is_paused:
            self.time += delta
            self.score = self.player.score

        # Put time and score text together
        time_surface = self.build_time_text_surface()
        score_surface = self.build_score_text_surface()
        self.add_blit_surface(BlitSurface(time_surface, (self.screen.get_rect().width - self.time_text_width, 0)))
        self.add_blit_surface(BlitSurface(score_surface, (self.score_text_width - score_surface.get_rect().width, 0)))

        super().update(delta)

    def build_time_text_surface(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        surface = self.font.font.render("{:02d}:{:02d}".format(min, sec), True, self.text_colour)
        return surface

    def build_score_text_surface(self):
        surface = self.font.font.render("{:03d}".format(self.score), True, self.text_colour)
        return surface
