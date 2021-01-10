import sys

import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("CollisionManager")
class CollisionManager(GameObjectBase):
    """Manages collision detection and response."""

    def __init__(self, collision_checks):
        self.collision_checks = collision_checks

    def do_collisions(self):
        for collision_check in self.collision_checks:
            self.collide_groups(*collision_check)

    def collide_groups(self, group_a, group_b):
        collisions = pygame.sprite.groupcollide(group_a, group_b, False, False, self.collided)
        for gob_a in collisions.keys():
            for gob_b in collisions[gob_a]:
                if gob_a.alive() and gob_b.alive():
                    if not self.has_mask(gob_a) or not self.has_mask(gob_b):
                        continue
                    collision = pygame.sprite.collide_mask(gob_a, gob_b)
                    if collision:
                        # Get world position of collision point for colliding GameObjects to know
                        world_pos = pygame.Vector2(gob_a.rect.topleft) + collision
                        gob_b.handle_collision(gob_a, world_pos)
                        gob_a.handle_collision(gob_b, world_pos)

    def collided(self, a, b):
        """Checks whether sprites a and b collide."""
        if (a.parent and a.parent == b) or (b.parent and b.parent == a):
            return False
        if not (a.is_collidable and b.is_collidable):
            sys.stderr.write("CollisionManager.collided(): {0} or {1} has is_collidable == False and is in a collision group.\n".format(a, b))
            return False
        if a == b:
            sys.stderr.write("CollisionManager.collided(): Same object. {0} or {1}.\n".format(a, b))
            return False
        return pygame.sprite.collide_rect(a, b)

    def has_mask(self, gob):
        """Checks whether game object gob has a collision mask. Returns True if it does, False otherwise."""
        if gob.mask is None:
            sys.stderr.write("CollisionManager.has_mask(): Missing mask: {0}\n".format(gob))
            return False
        return True
