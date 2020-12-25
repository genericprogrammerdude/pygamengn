import sys

import pygame


def main():
    try:
        from game_object import GameObject
    except ModuleNotFoundError:
        from sys import path
        path.append(r"./GameEngine")
        from game_object import GameObject

    pygame.init()

    size = width, height = 640, 480
    move_delta = [0, 0]
    speed = 2
    background = 50, 50, 50

    screen = pygame.display.set_mode(size)

    ball = GameObject("Assets/intro_ball.gif")

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
        move_delta = [0, 0]
        if pressed_keys[pygame.K_s]:
            move_delta[0] -= speed
        if pressed_keys[pygame.K_f]:
            move_delta[0] += speed
        if pressed_keys[pygame.K_e]:
            move_delta[1] -= speed
        if pressed_keys[pygame.K_d]:
            move_delta[1] += speed

        # Prevent player from exiting the screen
        if (ball.rect.left < 0 and move_delta[0] < 0) or (ball.rect.right > width and move_delta[0] > 0):
            move_delta[0] = 0
        if (ball.rect.top < 0 and move_delta[1] < 0) or (ball.rect.bottom > height and move_delta[1] > 0):
            move_delta[1] = 0

        # Move the player
        ball.rect.x = ball.rect.x + move_delta[0]
        ball.rect.y = ball.rect.y + move_delta[1]

        # Render
        screen.fill(background)
        GameObject.game_objects.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
