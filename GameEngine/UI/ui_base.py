from abc import abstractmethod

import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("UIBase")
class UIBase(GameObjectBase):
    """Base class for UI components."""

    def __init__(self, pos, size, children, fix_aspect_ratio):
        super().__init__()
        self.pos = pos
        self.size = size
        self.children = children
        self.fix_aspect_ratio = fix_aspect_ratio
        self.parent_rect = None
        self.rect = None
        self.image = None
        self.aspect_ratio = None

    def update(self, parent_rect, delta):
        """Updates the UI component and its children."""
        if parent_rect != self.parent_rect:
            self.resize_to_parent(parent_rect)
            self.parent_rect = parent_rect
            self.resize()

        for child in self.children:
            child.update(self.rect, delta)

    def resize_to_parent(self, parent_rect):
        """Resizes the component's rect to match size with its parent's rect."""
        width = parent_rect.width * self.size[0]
        height = parent_rect.height * self.size[1]
        if self.fix_aspect_ratio:
            if self.aspect_ratio is None:
                self.aspect_ratio = width / height
            if width / self.aspect_ratio > height:
                # Height is the limiting factor
                width = self.aspect_ratio * height
            elif height * self.aspect_ratio > width:
                # Width is the limiting factor
                height = width / self.aspect_ratio
        size = (round(width), round(height))
        pos = parent_rect.topleft + pygame.Vector2(parent_rect.width * self.pos[0], parent_rect.height * self.pos[1])
        self.rect = pygame.Rect(pos.x, pos.y, size[0], size[1])

    @abstractmethod
    def resize(self):
        """Called when the component resized its own rect to match its parent's rect."""
        pass
