import pygame


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50

    # Create world
    screen = pygame.display.set_mode(size)
    world_rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
    screen_rect = pygame.Rect(0, 0, size[0], size[1])

    # Create player
    player = GameObject("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png")
    player.set_pos((screen.get_rect().width / 2, screen.get_rect().height / 2))
    player.set_scale(0.8)
    linear_velocity = 150.0
    angular_velocity = 1.5

    # Add player to group of game objects
    game_objects = CameraAwareGroup(player, world_rect, screen_rect, True)

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
            player.set_angle(player.angle + angular_velocity)
        if pressed_keys[pygame.K_f]:
            player.set_angle(player.angle - angular_velocity)
        if pressed_keys[pygame.K_e]:
            player.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_velocity(-linear_velocity)

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
    from game_object import GameObject
    from camera_aware_group import CameraAwareGroup

    main()
