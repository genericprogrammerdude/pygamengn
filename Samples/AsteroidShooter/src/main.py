import logging
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
sys.path.append("../../../src")
sys.path.append("../../../src/pygamengn")

import pygame
import pygamengn

from space_shooter_game import SpaceShooterGame


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    factory = create_factory(os.path.join("..", "Assets"))

    # Create world
    pygame.display.set_icon(factory.images["ship"])
    pygame.display.set_caption("Game")

    game = factory.create("SpaceShooterGame", screen=screen)

    clock = pygame.time.Clock()

    server = pygamengn.Server()
    server.start()

    client = pygamengn.Client(server.address[0], server.address[1])

    while game.running:
        client.connect()
        client.send(b"Hello, World")
        print("client received: \"{0}\"".format(client.receive()))
        delta = clock.get_time()
        game.update(delta)
        clock.tick(60)

    server.stop()

    pygame.quit()


def create_factory(assets_dir) -> pygamengn.GameObjectFactory:
    """Instantiates GameObjectFactory, the factory that will create all the game objects."""
    from inventory import images, sounds, assets, game_types
    factory = pygamengn.GameObjectFactory(
        pygamengn.ClassRegistrar.registry,
        assets_dir,
        images,
        sounds,
        assets,
        game_types
    )
    factory.set_layer_manager_asset_name("LayerManager")
    return factory


if __name__ == "__main__":
    main()
