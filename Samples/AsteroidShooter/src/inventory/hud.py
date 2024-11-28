game_types = {
    "Hud": {
        "class_name": "Root",
        "kwargs": {
            "game_object:component": "container",
            "handles_input": False,
        },
        "container": {
            "class_name": "Component",
            "kwargs": {
                "game_object:children": [
                    "ScorePanel",
                    "TimePanel",
                    "Joystick",
                ],
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
                    "horz_align": "RIGHT",
                    "vert_align": "TOP",
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
                "class_name": "ColourPanel",
                "kwargs": {
                    "vert_align": "BOTTOM",
                    "pos": [0.028, -0.03],
                    "size": [0.1688, 0.3],
                    "corner_radius": 0.5,
                    "colour": [100, 100, 100, 80],
                    "fix_aspect_ratio" : True,
                    "game_object:children": [
                        "Ship",
                    ],
                },
                "Ship": {
                    "class_name": "TexturePanel",
                    "kwargs": {
                        "horz_align": "CENTRE",
                        "vert_align": "CENTRE",
                        "pos": [0, -0.02],
                        "size": [0.6, 0.6],
                        "image:image_asset": "ship",
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
            },
        },
    },
}
