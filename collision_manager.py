import pygame


class CollisionManager:
    """Manages collision detection and response."""

    def __init__(self, player, player_projectiles, turrets, turret_projectiles, asteroids):
        self.player = player
        self.player_projectiles = player_projectiles
        self.turrets = turrets
        self.turret_projectiles = turret_projectiles
        self.asteroids = asteroids

        self.collision_checks = [
            [self.player_projectiles, self.asteroids],
            [self.player_projectiles, self.turrets],
            [self.turret_projectiles, self.player],
            [self.turret_projectiles, self.asteroids],
            [self.asteroids, self.player]
        ]

    def do_collisions(self):
        for collision_check in self.collision_checks:
            self.collide_groups(*collision_check)

    def collide_groups(self, group_a, group_b):
        collisions = pygame.sprite.groupcollide(group_a, group_b, False, False, self.collided)
        for gob_a in collisions.keys():
            for gob_b in collisions[gob_a]:
                collision = pygame.sprite.collide_mask(gob_a, gob_b)
                if collision:
                    # Get world position of collision point for colliding GameObjects to know
                    world_pos = pygame.Vector2(gob_a.rect.topleft) + collision
                    gob_b.handle_collision(gob_a, world_pos)
                    gob_a.handle_collision(gob_b, world_pos)

    def collided(self, a, b):
        """Checks whether sprites a and b collide."""
        if a == b:
            return False
        if not (a.is_collidable and b.is_collidable):
            print(a, "or", b, "has is_collidable == False and it's in a collision group.")
            return False
        if (a.parent and a.parent == b) or (b.parent and b.parent == a):
            return False
        return pygame.sprite.collide_rect(a, b)
