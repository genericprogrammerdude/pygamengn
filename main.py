import pygame


class GameObject(pygame.sprite.Sprite):
    """Basic game object."""

    game_objects = pygame.sprite.Group()

    def __init__(self, image_fname):
        super().__init__()

        # Set the image to use for this sprite.
        self.image = pygame.image.load(image_fname)
        self.rect = self.image.get_rect()

        # Add to group of game objects
        GameObject.game_objects.add(self)


def main():
    pygame.init()

    size = width, height = 640, 480
    move_delta = [0, 0]
    speed = 2
    background = 50, 50, 50

    screen = pygame.display.set_mode(size)

    ball = GameObject("intro_ball.gif")
    ballrect = ball.rect

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
        if (ballrect.left < 0 and move_delta[0] < 0) or (ballrect.right > width and move_delta[0] > 0):
            move_delta[0] = 0
        if (ballrect.top < 0 and move_delta[1] < 0) or (ballrect.bottom > height and move_delta[1] > 0):
            move_delta[1] = 0

        # Move the player
        ballrect.x = ballrect.x + move_delta[0]
        ballrect.y = ballrect.y + move_delta[1]

        # Render
        screen.fill(background)
        GameObject.game_objects.draw(screen)
#         screen.blit(ball.image, ball.rect)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
