import pygame


class Button:
    """
    A graphical Button for Pygame.

    Attributes:
        text (str): button text.

    Example:
        >>> initialize Button
        >>> btn = Button( "Submit", pygame.Rect(100, 100, 110, 32), pygame.font.Font(None, 32), "black", "red", "lightblue",)
        >>> # Inside your main loop:
        >>> while running:
        >>>     events = pygame.event.get()
        >>>     btn.draw(window, events)
        >>>     if btn.onclick(events):
        >>>         print("Clicked!")
    """

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        color: str,
        hover_color: str,
        text_color="white",
    ):
        self.text = text
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_color = text_color
        self.clicked = False

    def draw(self, window: pygame.Surface, events: list[pygame.event.Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Default color
        current_color = self.color

        # Change color on hover
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current_color = self.color

        # Draw button body
        pygame.draw.rect(window, current_color, self.rect)
        # Draw button border (optional)
        pygame.draw.rect(window, "black", self.rect, 2)

        # Render and center text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)
        return self

    def onclick(self, events: list[pygame.event.Event]):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False


###################################################################

if __name__ == "__main__":
    pygame.init()
    # Main loop
    running = True
    window = pygame.display.set_mode((640, 480))

    # 1. Create Button
    btn = Button(
        "Submit",
        pygame.Rect(100, 100, 110, 32),
        pygame.font.Font(None, 32),
        "black",
        "red",
        "lightblue",
    )

    clock = pygame.time.Clock()
    while running:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        window.fill("white")
        ############################################################
        # 2. draw buttton
        btn.draw(window, events)
        # 3. listen click event
        if btn.onclick(events):
            print("clicked")

        ############################################################
        pygame.display.update()

    pygame.quit()
