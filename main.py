from sys import path
path.append("./GameEngine")

import pygame

from game_object import GameObject
from game_object_factory import GameObjectFactory
from render_group import RenderGroup
from shield import Shield
from ship import Ship
from turret import Turret


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

    GameObjectFactory.initialize(open("Assets/inventory.json"))

    # Create world
    pygame.display.set_icon(GameObjectFactory.surfaces["ship"])
    pygame.display.set_caption("Game")
    world_rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
    screen_rect = screen.get_rect()

    render_group = RenderGroup(world_rect, screen_rect, True)
    player_collision_group = pygame.sprite.Group()
    badies_collision_group = pygame.sprite.Group()

    # Create player
    player = GameObjectFactory.create("PlayerShip", enemies=badies_collision_group)
    player.set_pos(pygame.Vector2(screen_rect.width / 2.0, screen_rect.height / 2.0))
    linear_velocity = 200.0
    angular_velocity = 1.5

    render_group.set_target(player)
    player.add_to_groups([render_group, player_collision_group])

    # Create a turret
    turret = GameObjectFactory.create("EnemyTurret", enemies=player_collision_group)
    turret.set_pos(pygame.Vector2(screen_rect.width * 0.75, screen_rect.height * 0.75))
    turret.set_target(player)
    turret.add_to_groups([render_group, badies_collision_group])

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
                if event.key == pygame.K_SPACE:
                    player.fire()

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_s]:
            player.set_heading(player.heading + angular_velocity)
        if pressed_keys[pygame.K_f]:
            player.set_heading(player.heading - angular_velocity)
        if pressed_keys[pygame.K_e]:
            player.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_velocity(player.mover.velocity * 0.8)
#         if pressed_keys[pygame.K_SPACE]:
#             player.fire()

        # Update groups
        render_group.update(clock.get_time())

        # Render
        screen.fill(background)
        render_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
