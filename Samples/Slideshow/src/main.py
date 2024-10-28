import logging
import os

# The following lines are required only when running directly from a terminal window. VSCode launches don't need this.
if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    import sys
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.path.append("../../../src")

import pygame
import pygamengn

from slideshow import Slideshow


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.init()

    # Create window
    screen = pygame.display.set_mode((1920, 1080), pygame.DOUBLEBUF | pygame.HWSURFACE)

    factory = create_factory(os.path.join("..", "..", "Assets"))

    # Initialize window
    pygame.display.set_caption("Slideshow")
    pygame.mouse.set_visible(False)

    game = factory.create("Slideshow", screen=screen)

    clock = pygame.time.Clock()

    while game.running:
        delta = clock.get_time()
        if delta > 20:
            print(f"Bad FPS! {delta}")
        game.update(delta)

        clock.tick_busy_loop(60)

    pygame.quit()


def create_factory(assets_dir) -> pygamengn.GameObjectFactory:
    """Instantiates GameObjectFactory, the factory that will create all the game objects."""
    try:
        from inventory import images
    except ImportError:
        images = {}
    try:
        from inventory import sounds
    except ImportError:
        sounds = {}
    try:
        from inventory import assets
    except ImportError:
        assets = {
            "RenderGroup": {
                "class_name": "RenderGroup",
                "kwargs": {
                }
            },
            "LayerManager": {
                "class_name": "LayerManager",
                "kwargs": {
                    "layers": [
                    ]
                }
            },
        }
    try:
        from inventory import game_types
    except ImportError:
        game_types = {}

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
