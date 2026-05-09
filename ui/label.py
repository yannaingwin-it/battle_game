from typing import Any

import pygame


class Label:
    """
    A graphical Label for Pygame.

    Attributes:
        text (str): button text.
        x (int): x position.
        y (int): y position.
        font (pygame.font.Font): font.
        color (str): text color.

    Example:
        >>> initialize Label
        >>> label = Label( "label_name : ", 100, 100, pygame.font.Font(None, 20), "black", )
        >>> # Inside your main loop:
        >>> while running:
        >>>     label.draw(window)
    """

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        font: pygame.font.Font,
        color="black",
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.__width = 0

    def draw(self, window: pygame.Surface):

        # Render the text into a surface
        text_surface = self.font.render(self.text, True, self.color)
        self.__width = text_surface.get_width()
        # Draw it to the screen
        window.blit(text_surface, (self.x, self.y))

    def getWidth(self):
        return self.__width

    def setText(self, newText: str):
        self.text = newText


###################################################################

if __name__ == "__main__":
    pygame.init()
    # Main loop
    running = True
    window = pygame.display.set_mode((640, 480))

    # 1. Create Label
    username_label = Label(
        "username : ",
        100,
        100,
        pygame.font.Font(None, 20),
        "black",
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
        # 2. draw label
        username_label.draw(window)

        ############################################################
        pygame.display.update()

    pygame.quit()
