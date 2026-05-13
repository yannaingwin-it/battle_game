import pygame

from ui.label import Label


class GameLog:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 18)
        self.messages = []
        self._scrollY = 0
        self.lineHeight = 22
        self.padding = 8
        self.label = Label(
            "Game Log",
            self.x + self.padding,
            self.y + self.padding,
            pygame.font.SysFont(None, 30),
            "black",
        )

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def addMessage(self, message: str):
        # wrap long text into multiple lines
        words = message.split(" ")
        line = ""
        for word in words:
            test = line + word + " "
            if self.font.size(test)[0] > self.width - self.padding * 2:
                self.messages.append(line)
                line = word + " "
            else:
                line = test
        self.messages.append(line)

        # auto scroll to bottom
        total = len(self.messages) * self.lineHeight
        if total > self.height - self.padding * 2:
            self._scrollY = total - (self.height - self.padding * 2)

    def handleEvent(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if (
                self.getRect().collidepoint(mouse_pos)
                and event.type == pygame.MOUSEWHEEL
            ):
                self._scrollY -= event.y * 15
                self._scrollY = max(0, self._scrollY)

    def draw(self, window: pygame.Surface):
        # background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(window, "white", bg_rect)
        pygame.draw.rect(window, "black", bg_rect, 2)
        self.label.draw(window)
        divider_rect = pygame.Rect(
            self.label.x, self.y + 33, self.width - self.padding * 2, 1
        )
        pygame.draw.rect(window, "black", divider_rect, 2)
        # clip so text doesnt go outside box
        clip = window.subsurface(bg_rect.inflate(-2, -2))

        # draw messages
        for i, msg in enumerate(self.messages):
            y = self.padding + i * self.lineHeight - self._scrollY + divider_rect.y
            if -self.lineHeight < y < self.height:
                text_surf = self.font.render(msg, True, "black")
                clip.blit(text_surf, (self.padding, y))


if __name__ == "__main__":
    import pygame
    from game_log import GameLog

    pygame.init()
    window = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("GameLog Demo")

    font = pygame.font.SysFont("Arial", 12)
    log = GameLog(x=20, y=20, width=240, height=400)

    log.addMessage("[Game Message] Shawn attacked AI89 with damage 54: +63EXP")
    log.addMessage("[Game Message] AI32 attacked John with damage 14: +14EXP")

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        window.fill("lightgray")

        # test add message on spacebar
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    log.addMessage("[Game Message] New attack happened!")

        log.handleEvent(events)
        log.draw(window)

        pygame.display.update()

    pygame.quit()
