import pygame


class InputBox:
    """
    A graphical text input box for Pygame.

    Attributes:
        text (str): The current string content.

    Example:
        >>> initialize input box
        >>> inputBox = InputBox("", pygame.Rect(100, 100, 140, 32), font, "black", "red", "lightblue")
        >>> # Inside your main loop:
        >>> while running:
        >>>     events = pygame.event.get()
        >>>     inputBox.draw(window)
        >>>     if inputBox.onchange(events):
        >>>         print(inputBox.text)
    """

    isActive = False
    isChange = False

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        textColor: str,
        color: str,
        activeColor: str,
    ):

        self.text = text
        self.rect = rect
        self.font = font
        self.textColor = textColor
        self.color = color
        self.activeColor = activeColor
        self.__cursor_visible = True
        self.__last_blink = pygame.time.get_ticks()
        pass

    def onchange(self, events: list[pygame.event.Event]):
        """
        Example:
        >>> events = pygame.event.get()
        >>> inputBox.draw(window)
        >>> if inputBox.handleInput(events):
        >>>     print(inputBox.text)
        >>> <or>
        >>> if inputBox.draw(window).onchange(events):
        >>>    print(inputBox.text)
        """
        self.isChange = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 1:
            if self.rect.collidepoint(mouse_pos):
                self.isActive = True
                # Change cursor shape
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:
                self.isActive = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # 2. Handle Typing (Requires Events for single-press)
        for event in events:
            if event.type == pygame.KEYDOWN and self.isActive:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove last char

                elif event.key == pygame.K_RETURN:
                    print("Final Input self.text :", self.text)
                    self.text = ""  # Clear after enter

                else:
                    # Add the character typed
                    self.text += event.unicode

                self.isChange = True
        return self.isChange

    # draw
    def draw(
        self,
        window: pygame.Surface,
    ):

        # Change color if active
        draw_color = self.activeColor if self.isActive else self.color

        pygame.draw.rect(window, draw_color, self.rect, 1)

        # Render the text
        text_surface = self.font.render(self.text, True, "black")
        window.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        if self.isActive:
            current_time = pygame.time.get_ticks()
            # Toggle cursor every 500 milliseconds
            if current_time - self.__last_blink > 500:
                self.__cursor_visible = not self.__cursor_visible
                self.__last_blink = current_time

            if self.__cursor_visible:
                # Calculate cursor position (start of box + padding + text width)
                cursor_x = self.rect.x + 5 + text_surface.get_width()
                cursor_y = self.rect.y + 5
                # Draw a simple vertical line |
                pygame.draw.line(
                    window,
                    self.textColor,
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + self.rect.height - 10),
                    2,
                )

        # Auto-resize the box if text is too long
        self.rect.w = max(self.rect.w, text_surface.get_width() + 10)
        return self


###################################################################

if __name__ == "__main__":
    pygame.init()
    # Main loop
    running = True
    window = pygame.display.set_mode((640, 480))

    # Create Input Box and font

    # 1. Create Input Box
    inputBox = InputBox(
        "",
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
        # 2. draw and Handle Input
        inputBox.draw(window)
        # 3. listen onchnage event
        if inputBox.onchange(events):  # the return value is true if input is changed
            print("Input Change", inputBox.text)
            pass

        ############################################################
        pygame.display.update()

    pygame.quit()
