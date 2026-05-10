import pygame


class HPBar:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        maxHp: int,
        currentHp: int,
        font: pygame.font.Font,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.maxHp = maxHp
        self.currentHp = currentHp

    def draw(
        self,
        window: pygame.Surface,
    ):

        # calc fill ratio
        ratio = max(0, self.currentHp / self.maxHp)

        # background (empty bar)
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, "darkred", bg_rect)

        # fill (current hp)
        fill_rect = pygame.Rect(self.x, self.y, int(self.width * ratio), self.height)

        # color changes based on HP
        if ratio > 0.5:
            color = "limegreen"
        elif ratio > 0.25:
            color = "orange"
        else:
            color = "red"

        pygame.draw.rect(window, color, fill_rect)

        # border
        pygame.draw.rect(window, "black", bg_rect, 2)

        # HP text centered on bar
        text = f"{int(self.currentHp)} / {self.maxHp}"
        text_surf = self.font.render(text, True, "white")
        text_rect = text_surf.get_rect(center=bg_rect.center)
        window.blit(text_surf, text_rect)


###################################################################


def _demo():
    pygame.init()
    # Main loop
    running = True
    window = pygame.display.set_mode((640, 480))

    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # 1. Create Button
    hpBar = HPBar(
        x=100,
        y=200,
        width=150,
        height=20,
        maxHp=200,
        currentHp=100,
        font=pygame.font.Font(None, 20),
    )

    clock = pygame.time.Clock()
    while running:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if hpBar.currentHp < 100:
                    hpBar.currentHp += 10
                else:
                    hpBar.currentHp -= 10
        window.fill("white")
        ############################################################
        # 2. draw buttton
        hpBar.draw(window)
        # if hpBar.currentHp <= 0:
        #     pygame.time.set_timer(pygame.USEREVENT, 0)
        ############################################################
        pygame.display.update()

    pygame.quit()


### what should i write in there
if __name__ == "__main__":
    _demo()
