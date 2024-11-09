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
    logging.basicConfig(level=logging.FATAL, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    pygame.init()

    # Create window
    flags = 0 #pygame.DOUBLEBUF | pygame.SCALED | pygame.OPENGL
    # screen = pygame.display.set_mode(size = (960, 540), flags = flags, depth = 3, vsync = 1)
    screen = pygame.display.set_mode(size = (1920, 1080), flags = flags, depth = 3, vsync = 1)
    # print(pygame.display.Info())

    factory = create_factory(os.path.join("..", "..", "Assets"))

    # Initialize window
    pygame.display.set_caption("Slideshow")
    pygame.mouse.set_visible(False)

    game = factory.create("Slideshow", screen=screen)

    capture_video = True

    if not capture_video:
        clock = pygame.time.Clock()
        while game.running:
            delta = clock.get_time()
            game.update(delta)
            clock.tick_busy_loop(60)

    else:
        import moviepy.editor
        import numpy
        import inventory

        class FrameMaker:
            def __init__(self, fps):
                self.__fps = fps
                self.__delta = 1000 / self.__fps

            def make_frame(self, t):
                game.update(self.__delta)
                surface = pygame.display.get_surface()
                r = pygame.surfarray.pixels_red(surface)
                g = pygame.surfarray.pixels_green(surface)
                b = pygame.surfarray.pixels_blue(surface)
                rv = numpy.stack((r, g, b)).T
                return rv

        fps = 30
        duration = (
            inventory.image_load_count * (inventory.on_display_time + inventory.flying_in_time) / 1000 +
            inventory.flying_out_time / 1000
        )
        frame_maker = FrameMaker(fps = fps)

        clip = moviepy.editor.VideoClip(frame_maker.make_frame, duration = duration)
        clip.write_videofile(
            "mama.mp4",
            fps = fps,
            codec = "mpeg4",
            audio = False,
            preset = "ultrafast",
            threads = 8,
        )
        clip.close()

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
