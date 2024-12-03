import asyncio
import logging
import os

# The following lines are required only when running directly from a terminal window. VSCode launches don't need this.
if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    import sys
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.path.append("../../../src")

import pygame
import pygamengn

from asteroid_shooter_game import AsteroidShooterGame


async def main(assets_dir: str = None):
    logging.basicConfig(level=logging.WARN, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    if not assets_dir:
        assets_dir = os.path.join("..", "..", "Assets")
    factory = create_factory(assets_dir)

    # Initialize window
    pygame.display.set_icon(factory.images["ship_icon"])
    pygame.display.set_caption("Asteroid Shooter")

    game = factory.create("AsteroidShooterGame", screen=screen)

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        game.update(delta)

        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


def create_factory(assets_dir) -> pygamengn.GameObjectFactory:
    """Instantiates GameObjectFactory, the factory that will create all the game objects."""
    from inventory.inventory import images, sounds, assets, game_types
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
    asyncio.run(main())
