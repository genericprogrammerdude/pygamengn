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
    "mechanical_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "mechanical-font/MechanicalBold-oOmA.otf",
            "size": 80
        }
    },
}


DEVELOP_AND_DEBUG = True

import photo_metadata
import images_dict

if DEVELOP_AND_DEBUG:
    image_load_count = 4
    image_index_start = 220
    photo_asset_names = [f"/Photo_{i + image_index_start:03}" for i in range(image_load_count)]
    images = {}
    for i in range(image_load_count):
        images[f"{i + image_index_start:03}"] = images_dict.images[f"{i + image_index_start:03}"]
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
            "game_object:year_panel": "/YearPanel",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": []
            }
        }
    },
    "PhotoSpawner": {
        "class_name": "PhotoSpawner",
        "kwargs": {
            "game_object:photos": photo_asset_names,
            "durations": {
                "flying_in": 2000,
                "on_display": 4000,
                "flying_out": 2000,
            }
        }
    },
    "YearPanel": {
        "class_name": "ColourPanel",
        "kwargs": {
            "pos": [0.5, 0.85],
            "size": [0.11, 0.07],
            "game_object:children": [
                "YearText"
            ],
            "fix_aspect_ratio": True,
            "colour": [100, 100, 100, 150],
            "border_radius": 0.3,
        },
        "YearText": {
            "class_name": "TextPanel",
            "kwargs": {
                "pos": [0, 0.08],
                "size": [1, 1],
                "game_object:children": [],
                "fix_aspect_ratio": True,
                "asset:font_asset": "mechanical_font",
                "text_colour": [255, 211, 0],
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "name": "year_text",
            }
        }
    },
}

if DEVELOP_AND_DEBUG:
    for i in range(image_load_count):
        game_types[
            f"Photo_{i + image_index_start:03}"
        ] = photo_metadata.photo_metadata_dictionary[f"Photo_{i + image_index_start:03}"]
else:
    game_types.update(photo_metadata.photo_metadata_dictionary)
