import sys

import pygame

sys.path.append("./GameEngine")

from asteroid import Asteroid, AsteroidSpawner
from collision_manager import CollisionManager
from game import Game
from game_object_factory import GameObjectFactory
from level import Level
from render_group import RenderGroup
from shield import Shield
from ship import Ship
from sprite_group import SpriteGroup
from turret import Turret


def main():
    pygame.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

    GameObjectFactory.initialize(open("Assets/inventory.json"))

    # Create world
    pygame.display.set_icon(GameObjectFactory.surfaces["ship"])
    pygame.display.set_caption("Game")

    game = GameObjectFactory.create("SpaceShooterGame", screen=screen)

    level = None
    if len(sys.argv) > 1:
        level = GameObjectFactory.create(sys.argv[1])
    else:
        level = GameObjectFactory.create("Level_01")
    level.create_objects(game.render_group)
    player = level.player

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    player.fire()

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            player.set_heading(player.heading + player.mover.angular_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_heading(player.heading - player.mover.angular_velocity)
        if pressed_keys[pygame.K_w]:
            player.set_velocity(player.mover.max_velocity)
        if pressed_keys[pygame.K_s]:
            player.set_velocity(player.mover.velocity * 0.8)

        # Update groups
        delta = clock.get_time()
        game.update(delta)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
