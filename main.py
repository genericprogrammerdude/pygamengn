import pygame


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

    # Load all the stuffs
    explosion_atlas_image = pygame.image.load("Assets/Explosions/explosion1.png").convert_alpha()
    ship_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha()
    shield_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield1.png").convert_alpha()
    turret_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/turretBase_big.png").convert_alpha()
    turret_gun_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/gun04.png").convert_alpha()
    projectile_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Lasers/laserRed06.png").convert_alpha()

    # Create world
    pygame.display.set_icon(ship_image)
    pygame.display.set_caption("Game")
    world_rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
    screen_rect = screen.get_rect()

    # Create player
    explosion_atlas = Atlas(explosion_atlas_image, (256, 256))
    player = Ship(ship_image, explosion_atlas, 0.5)
    player.set_pos(pygame.Vector2(screen_rect.width / 2.0, screen_rect.height / 2.0))
    player.set_scale(0.8)
    linear_velocity = 200.0
    angular_velocity = 1.5

    # Create a turret
    turret = Turret(turret_image, projectile_image)
    turret.set_scale(1.25)
    turret.set_pos(pygame.Vector2(screen_rect.width * 0.75, screen_rect.height * 0.75))
    turret.set_target(player)

    # Add player and turret to group of game objects
    game_objects = CameraAwareGroup(player, world_rect, screen_rect, True)
    game_objects.add(turret)
    game_objects.move_to_back(turret)

    # Attach shield to player
    shield = GameObject(shield_image)
    shield.transform()
    player.attach(shield, (0, 0))

    # Attach gun to turret
    turret_gun = GameObject(turret_gun_image)
    turret.attach(turret_gun, (0, -15))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_s]:
            player.set_heading(player.heading + angular_velocity)
        if pressed_keys[pygame.K_f]:
            player.set_heading(player.heading - angular_velocity)
        if pressed_keys[pygame.K_e]:
            player.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_velocity(player.velocity * 0.8)

        # Update groups
        game_objects.update(clock.get_time())

        # Render
        screen.fill(background)
        game_objects.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    from sys import path
    path.append(r"./GameEngine")
    from ship import Ship
    from camera_aware_group import CameraAwareGroup
    from turret import Turret
    from atlas import Atlas
    from game_object import GameObject

    main()
