import logging
import os
import sys

# The following 3 lines are required only when running directly from a terminal window. VSCode launches don't need this.
if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.path.append("../../../src")

import pygame
import pygamengn

from space_nerds_mp_game import SpaceNerdsMPGame


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.init()

    # Create window
    screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    factory = create_factory(os.path.join("..", "..", "Assets"))

    # Initialize window
    pygame.display.set_icon(factory.images["ship_blue"])
    pygame.display.set_caption("Space Nerds MP")

    game = factory.create("SpaceNerdsMPGame", screen=screen)

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        game.update(delta)

        clock.tick(60)

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
    factory.set_replication_manager_asset_name("ReplicationManager")
    return factory


if __name__ == "__main__":
    main()
