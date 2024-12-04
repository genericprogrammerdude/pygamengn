images = {
    "ship": "SpaceShooterRedux/PNG/playerShip2_blue.png",
    "ship_icon": "../../favicon.png",
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
    "joystick": "joystick.png",
    "ship-alpha": "ship-alpha.png",
    "red-button": "red-button.png",
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
    "explosion_small": "Explosions/Explosion1.ogg",
    "explosion_large": "Explosions/Explosion5.ogg",
    "enter_sound": "SpaceShooterRedux/Bonus/sfx_shieldUp.ogg"
}

fonts = {
    "fast_hand": "fast-hand-font/FastHand-lgBMV.ttf",
}

assets = {
    "RenderGroup": {
        "class_name": "RenderGroup",
        "kwargs": {
            "grid_draw": False,
            "grid_colour": [100, 100, 100],
            "grid_interval": 100,
            "image:background": "background",
            "target_follow_tightness": 0.1,
        },
    },
    "PlayerGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
    },
    "PlayerProjectilesGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
    },
    "AsteroidsGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
    },
    "AsteroidProjectilesGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
    },
    "AsteroidTurretsGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
    },
    "TriggersGroup": {
        "class_name": "SpriteGroup",
        "kwargs": {},
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
            ],
        },
    },
    "explosion_small_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion1"],
            "frame_size": [256, 256],
            "scale": 0.8,
        },
    },
    "explosion_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion2", "explosion3", "explosion4"],
            "frame_size": [256, 256],
        },
    },
    "explosion_big_atlas": {
        "class_name": "Atlas",
        "kwargs": {
            "image:images": ["explosion3", "explosion4"],
            "frame_size": [256, 256],
            "scale": 1.5,
        },
    },
    "fast_hand_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "fast-hand-font/FastHand-lgBMV.ttf",
            "size": 51,
        },
    },
}

import inventory.gameplay_types
import inventory.main_menu
import inventory.pause_menu
import inventory.debrief_ui
import inventory.hud
game_types = (
    inventory.gameplay_types.game_types |
    inventory.main_menu.game_types |
    inventory.pause_menu.game_types |
    inventory.debrief_ui.game_types |
    inventory.hud.game_types
)
