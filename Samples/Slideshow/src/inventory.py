assets = {
    "RenderGroup": {
        "class_name": "RenderGroup",
        "kwargs": {
        }
    },
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": [
                ["Photo"],
            ]
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


DEVELOP_AND_DEBUG = True

import photo_metadata
import images_dict

if DEVELOP_AND_DEBUG:
    image_load_count = 3
    photo_asset_names = [f"/Photo_{i:03}" for i in range(image_load_count)]
    images = {}
    for i in range(image_load_count):
        images[f"{i:03}"] = images_dict.images[f"{i:03}"]
else:
    photo_asset_names = photo_metadata.photo_asset_names
    images = images_dict.images

game_types = {
    "Slideshow": {
        "class_name": "Slideshow",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:photo_spawner": "/PhotoSpawner",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": [
                ]
            }
        }
    },
    "PhotoSpawner": {
        "class_name": "PhotoSpawner",
        "kwargs": {
            "spawn_freq": 10000,
            "photo_time": 7500,
            "game_object:photos": photo_asset_names,
        }
    },
}

if DEVELOP_AND_DEBUG:
    for i in range(image_load_count):
        game_types[f"Photo_{i:03}"] = photo_metadata.photo_metadata_dictionary[f"Photo_{i:03}"]
else:
    game_types.update(photo_metadata.photo_metadata_dictionary)
