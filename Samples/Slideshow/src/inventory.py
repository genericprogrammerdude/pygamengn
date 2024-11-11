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
            "size": 72
        }
    },
    "info_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "mechanical-font/Mechanical-g5Y5.otf",
            "size": 24
        }
    },
}


DEVELOP_AND_DEBUG = True

import photo_metadata
import images_dict

if DEVELOP_AND_DEBUG:
    image_load_count = 10
    image_index_start = 80
    photo_asset_names = [f"/Photo_{i + image_index_start:03}" for i in range(image_load_count)]
    images = {}
    for i in range(image_load_count):
        images[f"{i + image_index_start:03}"] = images_dict.images[f"{i + image_index_start:03}"]
else:
    photo_asset_names = photo_metadata.photo_asset_names
    images = images_dict.images
    image_load_count = len(images)
    image_index_start = 0

flying_in_time = 3000
on_display_time = 45000
flying_out_time = 2000

game_types = {
    "Slideshow": {
        "class_name": "Slideshow",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:photo_spawner": "/PhotoSpawner",
            "game_object:year_panel": "/YearPanel",
            "game_object:bar_panel": "/BarPanel",
            "game_object:photo_info_panel": "/PhotoInfoPanel",
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
                "flying_in": flying_in_time,
                "on_display": on_display_time,
                "flying_out": flying_out_time,
            }
        }
    },
    "YearPanel": {
        "class_name": "ColourPanel",
        "kwargs": {
            "pos": [0, 0.87],
            "size": [0.11, 0.05],
            "game_object:children": [
                "YearText",
            ],
            "fix_aspect_ratio": True,
            "colour": [100, 100, 100, 150],
            "game_object:corner_radii": "corner_radii",
            "name": "year_panel",
        },
        "corner_radii": {
            "class_name": "CornerRadii",
            "kwargs": {
                "top_left": 1,
                "top_right": 1,
                "bottom_right": 0,
                "bottom_left": 0,
            },
        },
        "YearText": {
            "class_name": "TextPanel",
            "kwargs": {
                "pos": [0.02, 0.1],
                "size": [1, 1],
                "game_object:children": [],
                "fix_aspect_ratio": True,
                "asset:font_asset": "mechanical_font",
                "text_colour": [255, 211, 0],
                "name": "year_text",
                "horz_align": "CENTRE",
                "vert_align": "CENTRE",
                "shadow": True,
                "shadow_colour": [50, 40, 0],
            },
        },
    },
    "BarPanel": {
        "class_name": "ColourPanel",
        "kwargs": {
            "pos": [0, 0.92],
            "size": [1, 0.015],
            "game_object:children": [],
            "fix_aspect_ratio": True,
            "colour": [100, 100, 100, 150],
            "name": "bar_panel",
        },
    },
    "PhotoInfoPanel": {
        "class_name": "ColourPanel",
        "kwargs": {
            "pos": [0, 0],
            "size": [0.2, 0.13],
            "game_object:children": [
                "PhotoNameText",
                "PhotoDateText",
                "PhotoFocalPointText",
                "PhotoScaleText",
            ],
            "fix_aspect_ratio": True,
            "colour": [100, 100, 100, 150],
            "name": "photo_info_panel",
        },
        "PhotoNameText": {
            "base_type": "/PhotoInfoPanel/PhotoInfoText",
            "kwargs": {
                "pos": [0.02, 0.02],
                "name": "photo_name_text",
                "text": "Name:",
            },
        },
        "PhotoDateText": {
            "base_type": "/PhotoInfoPanel/PhotoInfoText",
            "kwargs": {
                "pos": [0.02, 0.27],
                "name": "photo_date_text",
                "text": "Date:",
            },
        },
        "PhotoFocalPointText": {
            "base_type": "/PhotoInfoPanel/PhotoInfoText",
            "kwargs": {
                "pos": [0.02, 0.52],
                "name": "photo_focal_point_text",
                "text": "Focal point:",
            },
        },
        "PhotoScaleText": {
            "base_type": "/PhotoInfoPanel/PhotoInfoText",
            "kwargs": {
                "pos": [0.02, 0.77],
                "name": "photo_scale_text",
                "text": "Scale:",
            },
        },
        "PhotoInfoText": {
            "class_name": "TextPanel",
            "kwargs": {
                "size": [1, 0.25],
                "game_object:children": [],
                "fix_aspect_ratio": True,
                "asset:font_asset": "info_font",
                "text_colour": [255, 211, 0],
            },
        },
    },
}

if DEVELOP_AND_DEBUG:
    for i in range(image_load_count):
        game_types[
            f"Photo_{i + image_index_start:03}"
        ] = photo_metadata.photo_metadata_dictionary[f"Photo_{i + image_index_start:03}"]
else:
    game_types.update(photo_metadata.photo_metadata_dictionary)
