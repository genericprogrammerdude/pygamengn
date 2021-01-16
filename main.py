import sys

import pygame

sys.path.append("./GameEngine")

from game_object_factory import GameObjectFactory
from space_shooter_game import SpaceShooterGame


def main():
    pygame.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    GameObjectFactory.initialize(open("Assets/inventory.json"))

    # Create world
    pygame.display.set_icon(GameObjectFactory.surfaces["ship"])
    pygame.display.set_caption("Game")

    game = GameObjectFactory.create("SpaceShooterGame", screen=screen)

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        game.update(delta)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
