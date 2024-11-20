images = {
    "ship": "SpaceShooterRedux/PNG/playerShip2_blue.png",
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
        }
    },
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": [
            ]
        }
    },
    "fast_hand_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "fast-hand-font/FastHand-lgBMV.ttf",
            "size": 42
        }
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
            # "game_object:pause_menu_ui": "/PauseMenu",
            # "game_object:debrief_panel": "/DebriefPanel",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": [
                ]
            }
        }
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
                "border_width": 0.01,
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
                        "shadow": True,
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
                        "name": "start_button_text",
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
                        "name": "exit_button_text",
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
                    ]
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
                    ]
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
                    },
                },
            },
        },
    },
    # "PauseMenu": {
    #     "class_name": "PauseMenu",
    #     "kwargs": {
    #         "pos": [0.25, 0.25],
    #         "size": [0.5, 0.5],
    #         "game_object:children": [
    #             "ResumeButton",
    #             "ExitButton"
    #         ],
    #         "fix_aspect_ratio": False,
    #         "corner_radius": 0.05,
    #         "colour": [100, 100, 100, 128]
    #     },
    #     "ResumeButton": {
    #         "base_type": "/MainMenu/MenuButton",
    #         "kwargs": {
    #             "pos": [0.25, 0.2],
    #             "game_object:children": [
    #                 "ResumeText"
    #             ],
    #             "name": "resume_button"
    #         },
    #         "ResumeText": {
    #             "base_type": "/MainMenu/MenuButton/MenuButtonText",
    #             "kwargs": {
    #                 "text": "Resume Game"
    #             }
    #         }
    #     },
    #     "ExitButton": {
    #         "base_type": "/MainMenu/MenuButton",
    #         "kwargs": {
    #             "pos": [0.25, 0.55],
    #             "game_object:children": [
    #                 "ExitText"
    #             ],
    #             "name": "exit_button"
    #         },
    #         "ExitText": {
    #             "base_type": "/MainMenu/MenuButton/MenuButtonText",
    #             "kwargs": {
    #                 "text": "Exit"
    #             }
    #         }
    #     },
    # },
    # "DebriefPanel": {
    #     "class_name": "DebriefPanel",
    #     "kwargs": {
    #         "pos": [0.25, 0.15],
    #         "size": [0.5, 0.7],
    #         "game_object:children": [
    #             "ContinueButton",
    #             "AsteroidRowPanel",
    #             "WaypointRowPanel",
    #             "FinalScorePanel"
    #         ],
    #         "fix_aspect_ratio": False,
    #         "corner_radius": 0.05,
    #         "colour": [100, 100, 100, 128],
    #     },
    #     "ContinueButton": {
    #         "class_name": "ColourPanel",
    #         "kwargs": {
    #             "pos": [0.25, 0.7],
    #             "size": [0.5, 0.15],
    #             "game_object:children": [
    #                 "ContinueText"
    #             ],
    #             "fix_aspect_ratio": False,
    #             "name": "continue_button",
    #             "corner_radius": 0.15,
    #             "colour": [200, 200, 200, 100],
    #             "hover_colour": [100, 210, 100, 100]
    #         },
    #         "ContinueText": {
    #             "class_name": "TextPanel",
    #             "kwargs": {
    #                 "pos": [0, 0],
    #                 "size": [1, 1],
    #                 "game_object:children": [],
    #                 "fix_aspect_ratio": True,
    #                 "asset:font_asset": "fast_hand_font",
    #                 "text_colour": [0, 200, 100],
    #                 "horz_align": "CENTRE",
    #                 "vert_align": "CENTRE",
    #                 "text": "Continue"
    #             }
    #         }
    #     },
    #     "AsteroidRowPanel": {
    #         "base_type": "/DebriefPanel/DebriefRowPanel",
    #         "kwargs": {
    #             "game_object:children": [
    #                 "Spinner",
    #                 "Count",
    #                 "Multiplier",
    #                 "Total"
    #             ],
    #             "pos": [0.1, 0.15]
    #         },
    #         "Spinner": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Spinner",
    #             "kwargs": {
    #                 "image:image_asset": "asteroid_04",
    #                 "angular_velocity": 45
    #             }
    #         },
    #         "Count": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Count",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "CountText"
    #                 ]
    #             },
    #             "CountText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "asteroid_count_text"
    #                 }
    #             }
    #         },
    #         "Multiplier": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Multiplier",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "MultiplierText"
    #                 ]
    #             },
    #             "MultiplierText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "asteroid_multiplier_text"
    #                 }
    #             }
    #         },
    #         "Total": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Total",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "TotalText"
    #                 ]
    #             },
    #             "TotalText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "asteroid_total_text"
    #                 }
    #             }
    #         }
    #     },
    #     "WaypointRowPanel": {
    #         "base_type": "/DebriefPanel/DebriefRowPanel",
    #         "kwargs": {
    #             "game_object:children": [
    #                 "Spinner",
    #                 "Count",
    #                 "Multiplier",
    #                 "Total"
    #             ],
    #             "pos": [0.1, 0.3]
    #         },
    #         "Spinner": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Spinner",
    #             "kwargs": {
    #                 "image:image_asset": "waypoint",
    #                 "angular_velocity":-45
    #             }
    #         },
    #         "Count": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Count",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "CountText"
    #                 ]
    #             },
    #             "CountText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "waypoint_count_text"
    #                 }
    #             }
    #         },
    #         "Multiplier": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Multiplier",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "MultiplierText"
    #                 ]
    #             },
    #             "MultiplierText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "waypoint_multiplier_text"
    #                 }
    #             }
    #         },
    #         "Total": {
    #             "base_type": "/DebriefPanel/DebriefRowPanel/Total",
    #             "kwargs": {
    #                 "game_object:children": [
    #                     "TotalText"
    #                 ]
    #             },
    #             "TotalText": {
    #                 "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
    #                 "kwargs": {
    #                     "name": "waypoint_total_text"
    #                 }
    #             }
    #         }
    #     },
    #     "FinalScorePanel": {
    #         "class_name": "ColourPanel",
    #         "kwargs": {
    #             "pos": [0.1, 0.45],
    #             "size": [0.8, 0.1],
    #             "game_object:children": [
    #                 "Spinner",
    #                 "TotalTitlePanel",
    #                 "TotalScorePanel"
    #             ],
    #             "corner_radius": 0.15,
    #             "fix_aspect_ratio": False,
    #             "colour": [150, 150, 150, 100]
    #         },
    #         "Spinner": {
    #             "class_name": "Spinner",
    #             "kwargs": {
    #                 "pos": [0, 0.12],
    #                 "size": [0.1, 1],
    #                 "game_object:children": [],
    #                 "fix_aspect_ratio": True,
    #                 "image:image_asset": "ship",
    #                 "angular_velocity": 30
    #             }
    #         },
    #         "TotalTitlePanel": {
    #             "class_name": "ColourPanel",
    #             "kwargs": {
    #                 "pos": [0.1, 0.08],
    #                 "size": [0.6, 1],
    #                 "game_object:children": [
    #                     "TotalTitleText"
    #                 ],
    #                 "fix_aspect_ratio": False,
    #                 "corner_radius": 0.15,
    #                 "colour": [0, 0, 0, 0]
    #             },
    #             "TotalTitleText": {
    #                 "class_name": "TextPanel",
    #                 "kwargs": {
    #                     "pos": [0, 0],
    #                     "size": [1, 1],
    #                     "game_object:children": [],
    #                     "fix_aspect_ratio": True,
    #                     "asset:font_asset": "fast_hand_font",
    #                     "text_colour": [0, 200, 100],
    #                     "horz_align": "RIGHT",
    #                     "vert_align": "CENTRE",
    #                     "text": "Final Score"
    #                 }
    #             }
    #         },
    #         "TotalScorePanel": {
    #             "class_name": "ColourPanel",
    #             "kwargs": {
    #                 "pos": [0.7, 0],
    #                 "size": [0.3, 1],
    #                 "game_object:children": [
    #                     "TotalText"
    #                 ],
    #                 "fix_aspect_ratio": False,
    #                 "corner_radius": 0.15,
    #                 "colour": [0, 0, 0, 0]
    #             },
    #             "TotalText": {
    #                 "class_name": "TextPanel",
    #                 "kwargs": {
    #                     "pos": [0, 0],
    #                     "size": [1, 1],
    #                     "game_object:children": [],
    #                     "fix_aspect_ratio": True,
    #                     "name": "total_score_text",
    #                     "asset:font_asset": "fast_hand_font",
    #                     "text_colour": [0, 200, 100],
    #                     "horz_align": "RIGHT",
    #                     "vert_align": "CENTRE",
    #                     "text": "0"
    #                 }
    #             }
    #         }
    #     },
    #     "DebriefRowPanel": {
    #         "class_name": "ColourPanel",
    #         "kwargs": {
    #             "size": [0.8, 0.1],
    #             "game_object:children": [],
    #             "fix_aspect_ratio": False,
    #             "corner_radius": 0.15,
    #             "colour": [150, 150, 150, 100]
    #         },
    #         "Spinner": {
    #             "class_name": "Spinner",
    #             "kwargs": {
    #                 "pos": [0, 0],
    #                 "size": [0.1, 1],
    #                 "game_object:children": [],
    #                 "fix_aspect_ratio": True,
    #             }
    #         },
    #         "Count": {
    #             "class_name": "ColourPanel",
    #             "kwargs": {
    #                 "pos": [0.1, 0],
    #                 "size": [0.3, 1],
    #                 "fix_aspect_ratio": False,
    #                 "corner_radius": 0.15,
    #                 "colour": [0, 0, 0, 0]
    #             }
    #         },
    #         "Multiplier": {
    #             "class_name": "ColourPanel",
    #             "kwargs": {
    #                 "pos": [0.4, 0],
    #                 "size": [0.3, 1],
    #                 "fix_aspect_ratio": False,
    #                 "corner_radius": 0.15,
    #                 "colour": [0, 0, 0, 0]
    #             }
    #         },
    #         "Total": {
    #             "class_name": "ColourPanel",
    #             "kwargs": {
    #                 "pos": [0.7, 0],
    #                 "size": [0.3, 1],
    #                 "fix_aspect_ratio": False,
    #                 "corner_radius": 0.15,
    #                 "colour": [0, 0, 0, 0]
    #             }
    #         },
    #         "RowText": {
    #             "class_name": "TextPanel",
    #             "kwargs": {
    #                 "pos": [0, 0],
    #                 "size": [1, 1],
    #                 "game_object:children": [],
    #                 "fix_aspect_ratio": True,
    #                 "asset:font_asset": "fast_hand_font",
    #                 "text_colour": [0, 200, 100],
    #                 "horz_align": "RIGHT",
    #                 "vert_align": "CENTRE",
    #                 "text": "0"
    #             }
    #         }
    #     }
    # },
}
