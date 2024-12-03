game_types = {
    "AsteroidShooterGame": {
        "class_name": "AsteroidShooterGame",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:main_menu_ui": "/MainMenu",
            "game_object:pause_menu_ui": "/PauseMenu",
            "game_object:debrief_ui": "/DebriefUI",
            "game_object:hud_ui": "/Hud",
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
                "velocity_decay_ms": 2000,
                "max_velocity": 250.0,
                "angular_velocity": 120,
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
            "score_on_die": 50,
            "max_angular_velocity": 30,
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
            "kill_when_off_screen": True,
            "off_screen_ttl": 2000,
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
            "score_on_die": 30,
            "max_angular_velocity": 60,
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
            "score_on_die": 20,
            "max_angular_velocity": 80,
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
            "score_on_die": 10,
            "max_angular_velocity": 100,
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
            "score_on_die": 7,
            "max_angular_velocity": 120,
        }
    }
}