import asyncio
import logging
import os
import time

# The following lines are required only when running directly from a terminal window. VSCode launches don't need this.
if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    import sys
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.path.append("../../../src")

import pygame
import pygamengn

from asteroid_shooter_game import AsteroidShooterGame


async def main(assets_dir: str = None):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    t = time.time()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    logging.info(f"Initialized pygame: {time.time() - t:.3f} seconds")
    t = time.time()

    if not assets_dir:
        assets_dir = os.path.join("..", "..", "Assets")
    factory = await create_factory(assets_dir)
    logging.info(f"Created factory: {time.time() - t:.3f} seconds")
    t = time.time()

    # Create window
    screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)

    # Initialize window
    pygame.display.set_icon(factory.images["ship_icon"].surface)
    pygame.display.set_caption("Asteroid Continuum 1983")

    logging.info(f"Create game")
    game = factory.create("AsteroidShooterGame", screen=screen)
    logging.info(f"Created game: {time.time() - t:.3f} seconds")

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        game.update(delta)

        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


async def create_factory(assets_dir) -> pygamengn.GameObjectFactory:
    """Instantiates GameObjectFactory, the factory that will create all the game objects."""
    from inventory.inventory import images, sounds, assets, game_types
    factory = pygamengn.GameObjectFactory(
        pygamengn.ClassRegistrar.registry,
    )
    await factory.load(
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
