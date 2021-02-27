images = {
    "ship": "SpaceShooterRedux/PNG/playerShip2_blue.png",
    "explosion1": "Explosions/explosion1.png",
    "explosion2": "Explosions/explosion2.png",
    "explosion3": "Explosions/explosion3.png",
    "explosion4": "Explosions/explosion4.png",
    "shield1": "SpaceShooterRedux/PNG/Effects/shield1.png",
    "shield2": "SpaceShooterRedux/PNG/Effects/shield2.png",
    "shield3": "SpaceShooterRedux/PNG/Effects/shield3.png",
    "turret": "SpaceShooterRedux/PNG/Parts/turretBase_big.png",
    "turret_gun": "SpaceShooterRedux/PNG/Parts/gun04.png",
    "turret_projectile": "SpaceShooterRedux/PNG/Lasers/laserRed06.png",
    "player_projectile": "SpaceShooterRedux/PNG/Lasers/laserGreen07.png",
    "player_health_bar_fg": "SpaceShooterRedux/PNG/Lasers/laserBlue02.png",
    "player_health_bar_bg": "SpaceShooterRedux/PNG/Lasers/laserBlue14.png",
    "turret_health_bar_fg": "SpaceShooterRedux/PNG/Lasers/laserRed02.png",
    "turret_health_bar_bg": "SpaceShooterRedux/PNG/Lasers/laserRed14.png",
    "turret_projectile2": "SpaceShooterRedux/PNG/Lasers/laserBlue01.png",
    "asteroid_00": "SpaceShooterRedux/PNG/Meteors/meteorBrown_big1.png",
    "asteroid_01": "SpaceShooterRedux/PNG/Meteors/meteorBrown_big2.png",
    "asteroid_02": "SpaceShooterRedux/PNG/Meteors/meteorBrown_big3.png",
    "asteroid_03": "SpaceShooterRedux/PNG/Meteors/meteorBrown_big4.png",
    "asteroid_04": "SpaceShooterRedux/PNG/Meteors/meteorBrown_med1.png",
    "asteroid_05": "SpaceShooterRedux/PNG/Meteors/meteorBrown_med2.png",
    "asteroid_06": "SpaceShooterRedux/PNG/Meteors/meteorBrown_small1.png",
    "asteroid_07": "SpaceShooterRedux/PNG/Meteors/meteorBrown_small2.png",
    "asteroid_08": "SpaceShooterRedux/PNG/Meteors/meteorBrown_tiny1.png",
    "asteroid_09": "SpaceShooterRedux/PNG/Meteors/meteorBrown_tiny2.png",
    "background": "SpaceShooterRedux/Backgrounds/darkPurple.png",
    "waypoint": "SpaceShooterRedux/PNG/ufoRed.png",
    "arrow": "arrow.png",
    "0": "SpaceShooterRedux/PNG/UI/numeral0.png",
    "1": "SpaceShooterRedux/PNG/UI/numeral1.png",
    "2": "SpaceShooterRedux/PNG/UI/numeral2.png",
    "3": "SpaceShooterRedux/PNG/UI/numeral3.png",
    "4": "SpaceShooterRedux/PNG/UI/numeral4.png",
    "5": "SpaceShooterRedux/PNG/UI/numeral5.png",
    "6": "SpaceShooterRedux/PNG/UI/numeral6.png",
    "7": "SpaceShooterRedux/PNG/UI/numeral7.png",
    "8": "SpaceShooterRedux/PNG/UI/numeral8.png",
    "9": "SpaceShooterRedux/PNG/UI/numeral9.png"
}

sounds = {
    "ship_shot": "SpaceShooterRedux/Bonus/sfx_laser1.ogg",
    "turret_shot": "SpaceShooterRedux/Bonus/sfx_laser2.ogg",
    "explosion_small": "Explosions/Explosion+1.wav",
    "explosion_large": "Explosions/Explosion+5.wav",
    "enter_sound": "SpaceShooterRedux/Bonus/sfx_shieldUp.ogg"
}

