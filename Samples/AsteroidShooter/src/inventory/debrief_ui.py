game_types = {
    "DebriefUI": {
        "class_name": "DebriefUI",
        "kwargs": {
            "game_object:component": "container",
            "game_object:asteroid_spawner": "/MainMenu/AsteroidSpawner",
        },
        "container": {
            "class_name": "ColourPanel",
            "kwargs": {
                "pos": [0.25, 0.15],
                "size": [0.5, 0.7],
                "game_object:children": [
                    "ContinueButton",
                    "AsteroidRowPanel",
                    "WaypointRowPanel",
                    "FinalScorePanel",
                ],
                "fix_aspect_ratio": False,
                "corner_radius": 0.05,
                "colour": [100, 100, 100, 128],
            },
            "ContinueButton": {
                "base_type": "/MainMenu/MenuButton",
                "kwargs": {
                    "pos": [0.25, 0.7],
                    "size": [0.5, 0.15],
                    "game_object:children": [
                        "ContinueText",
                    ],
                    "name": "continue_button",
                },
                "ContinueText": {
                    "base_type": "/MainMenu/MenuButton/MenuButtonText",
                    "kwargs": {
                        "text": "Continue",
                    }
                }
            },
            "AsteroidRowPanel": {
                "base_type": "/DebriefUI/DebriefRowPanel",
                "kwargs": {
                    "game_object:children": [
                        "Spinner",
                        "Count",
                        "Multiplier",
                        "Total"
                    ],
                    "pos": [0.1, 0.15]
                },
                "Spinner": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Spinner",
                    "kwargs": {
                        "image:image_asset": "asteroid_04",
                        "angular_velocity": 45
                    }
                },
                "Count": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Count",
                    "kwargs": {
                        "game_object:children": [
                            "CountText"
                        ]
                    },
                    "CountText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "asteroid_count_text"
                        }
                    }
                },
                "Multiplier": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Multiplier",
                    "kwargs": {
                        "game_object:children": [
                            "MultiplierText"
                        ]
                    },
                    "MultiplierText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "asteroid_multiplier_text"
                        }
                    }
                },
                "Total": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Total",
                    "kwargs": {
                        "game_object:children": [
                            "TotalText"
                        ]
                    },
                    "TotalText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "asteroid_total_text"
                        }
                    }
                }
            },
            "WaypointRowPanel": {
                "base_type": "/DebriefUI/DebriefRowPanel",
                "kwargs": {
                    "game_object:children": [
                        "Spinner",
                        "Count",
                        "Multiplier",
                        "Total"
                    ],
                    "pos": [0.1, 0.3]
                },
                "Spinner": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Spinner",
                    "kwargs": {
                        "image:image_asset": "waypoint",
                        "angular_velocity":-45
                    }
                },
                "Count": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Count",
                    "kwargs": {
                        "game_object:children": [
                            "CountText"
                        ]
                    },
                    "CountText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "waypoint_count_text"
                        }
                    }
                },
                "Multiplier": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Multiplier",
                    "kwargs": {
                        "game_object:children": [
                            "MultiplierText"
                        ]
                    },
                    "MultiplierText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "waypoint_multiplier_text"
                        }
                    }
                },
                "Total": {
                    "base_type": "/DebriefUI/DebriefRowPanel/Total",
                    "kwargs": {
                        "game_object:children": [
                            "TotalText"
                        ]
                    },
                    "TotalText": {
                        "base_type": "/DebriefUI/DebriefRowPanel/RowText",
                        "kwargs": {
                            "name": "waypoint_total_text"
                        }
                    }
                }
            },
            "FinalScorePanel": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.1, 0.45],
                    "size": [0.8, 0.1],
                    "game_object:children": [
                        "Spinner",
                        "TotalTitlePanel",
                        "TotalScorePanel"
                    ],
                    "corner_radius": 0.15,
                    "fix_aspect_ratio": False,
                    "colour": [150, 150, 150, 100]
                },
                "Spinner": {
                    "class_name": "Spinner",
                    "kwargs": {
                        "pos": [0, 0.12],
                        "size": [0.1, 1],
                        "fix_aspect_ratio": True,
                        "image:image_asset": "ship",
                        "angular_velocity": 30
                    }
                },
                "TotalTitlePanel": {
                    "class_name": "ColourPanel",
                    "kwargs": {
                        "pos": [0.1, 0.08],
                        "size": [0.6, 1],
                        "game_object:children": [
                            "TotalTitleText"
                        ],
                        "fix_aspect_ratio": False,
                        "corner_radius": 0.15,
                        "colour": [0, 0, 0, 0]
                    },
                    "TotalTitleText": {
                        "class_name": "TextPanel",
                        "kwargs": {
                            "pos": [0, 0],
                            "size": [1, 1],
                            "fix_aspect_ratio": True,
                            "asset:font_asset": "fast_hand_font",
                            "text_colour": [0, 200, 100],
                            "horz_align": "RIGHT",
                            "vert_align": "CENTRE",
                            "text": "Final Score"
                        }
                    }
                },
                "TotalScorePanel": {
                    "class_name": "ColourPanel",
                    "kwargs": {
                        "pos": [0.7, 0],
                        "size": [0.3, 1],
                        "game_object:children": [
                            "TotalText"
                        ],
                        "fix_aspect_ratio": False,
                        "corner_radius": 0.15,
                        "colour": [0, 0, 0, 0]
                    },
                    "TotalText": {
                        "class_name": "TextPanel",
                        "kwargs": {
                            "pos": [0, 0],
                            "size": [1, 1],
                            "fix_aspect_ratio": True,
                            "name": "total_score_text",
                            "asset:font_asset": "fast_hand_font",
                            "text_colour": [0, 200, 100],
                            "horz_align": "RIGHT",
                            "vert_align": "CENTRE",
                            "text": "0"
                        }
                    }
                }
            },
        },
        "DebriefRowPanel": {
            "class_name": "ColourPanel",
            "kwargs": {
                "size": [0.8, 0.1],
                "game_object:children": [],
                "fix_aspect_ratio": False,
                "corner_radius": 0.15,
                "colour": [150, 150, 150, 100]
            },
            "Spinner": {
                "class_name": "Spinner",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [0.1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                }
            },
            "Count": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.1, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
                    "corner_radius": 0.15,
                    "colour": [0, 0, 0, 0]
                }
            },
            "Multiplier": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.4, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
                    "corner_radius": 0.15,
                    "colour": [0, 0, 0, 0]
                }
            },
            "Total": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.7, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
                    "corner_radius": 0.15,
                    "colour": [0, 0, 0, 0]
                }
            },
            "RowText": {
                "class_name": "TextPanel",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                    "asset:font_asset": "fast_hand_font",
                    "text_colour": [0, 200, 100],
                    "horz_align": "RIGHT",
                    "vert_align": "CENTRE",
                    "text": "0"
                },
            },
        },
    },
}
