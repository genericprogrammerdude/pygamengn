import random

import pygame

from game_object import GameObject
from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory
from render_group import RenderGroup
from transform import Transform
from turret import Turret
from updatable import Updatable


@GameObjectFactory.register("Asteroid")
class Asteroid(GameObject):

    def __init__(self, images, mover, health, death_spawn, score_on_die, **kwargs):
        super().__init__(image_asset=random.choice(images), **kwargs)
        self.mover = mover
        self.health = health
        self.death_spawn = death_spawn
        self.spin_delta_factor = random.choice([-1.0, 1.0])
        self.score_on_die = score_on_die

    def update(self, delta):
        spin_delta = (45.0 * delta) / 1000.0 * self.spin_delta_factor
        self.set_heading(self.heading + spin_delta)
        self.pos = self.pos + self.mover.move(delta)
        super().update(delta)
        for attachment in self.attachments:
            attachment.game_object.set_pos(self.pos)

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        # Apply damage to the collided sprite
        if isinstance(gob, Turret):
            # HACK ALERT!
            if gob.get_object_id() > self.get_object_id():
                # Ignore collision because the turret is drawn over the asteroid, so they shouldn't collide
                return
        super().handle_collision(gob, world_pos)

    def die(self, instigator):
        """Die. Plays an explosion if it was given an atlas for  the AnimatedTexture."""
        if self.alive():
            if self.death_spawn:
                angle = -30.0
                angle_inc = 60.0 / len(self.death_spawn)
                for spawn_type in self.death_spawn:
                    next_angle = angle + angle_inc
                    heading = random.uniform(angle, next_angle) % 360
                    angle = next_angle
                    spawn = GameObjectFactory.create(spawn_type, heading=heading)
                    spawn.set_pos(self.pos)
                    direction = Transform.rotate(self.mover.direction, heading)
                    spawn.mover.set_direction(direction)
                    spawn.transform()
        try:
            instigator.add_score(self.score_on_die)
        except AttributeError:
            pass
        super().die(instigator)


@GameObjectFactory.register("AsteroidSpawner")
class AsteroidSpawner(Updatable):
    """Spawns asteroids just to be annoying."""

    def __init__(self, asteroid_types, spawn_freq, render_group):
        self.asteroid_types = asteroid_types
        self.spawn_freq = spawn_freq
        self.time_to_next_spawn = random.randrange(spawn_freq)
        self.render_group = render_group

    def set_player(self, player):
        """Sets the player game object."""
        self.player = player

    def update(self, delta):
        self.time_to_next_spawn -= delta
        if self.time_to_next_spawn <= 0:
            self.time_to_next_spawn = random.randrange(self.spawn_freq)
            asteroid_type = random.choice(self.asteroid_types)
            heading = random.randrange(0, 360)
            asteroid = GameObjectFactory.create(asteroid_type, heading=heading)
            pos, direction = self.get_random_pos_dir(self.render_group.get_world_view_rect())
            asteroid.mover.set_direction(direction)
            asteroid.set_pos(pos)
            asteroid.transform()
            for attachment in asteroid.attachments:
                attachment.game_object.set_target(self.player)

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