assets = {
    "RenderGroup": {
        "class_name": "RenderGroup",
        "kwargs": {
            "grid_draw": False,
            "grid_color": [100, 100, 100],
            "grid_interval": 100,
            "image:background": "background"
        }
    },
    "PlayerGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "PlayerProjectilesGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "AsteroidsGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "AsteroidProjectilesGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "AsteroidTurretsGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "TriggersGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {}
    },
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": [
                ["Projectile"],
                ["Ship"],
                ["Shield"],
                ["Waypoint", "/PlayerShip/Waypoint/LeftDigit", "/PlayerShip/Waypoint/RightDigit"],
                ["Asteroid"],
                ["/AsteroidMother/AsteroidTurret/AsteroidProjectile"],
                ["/AsteroidMother/AsteroidTurret"],
                ["/AsteroidMother/AsteroidTurret/AsteroidTurretGun"],
                ["NavArrow"],
                ["AnimatedTexture"],
                ["HealthBar"]
            ]
        }
    },
    "explosion_small_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion1"],
            "frame_size": [256, 256]
        }
    },
    "explosion_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion2", "explosion3", "explosion4"],
            "frame_size": [256, 256]
        }
    },
    "explosion_big_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion3", "explosion4"],
            "frame_size": [256, 256]
        }
    },
    "fast_hand_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "fast-hand-font/FastHand-lgBMV.ttf",
            "size": 42
        }
    }
}

