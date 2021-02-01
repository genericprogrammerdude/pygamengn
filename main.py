import logging
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
sys.path.append("./GameEngine")

import pygame

from class_registrar import ClassRegistrar
from game_object_factory import GameObjectFactory
from space_shooter_game import SpaceShooterGame


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    factory = create_factory()

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


def create_factory() -> GameObjectFactory:
    """Instantiates GameObjectFactory, the factory that will create all the game objects."""
    from Assets.inventory import images, sounds, assets, game_types
    factory = GameObjectFactory(ClassRegistrar.registry, images, sounds, assets, game_types)
    factory.set_layer_manager_asset_name("LayerManager")
    return factory


if __name__ == "__main__":
    main()
