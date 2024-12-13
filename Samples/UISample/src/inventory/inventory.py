images = {
    "ship": {
        "class_name": "ImageAsset",
        "kwargs": {
            "fname": "SpaceShooterRedux/PNG/playerShip2_blue.png",
        },
    },
    "ship_icon": {
        "class_name": "ImageAsset",
        "kwargs": {
            "fname": "favicon.png",
        }
    },
}

sounds = {
}

assets = {
    "RenderGroup": {
        "class_name": "RenderGroup",
        "kwargs": {
            "grid_draw": False,
            "grid_colour": [100, 100, 100],
            "grid_interval": 100,
        },
    },
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": [],
        },
    },
    "fast_hand_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "fast-hand-font/FastHand-lgBMV.ttf",
            "size": 50,
        },
    },
}


from pygame import MOUSEBUTTONDOWN, MOUSEMOTION

game_types = {
    "UISample": {
        "class_name": "UISample",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:main_menu_ui": "/MainMenu",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": []
            },
        },
    },
    "MainMenu": {
        "class_name": "MainMenu",
        "kwargs": {
            "game_object:component": "Background",
        },
        "Background": {
            "class_name": "ColourPanel",
            "kwargs": {
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "size": [0.5, 0.5],
                "game_object:children": [
                    "StartButton",
                    "ExitButton",
                    "SpinnerPanel",
                    "StaticShipPanel",
                ],
                "name": "main_menu",
                "colour": [100, 100, 100, 128],
                "corner_radius": 0.1,
                "game_object:corner_radii": "corner_radii",
                "border_width": 0.005,
                "border_colour": [0, 200, 100],
            },
            "corner_radii": {
                "class_name": "CornerRadii",
                "kwargs": {
                    "top_left": 0.125,
                    "top_right": 0.25,
                    "bottom_right": 0.375,
                    "bottom_left": 0.5,
                },
            },
            "MenuButton": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "size": [0.5, 0.25],
                    "game_object:children": [],
                    "colour": [200, 200, 200, 100],
                    "hover_colour": [100, 210, 100, 100],
                    "corner_radius": 0.15,
                    "game_object:corner_radii": "/MainMenu/Background/corner_radii",
                    "wanted_mouse_events": [MOUSEBUTTONDOWN, MOUSEMOTION],
                },
                "MenuButtonText": {
                    "class_name": "TextPanel",
                    "kwargs": {
                        "asset:font_asset": "fast_hand_font",
                        "text_colour": [0, 200, 100],
                        "shadow_colour": [0, 20, 10],
                        "horz_align": "CENTRE",
                        "vert_align": "CENTRE",
                    }
                }
            },
            "StartButton": {
                "base_type": "/MainMenu/Background/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.2],
                    "game_object:children": [
                        "StartText",
                    ],
                    "name": "start_button",
                },
                "StartText": {
                    "base_type": "/MainMenu/Background/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Start",
                        "name": "start_text",
                    },
                },
            },
            "ExitButton": {
                "base_type": "/MainMenu/Background/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.55],
                    "game_object:children": [
                        "ExitText",
                    ],
                    "name": "exit_button",
                },
                "ExitText": {
                    "base_type": "/MainMenu/Background/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Exit",
                        "name": "exit_text",
                        "auto_font_size": True,
                        "auto_font_size_factor": 0.8,
                    },
                },
            },
            "SpinnerPanel": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.8, 0.4],
                    "size": [0.15, 0.2],
                    "colour": [240, 200, 200, 100],
                    "game_object:children": [
                        "Spinner",
                    ],
                    "name": "spinner_panel",
                },
                "Spinner": {
                    "class_name": "Spinner",
                    "kwargs": {
                        "vert_align": "CENTRE",
                        "horz_align": "CENTRE",
                        "size": [0.8, 0.8],
                        "image:image_asset": "ship",
                        "name": "spinner",
                        "angular_velocity": 40,
                    },
                },
            },
            "StaticShipPanel": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "vert_align": "CENTRE",
                    "pos": [0.05, -0.02],
                    "size": [0.15, 0.4],
                    "colour": [200, 20, 200, 100],
                    "game_object:children": [
                        "ShipPanel",
                    ],
                    "name": "static_ship",
                },
                "ShipPanel": {
                    "class_name": "TexturePanel",
                    "kwargs": {
                        "vert_align": "CENTRE",
                        "horz_align": "CENTRE",
                        "size": [0.45, 0.2],
                        "image:image_asset": "ship",
                        "fix_aspect_ratio": True,
                        "wanted_mouse_events": [MOUSEMOTION],
                        "scale_texture_to_rect": False,
                    },
                },
            },
        },
    },
}
