import pygame

from .ui_type import ColorValue, Variant


class Button:
    """
    A graphical Button for Pygame.

    Attributes:
        text (str): button text.
        variant (Variant): Literal["default", "outlined", "filled", "text"]

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
        color: ColorValue,
        hover_color: ColorValue,
        text_color: ColorValue = "white",
        radius=-1,
        variant: Variant = "default",
    ):
        self.text = text
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_color = text_color
        self.clicked = False
        self.radius = radius
        self.variant = variant
        self.click_sound = pygame.mixer.Sound("click.wav")

    def draw(self, window: pygame.Surface, events: list[pygame.event.Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Default color
        current_color = self.color
        current_text_color = self.text_color
        # Change color on hover
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current_color = self.color
                    current_text_color = "white"

        # Draw button body
        if self.variant == "default" or self.variant == "filled":
            pygame.draw.rect(
                window,
                current_color,
                self.rect,
                border_radius=self.radius,
            )
        elif self.variant == "outlined":
            pygame.draw.rect(
                window,
                current_color,
                self.rect,
                1,
                border_radius=self.radius,
            )
        elif self.variant == "text":
            pass

        # Render and center text
        text_surf = self.font.render(self.text, True, current_text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)
        return self

    def onclick(self, events: list[pygame.event.Event]):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click_sound.play()
                    return True
        return False


###################################################################


def _demo():
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
        radius=8,
        variant="filled",
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
            btn.color = "green"

        ############################################################
        pygame.display.update()

    pygame.quit()


### what should i write in there
if __name__ == "__main__":
    _demo()
