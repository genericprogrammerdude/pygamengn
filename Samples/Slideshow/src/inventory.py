images = {
    "background": "SpaceShooterRedux/Backgrounds/darkPurple.png",
}

sounds = {
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
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": []
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
    "Slideshow": {
        "class_name": "Slideshow",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": []
            }
        }
    },
}
