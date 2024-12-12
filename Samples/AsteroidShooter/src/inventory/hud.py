import pygame

game_types = {
    "Hud": {
        "class_name": "Hud",
        "kwargs": {
            "game_object:component": "container",
        },
        "container": {
            "class_name": "Component",
            "kwargs": {
                "game_object:children": [
                    "ScorePanel",
                    "TimePanel",
                    "Joystick",
                ],
                "name": "hud",
            },
            "ScorePanel": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [0.1, 0.06],
                    "game_object:children": [
                        "ScoreText"
                    ],
                    "fix_aspect_ratio": True,
                    "corner_radius": 0.3,
                    "colour": [100, 100, 100, 100]
                },
                "ScoreText": {
                    "base_type": "/Hud/HudText",
                    "kwargs": {
                        "horz_align": "RIGHT",
                        "text": "0",
                        "name": "score_text",
                        "auto_font_size": True,
                        "auto_font_size_factor": 0.8,
                    },
                },
            },
            "TimePanel": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "horz_align": "CENTRE",
                    "vert_align": "BOTTOM",
                    "size": [0.12, 0.06],
                    "game_object:children": [
                        "TimeText",
                    ],
                    "fix_aspect_ratio": True,
                    "corner_radius": 0.3,
                    "colour": [100, 100, 100, 100],
                },
                "TimeText": {
                    "base_type": "/Hud/HudText",
                    "kwargs": {
                        "text": "00:00",
                        "name": "time_text",
                        "auto_font_size": True,
                        "auto_font_size_factor": 0.8,
                    },
                },
            },
            "Joystick": {
                "class_name": "Component",
                "kwargs": {
                    "name": "joystick",
                    "game_object:children": ["Stick", "Button", "Pause"],
                },
                "Stick": {
                    "class_name": "TexturePanel",
                    "kwargs": {
                        "name": "stick",
                        "pos": [0.03, 0.7],
                        "size": [0.25, 0.25],
                        "image:image_asset": "joystick",
                        "game_object:children": [
                            "Ship",
                        ],
                    },
                    "Ship": {
                        "class_name": "Spinner",
                        "kwargs": {
                            "image:image_asset": "ship-alpha",
                            "horz_align": "CENTRE",
                            "vert_align": "CENTRE",
                            "size": [0.5, 0.5],
                            "name": "ship",
                        },
                    },
                },
                "Button": {
                    "class_name": "Component",
                    "kwargs": {
                        "pos": [0.85, 0.75],
                        "size": [0.15, 0.25],
                        "game_object:children": ["ButtonPanel"],
                    },
                    "ButtonPanel": {
                        "class_name": "TexturePanel",
                        "kwargs": {
                            "size": [0.5, 0.5],
                            "image:image_asset": "red-button",
                            "name": "button",
                        },
                    },
                },
                "Pause": {
                    "class_name": "Component",
                    "kwargs": {
                        "pos": [0.85, 0.15],
                        "size": [0.15, 0.25],
                        "game_object:children": ["ButtonPanel"],
                    },
                    "ButtonPanel": {
                        "class_name": "TexturePanel",
                        "kwargs": {
                            "size": [0.3, 0.3],
                            "image:image_asset": "pause-button",
                            "name": "pause_button",
                        },
                    },
                },
            },
        },
        "HudText": {
            "class_name": "TextPanel",
            "kwargs": {
                "fix_aspect_ratio": True,
                "asset:font_asset": "fast_hand_font",
                "text_colour": [0, 200, 100],
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "shadow_colour": [0, 50, 25],
            },
        },
    },
}
