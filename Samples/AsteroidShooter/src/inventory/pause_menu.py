game_types = {
    "PauseMenu": {
        "class_name": "PauseMenu",
        "kwargs": {
            "game_object:component": "container",
            "update_on_pause": True,
        },
        "container": {
            "class_name": "ColourPanel",
            "kwargs": {
                "pos": [0.25, 0.25],
                "size": [0.5, 0.5],
                "game_object:children": [
                    "ResumeButton",
                    "ExitButton",
                ],
                "fix_aspect_ratio": False,
                "corner_radius": 0.05,
                "colour": [100, 100, 100, 128],
            },
            "ResumeButton": {
                "base_type": "/MainMenu/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.2],
                    "game_object:children": [
                        "ResumeText",
                    ],
                    "name": "resume_button"
                },
                "ResumeText": {
                    "base_type": "/MainMenu/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Resume Game",
                    },
                },
            },
            "ExitButton": {
                "base_type": "/MainMenu/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.55],
                    "game_object:children": [
                        "ExitText",
                    ],
                    "name": "exit_button",
                },
                "ExitText": {
                    "base_type": "/MainMenu/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Exit",
                    },
                },
            },
        },
    },
}
