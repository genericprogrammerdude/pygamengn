import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
sys.path.append("./GameEngine")

import pygame

from class_registrar import ClassRegistrar
from game_object_factory import GameObjectFactory
from space_shooter_game import SpaceShooterGame


def main():
    pygame.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    factory = GameObjectFactory(ClassRegistrar.registry, open("Assets/inventory.json"))
    factory.set_layer_manager_asset_name("LayerManager")

    # Create world
    pygame.display.set_icon(factory.images["ship"])
    pygame.display.set_caption("Game")

    game = factory.create("SpaceShooterGame", screen=screen)

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        game.update(delta)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
