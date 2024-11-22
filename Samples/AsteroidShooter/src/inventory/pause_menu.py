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
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "size": [0.5, 0.5],
                "game_object:children": [
                    "ResumeButton",
                    "ExitButton",
                ],
                "name": "pause_menu",
                "colour": [100, 100, 100, 128],
                "corner_radius": 0.125,
                "border_width": 0.005,
                "border_colour": [0, 200, 100],
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
                        "text": "Resume",
                        "name": "resume_text",
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
                        "name": "exit_text",
                    },
                },
            },
        },
    },
}
