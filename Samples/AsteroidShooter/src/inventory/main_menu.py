import pygame

game_types = {
    "MainMenu": {
        "class_name": "MainMenu",
        "kwargs": {
            "game_object:component": "container",
            "game_object:asteroid_spawner": "AsteroidSpawner",
        },
        "container": {
            "class_name": "ColourPanel",
            "kwargs": {
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "size": [0.5, 0.5],
                "game_object:children": [
                    "StartButton",
                    "ExitButton",
                ],
                "name": "main_menu",
                "fix_aspect_ratio": False,
                "colour": [100, 100, 100, 128],
                "corner_radius": 0.125,
                "border_width": 0.005,
                "border_colour": [0, 200, 100],
            },
            "StartButton": {
                "base_type": "/MainMenu/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.2],
                    "game_object:children": [
                        "StartText"
                    ],
                    "name": "start_button"
                },
                "StartText": {
                    "base_type": "/MainMenu/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Start",
                        "name": "start_text",
                    },
                },
            },
            "ExitButton": {
                "base_type": "/MainMenu/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.55],
                    "game_object:children": [
                        "ExitText"
                    ],
                    "name": "exit_button"
                },
                "ExitText": {
                    "base_type": "/MainMenu/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Exit",
                        "name": "exit_text",
                    },
                },
            },
        },
        "MenuButton": {
            "class_name": "ColourPanel",
            "kwargs": {
                "size": [0.5, 0.25],
                "game_object:children": [],
                "fix_aspect_ratio": False,
                "colour": [200, 200, 200, 100],
                "hover_colour": [100, 210, 100, 100],
                "corner_radius": 0.15,
                "wanted_mouse_events": [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION],
            },
            "MenuButtonText": {
                "class_name": "TextPanel",
                "kwargs": {
                    "horz_align": "CENTRE",
                    "vert_align": "CENTRE",
                    "size": [1, 1],
                    "fix_aspect_ratio": True,
                    "asset:font_asset": "fast_hand_font",
                    "text_colour": [0, 200, 100],
                    "shadow_colour": [0, 50, 25],
                }
            }
        },
        "AsteroidSpawner": {
            "class_name": "AsteroidSpawner",
            "kwargs": {
                "type_spec:asteroid_types": [
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidSmall",
                    "AsteroidTiny"
                ],
                "spawn_freq": 3000,
                "asset:render_group": "RenderGroup"
            },
        },
    },
}
