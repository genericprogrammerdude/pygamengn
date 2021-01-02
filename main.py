import random
import sys

import pygame

sys.path.append("./GameEngine")

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

    if len(sys.argv) > 1:
        GameObjectFactory.initialize(open(sys.argv[1]))
    else:
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

    # Create a turret
    turrets = [GameObjectFactory.create("EnemyTurret", enemies=player_collision_group) for i in range(3)]
    for turret in turrets:
        turret.set_pos(pygame.Vector2(random.randint(0, screen_rect.width), random.randint(0, screen_rect.height)))
        turret.set_target(player)
        turret.add_to_groups([render_group, badies_collision_group])
    
    turret2 = [GameObjectFactory.create("EnemyTurret2", enemies=player_collision_group) for i in range(2)]
    for turret in turret2:
        turret.set_pos(pygame.Vector2(random.randint(0, screen_rect.width), random.randint(0, screen_rect.height)))
        turret.set_target(player)
        turret.add_to_groups([render_group, badies_collision_group])
        
    render_group.set_target(player)
    player.add_to_groups([render_group, player_collision_group])

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
        if pressed_keys[pygame.K_a]:
            player.set_heading(player.heading + player.mover.angular_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_heading(player.heading - player.mover.angular_velocity)
        if pressed_keys[pygame.K_w]:
            player.set_velocity(player.mover.max_velocity)
        if pressed_keys[pygame.K_s]:
            player.set_velocity(player.mover.velocity * 0.8)

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
