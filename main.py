import pygame


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50

    screen = pygame.display.set_mode(size)

    ball = GameObject("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png")
    ball.set_pos((screen.get_rect().width / 2, screen.get_rect().height / 2))
    ball.set_scale(0.8)
    linear_velocity = 150.0
    angular_velocity = 1.5

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
            ball.set_angle(ball.angle + angular_velocity)
        if pressed_keys[pygame.K_f]:
            ball.set_angle(ball.angle - angular_velocity)
        if pressed_keys[pygame.K_e]:
            ball.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            ball.set_velocity(-linear_velocity)

        # Render
        screen.fill(background)
        GameObject.game_objects.update(clock.get_time())
        GameObject.game_objects.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    from sys import path
    path.append(r"./GameEngine")
    from game_object import GameObject

    main()
