import pygame


class CustomCursor:
    def __init__(
        self, cursor_surface: pygame.surface.Surface, hotspot: tuple[int, int] = (0, 0)
    ):
        self.cursor_surface = cursor_surface
        self.hotspot = hotspot
        self.cursor = pygame.cursors.Cursor(self.hotspot, self.cursor_surface)

    def getSurface(self):
        return pygame.transform.scale(self.cursor_surface, (50, 50))

    def getCursor(self):
        return self.cursor