game_types = {
    "SpaceNerdsMPGame": {
        "class_name": "SpaceNerdsMPGame",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:main_menu_ui": "/MainMenu",
            "game_object:pause_menu_ui": "/PauseMenu",
            "game_object:debrief_panel": "/DebriefPanel",
            "game_object:score_ui": "/ScorePanel",
            "game_object:time_ui": "/TimePanel",
            "game_object:level": "/Level_02",
            "asteroid_multiplier": 10,
            "waypoint_multiplier": 50
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": [
                    ["PlayerProjectilesGroup", "AsteroidsGroup"],
                    ["AsteroidsGroup", "PlayerGroup"],
                    ["AsteroidProjectilesGroup", "AsteroidsGroup"],
                    ["AsteroidProjectilesGroup", "PlayerGroup"],
                    ["AsteroidTurretsGroup", "AsteroidsGroup"],
                    ["TriggersGroup", "PlayerGroup"]
                ]
            }
        }
    },
    "MainMenu": {
        "class_name": "MainMenu",
        "kwargs": {
            "pos": [0.25, 0.25],
            "size": [0.5, 0.5],
            "game_object:children": [
                "StartButton",
                "MPButton",
                "ExitButton"
            ],
            "fix_aspect_ratio": False,
            "colour": [100, 100, 100, 128],
            "game_object:asteroid_spawner": "AsteroidSpawner"
        },
        "MenuButton": {
            "class_name": "ColourPanel",
            "kwargs": {
                "size": [0.5, 0.25],
                "game_object:children": [],
                "fix_aspect_ratio": False,
                "colour": [200, 200, 200, 100],
                "hover_colour": [100, 210, 100, 100]
            },
            "MenuButtonText": {
                "class_name": "TextPanel",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                    "asset:font_asset": "fast_hand_font",
                    "text_colour": [0, 200, 100],
                    "horz_align": "CENTRE",
                    "vert_align": "CENTRE"
                }
            }
        },
        "StartButton": {
            "base_type": "/MainMenu/MenuButton",
            "kwargs": {
                "pos": [0.25, 0.0625],
                "game_object:children": [
                    "StartText"
                ],
                "name": "start_button"
            },
            "StartText": {
                "base_type": "/MainMenu/MenuButton/MenuButtonText",
                "kwargs": {
                    "text": "Start"
                }
            }
        },
        "MPButton": {
            "base_type": "/MainMenu/MenuButton",
            "kwargs": {
                "pos": [0.25, 0.375],
                "game_object:children": [
                    "MPText"
                ],
                "name": "multiplayer_button"
            },
            "MPText": {
                "base_type": "/MainMenu/MenuButton/MenuButtonText",
                "kwargs": {
                    "text": "Multiplayer"
                }
            }
        },
        "ExitButton": {
            "base_type": "/MainMenu/MenuButton",
            "kwargs": {
                "pos": [0.25, 0.6875],
                "game_object:children": [
                    "ExitText"
                ],
                "name": "exit_button"
            },
            "ExitText": {
                "base_type": "/MainMenu/MenuButton/MenuButtonText",
                "kwargs": {
                    "text": "Exit"
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
            }
        }
    },
    "PauseMenu": {
        "class_name": "PauseMenu",
        "kwargs": {
            "pos": [0.25, 0.25],
            "size": [0.5, 0.5],
            "game_object:children": [
                "ResumeButton",
                "ExitButton"
            ],
            "fix_aspect_ratio": False,
            "colour": [100, 100, 100, 128]
        },
        "ResumeButton": {
            "base_type": "/MainMenu/MenuButton",
            "kwargs": {
                "pos": [0.25, 0.2],
                "game_object:children": [
                    "ResumeText"
                ],
                "name": "resume_button"
            },
            "ResumeText": {
                "base_type": "/MainMenu/MenuButton/MenuButtonText",
                "kwargs": {
                    "text": "Resume Game"
                }
            }
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
                    "text": "Exit"
                }
            }
        },
    },
    "DebriefPanel": {
        "class_name": "DebriefPanel",
        "kwargs": {
            "pos": [0.25, 0.15],
            "size": [0.5, 0.7],
            "game_object:children": [
                "ContinueButton",
                "AsteroidRowPanel",
                "WaypointRowPanel",
                "FinalScorePanel"
            ],
            "fix_aspect_ratio": False,
            "colour": [100, 100, 100, 128],
            "game_object:asteroid_spawner": "/MainMenu/AsteroidSpawner"
        },
        "ContinueButton": {
            "class_name": "ColourPanel",
            "kwargs": {
                "pos": [0.25, 0.7],
                "size": [0.5, 0.15],
                "game_object:children": [
                    "ContinueText"
                ],
                "fix_aspect_ratio": False,
                "name": "continue_button",
                "colour": [200, 200, 200, 100],
                "hover_colour": [100, 210, 100, 100]
            },
            "ContinueText": {
                "class_name": "TextPanel",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                    "asset:font_asset": "fast_hand_font",
                    "text_colour": [0, 200, 100],
                    "horz_align": "CENTRE",
                    "vert_align": "CENTRE",
                    "text": "Continue"
                }
            }
        },
        "AsteroidRowPanel": {
            "base_type": "/DebriefPanel/DebriefRowPanel",
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
                "base_type": "/DebriefPanel/DebriefRowPanel/Spinner",
                "kwargs": {
                    "image:image_asset": "asteroid_04",
                    "angular_velocity": 45
                }
            },
            "Count": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Count",
                "kwargs": {
                    "game_object:children": [
                        "CountText"
                    ]
                },
                "CountText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
                    "kwargs": {
                        "name": "asteroid_count_text"
                    }
                }
            },
            "Multiplier": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Multiplier",
                "kwargs": {
                    "game_object:children": [
                        "MultiplierText"
                    ]
                },
                "MultiplierText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
                    "kwargs": {
                        "name": "asteroid_multiplier_text"
                    }
                }
            },
            "Total": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Total",
                "kwargs": {
                    "game_object:children": [
                        "TotalText"
                    ]
                },
                "TotalText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
                    "kwargs": {
                        "name": "asteroid_total_text"
                    }
                }
            }
        },
        "WaypointRowPanel": {
            "base_type": "/DebriefPanel/DebriefRowPanel",
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
                "base_type": "/DebriefPanel/DebriefRowPanel/Spinner",
                "kwargs": {
                    "image:image_asset": "waypoint",
                    "angular_velocity":-45
                }
            },
            "Count": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Count",
                "kwargs": {
                    "game_object:children": [
                        "CountText"
                    ]
                },
                "CountText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
                    "kwargs": {
                        "name": "waypoint_count_text"
                    }
                }
            },
            "Multiplier": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Multiplier",
                "kwargs": {
                    "game_object:children": [
                        "MultiplierText"
                    ]
                },
                "MultiplierText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
                    "kwargs": {
                        "name": "waypoint_multiplier_text"
                    }
                }
            },
            "Total": {
                "base_type": "/DebriefPanel/DebriefRowPanel/Total",
                "kwargs": {
                    "game_object:children": [
                        "TotalText"
                    ]
                },
                "TotalText": {
                    "base_type": "/DebriefPanel/DebriefRowPanel/RowText",
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
                "fix_aspect_ratio": False,
                "colour": [150, 150, 150, 100]
            },
            "Spinner": {
                "class_name": "Spinner",
                "kwargs": {
                    "pos": [0, 0.12],
                    "size": [0.1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                    "name": "spinner",
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
                    "colour": [0, 0, 0, 0]
                },
                "TotalTitleText": {
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
                    "colour": [0, 0, 0, 0]
                },
                "TotalText": {
                    "class_name": "TextPanel",
                    "kwargs": {
                        "pos": [0, 0],
                        "size": [1, 1],
                        "game_object:children": [],
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
        "DebriefRowPanel": {
            "class_name": "ColourPanel",
            "kwargs": {
                "size": [0.8, 0.1],
                "game_object:children": [],
                "fix_aspect_ratio": False,
                "name": "asteroid_row_panel",
                "colour": [150, 150, 150, 100]
            },
            "Spinner": {
                "class_name": "Spinner",
                "kwargs": {
                    "pos": [0, 0],
                    "size": [0.1, 1],
                    "game_object:children": [],
                    "fix_aspect_ratio": True,
                    "name": "spinner"
                }
            },
            "Count": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.1, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
                    "colour": [0, 0, 0, 0]
                }
            },
            "Multiplier": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.4, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
                    "colour": [0, 0, 0, 0]
                }
            },
            "Total": {
                "class_name": "ColourPanel",
                "kwargs": {
                    "pos": [0.7, 0],
                    "size": [0.3, 1],
                    "fix_aspect_ratio": False,
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
                }
            }
        }
    },
    "PlayerShip": {
        "class_name": "Ship",
        "kwargs": {
            "image:image_asset": "ship",
            "type_spec:projectile_type": "/PlayerShip/PlayerProjectile",
            "fire_freq": 200,
            "game_object:mover": "PlayerShipMover",
            "type_spec:death_effect": "/Explosions/ExplosionBig",
            "damage": 50,
            "game_object:waypoint": "Waypoint",
            "sound:shot_sound": "ship_shot"
        },
        "groups": [
            "RenderGroup",
            "PlayerGroup"
        ],
        "attachments": [
            {
                "game_type": "/PlayerShip/PlayerShield",
                "offset": [0.0, 0.0]
            },
            {
                "game_type": "/PlayerShip/NavArrow",
                "offset": [0, 0],
                "parent_transform": False
            },
            {
                "game_type": "/PlayerShip/PlayerHealthBar",
                "offset": [0, 0],
                "parent_transform": False
            }
        ],
        "PlayerShipMover": {
            "class_name": "MoverVelocity",
            "kwargs": {
                "velocity": 0.0,
                "velocity_decay_factor": 0.9,
                "max_velocity": 200.0,
                "angular_velocity": 1.5
            }
        },
        "PlayerHealthBar": {
            "class_name": "HealthBar",
            "kwargs": {
                "image:images": ["player_health_bar_bg", "player_health_bar_fg"],
                "heading": 90,
                "is_collidable": False
            },
            "groups": [
                "RenderGroup"
            ]
        },
        "PlayerShield": {
            "class_name": "Shield",
            "kwargs": {
                "image:images": ["shield3", "shield2", "shield1"],
                "damage": 50
            },
            "groups": [
                "RenderGroup",
                "PlayerGroup"
            ]
        },
        "NavArrow": {
            "class_name": "NavArrow",
            "kwargs": {
                "image:image_asset": "arrow"
            },
            "groups": [
                "RenderGroup"
            ]
        },
        "PlayerProjectile": {
            "class_name": "Projectile",
            "kwargs": {
                "image:image_asset": "player_projectile",
                "type_spec:death_effect": "/Explosions/ExplosionSmall",
                "damage": 15,
                "game_object:mover": "PlayerProjectileMover",
                "kill_when_off_screen": True
            },
            "groups": [
                "RenderGroup",
                "PlayerProjectilesGroup"
            ],
            "PlayerProjectileMover": {
                "class_name": "MoverVelocity",
                "kwargs": {
                    "velocity": 1200.0,
                    "velocity_decay_factor": 1.0,
                    "max_velocity": 800.0,
                    "angular_velocity": 0.0
                }
            }
        },
        "Waypoint": {
            "class_name": "Waypoint",
            "kwargs": {
                "image:image_asset": "waypoint",
                "type_spec:death_effect": "/Explosions/Explosion",
                "kill_when_off_screen": False,
                "distance": 1000,
                "angular_velocity": 60.0,
                "image:digit_image_assets": [
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9"
                ],
                "sound:enter_sound": "enter_sound"
            },
            "groups": [
                "RenderGroup",
                "TriggersGroup"
            ],
            "attachments": [
                {
                    "game_type": "/PlayerShip/Waypoint/LeftDigit",
                    "offset": [-10.0, 0.0]
                },
                {
                    "game_type": "/PlayerShip/Waypoint/RightDigit",
                    "offset": [10.0, 0.0]
                }
            ],
            "LeftDigit": {
                "class_name": "GameObject",
                "kwargs": {
                    "image:image_asset": "0",
                    "is_collidable": False
                },
                "groups": [
                    "RenderGroup"
                ]
            },
            "RightDigit": {
                "class_name": "GameObject",
                "kwargs": {
                    "image:image_asset": "1",
                    "is_collidable": False
                },
                "groups": [
                    "RenderGroup"
                ]
            }
        }
    },
    "Explosions": {
        "Explosion": {
            "class_name": "AnimatedTexture",
            "kwargs": {
                "asset:asset": "explosion_atlas",
                "duration": 750,
                "scale": 1
            },
            "groups": [
                "RenderGroup"
            ]
        },
        "ExplosionSmall": {
            "class_name": "AnimatedTexture",
            "kwargs": {
                "asset:asset": "explosion_small_atlas",
                "duration": 500,
                "scale": 0.8,
                "sound:sound": "explosion_small"
            },
            "groups": [
                "RenderGroup"
            ]
        },
        "ExplosionBig": {
            "class_name": "AnimatedTexture",
            "kwargs": {
                "asset:asset": "explosion_big_atlas",
                "duration": 1500,
                "scale": 1.5,
                "sound:sound": "explosion_large"
            },
            "groups": [
                "RenderGroup"
            ]
        }
    },
    "Level_02": {
        "class_name": "Level",
        "kwargs": {
            "game_object:player_spec": "PlayerSpec",
            "game_object:enemy_specs": [],
            "game_object:updatables": [
                "AsteroidSpawner"
            ]
        },
        "PlayerSpec": {
            "class_name": "LevelObject",
            "kwargs": {
                "type_spec:game_type": "/PlayerShip",
                "spawn_pos": [640, 360]
            }
        },
        "AsteroidSpawner": {
            "class_name": "AsteroidSpawner",
            "kwargs": {
                "type_spec:asteroid_types": [
                    # Ugly hack to reduce the number of times AsteroidMother is selected
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidBig",
                    "AsteroidMedium",
                    "AsteroidMother"
                ],
                "spawn_freq": 1000,
                "asset:render_group": "RenderGroup",
                "freq_accel_threshold": 20000
            }
        },
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
            "colour": [100, 100, 100, 100]
        },
        "ScoreText": {
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
                "text": "0000"
            }
        }
    },
    "TimePanel": {
        "class_name": "ColourPanel",
        "kwargs": {
            "pos": [0.88, 0],
            "size": [0.12, 0.06],
            "game_object:children": [
                "TimeText"
            ],
            "fix_aspect_ratio": True,
            "colour": [100, 100, 100, 100]
        },
        "TimeText": {
            "class_name": "TextPanel",
            "kwargs": {
                "pos": [0, 0],
                "size": [1, 1],
                "game_object:children": [],
                "fix_aspect_ratio": True,
                "asset:font_asset": "fast_hand_font",
                "text_colour": [0, 200, 100],
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "text": "00:00"
            }
        }
    },
    "AsteroidMother": {
        "base_type": "AsteroidBase",
        "kwargs": {
            "image:images": [
                "asteroid_00",
                "asteroid_01",
                "asteroid_02",
                "asteroid_03"
            ],
            "health": 40,
            "damage": 10,
            "type_spec:death_spawn": ["AsteroidSmall", "AsteroidMedium"],
            "score_on_die": 50
        },
        "attachments": [
            {
                "game_type": "/AsteroidMother/AsteroidTurret",
                "offset": [0, 0],
                "parent_transform": False
            }
        ],
        "AsteroidTurret": {
            "class_name": "Turret",
            "kwargs": {
                "image:image_asset": "turret",
                "type_spec:projectile_type": "/AsteroidMother/AsteroidTurret/AsteroidProjectile",
                "fire_freq": 1500,
                "health": 20,
                "type_spec:death_effect": "/Explosions/Explosion",
                "score_on_die": 20,
                "sound:shot_sound": "turret_shot"
            },
            "attachments": [
                {
                    "game_type": "/AsteroidMother/AsteroidTurret/AsteroidTurretGun",
                    "offset": [0.0, -15.0]
                }
            ],
            "groups": [
                "RenderGroup",
                "AsteroidTurretsGroup"
            ],
            "AsteroidTurretGun": {
                "class_name": "GameObject",
                "kwargs": {
                    "image:image_asset": "turret_gun",
                    "scale": 0.8,
                    "is_collidable": False
                },
                "groups": [
                    "RenderGroup"
                ]
            },
            "AsteroidProjectile": {
                "class_name": "Projectile",
                "kwargs": {
                    "image:image_asset": "turret_projectile",
                    "type_spec:death_effect": "/Explosions/ExplosionSmall",
                    "damage": 10,
                    "game_object:mover": "EnemyTurretProjectileMover",
                    "kill_when_off_screen": True
                },
                "groups": [
                    "RenderGroup",
                    "AsteroidProjectilesGroup"
                ],
                "EnemyTurretProjectileMover": {
                    "class_name": "MoverVelocity",
                    "kwargs": {
                        "velocity": 500.0,
                        "velocity_decay_factor": 1.0,
                        "max_velocity": 500.0,
                        "angular_velocity": 0.0
                    }
                }
            }
        }
    },
    "AsteroidBase": {
        "class_name": "Asteroid",
        "kwargs": {
            "type_spec:death_effect": "/Explosions/Explosion",
            "game_object:mover": "AsteroidMover",
            "type_spec:death_spawn": [],
            "kill_when_off_screen": True
        },
        "groups": [
            "RenderGroup",
            "AsteroidsGroup"
        ],
        "AsteroidMover": {
            "class_name": "MoverVelDir",
            "kwargs": {
                "velocity": 50.0,
                "direction": [0, 1]
            }
        }
    },
    "AsteroidBig": {
        "base_type": "AsteroidBase",
        "kwargs": {
            "image:images": [
                "asteroid_00",
                "asteroid_01",
                "asteroid_02",
                "asteroid_03"
            ],
            "health": 40,
            "damage": 10,
            "type_spec:death_spawn": ["AsteroidMedium", "AsteroidMedium"],
            "score_on_die": 30
        }
    },
    "AsteroidMedium": {
        "base_type": "AsteroidBase",
        "kwargs": {
            "image:images": [
                "asteroid_04",
                "asteroid_05"
            ],
            "health": 20,
            "damage": 5,
            "type_spec:death_spawn": ["AsteroidSmall", "AsteroidTiny"],
            "score_on_die": 20
        }
    },
    "AsteroidSmall": {
        "base_type": "AsteroidBase",
        "kwargs": {
            "image:images": [
                "asteroid_06",
                "asteroid_07"
            ],
            "health": 10,
            "damage": 2,
            "score_on_die": 10
        }
    },
    "AsteroidTiny": {
        "base_type": "AsteroidBase",
        "kwargs": {
            "image:images": [
                "asteroid_08"
            ],
            "health": 5,
            "type_spec:death_effect": "/Explosions/ExplosionSmall",
            "damage": 1,
            "score_on_die": 7
        }
    }
}
