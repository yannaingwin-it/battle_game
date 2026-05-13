from typing import Literal, TypeAlias
import pygame

from ui.hp_bar import HPBar
from ui.label import Label

Job: TypeAlias = Literal["Warrior", "Tanker"]


class Charactor:
    __img_size = 100

    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        job: Job,
        level: int,
        hp: int,
        atk: int,
        defe: int,
        exp: int,
        is_alive: bool,
        is_player: bool,
    ):
        self.name = name
        self.job = job
        self.level = level
        self.atk = atk
        self.defe = defe
        self.exp = exp
        self.is_alive = is_alive
        self.is_player = is_player
        self.x = x
        self.y = y

        self.hpBar = HPBar(
            x=x,
            y=y,
            width=100,
            height=20,
            maxHp=hp,
            currentHp=hp,
            font=pygame.font.Font(None, 20),
        )

        warrior_img = pygame.image.load("warrior.png")
        tanker_img = pygame.image.load("tanker.png")

        self.char_img = warrior_img if self.job == "Warrior" else tanker_img
        self.char_surface = pygame.transform.scale(
            self.char_img, (self.__img_size, self.__img_size)
        )
        if not self.is_player:
            self.char_surface = pygame.transform.flip(self.char_surface, True, False)

        self.char_surface_rect = self.char_surface.get_rect()

        self.label = Label(
            f"level {self.level} : {self.name}",
            self.hpBar.x,
            self.hpBar.y,
            pygame.font.Font(None, 20),
            "white",
        )

    def setCurrentHp(self, hp: int):
        if hp > self.hpBar.maxHp:
            hp = self.hpBar.maxHp
        self.hpBar.currentHp = hp

    def _getCharSurfaceRect(self):
        return self.char_surface_rect

    def _setCharSurfaceRact(self, char_rect: pygame.Rect):
        self.char_surface_rect = char_rect

    def draw(
        self,
        window: pygame.Surface,
    ):

        char_rect = window.blit(self.char_surface, (self.x, self.y))
        self.hpBar.draw(window)
        self.hpBar.x = char_rect.x
        self.hpBar.y = char_rect.y - 10
        self.label.draw(window)
        self.label.x = self.hpBar.x
        self.label.y = self.hpBar.y - 13
        self._setCharSurfaceRact(char_rect)

    def onclick(self, events: list[pygame.event.Event]):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._getCharSurfaceRect().collidepoint(mouse_pos):
                    print(self.name, self.job, self.hpBar.currentHp, "is Clicked")

                    self.is_active = True
                    return True
                else:
                    self.is_active = False
                    return False
        return False


def _demo():
    import pygame

    from charactor import Charactor

    pygame.init()

    running = True
    window = pygame.display.set_mode((640, 480))

    charactor = Charactor(
        x=100,
        y=200,
        name="Shawn",
        job="Tanker",
        level=1,
        hp=100,
        atk=10,
        defe=10,
        exp=0,
        is_alive=True,
        is_player=True,
    )

    clock = pygame.time.Clock()
    while running:
        clock.tick(30)
        window.fill("white")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        charactor.draw(window)
        if charactor.onclick(events):
            print(
                charactor.name,
                charactor.job,
                charactor.hpBar.currentHp,
                charactor.hpBar.maxHp,
                "is Clicked",
            )
            dmg = -10 if charactor.hpBar.currentHp > 0 else 1000
            newHp = charactor.hpBar.currentHp + dmg
            charactor.setCurrentHp(newHp)
        pygame.display.update()

    pygame.quit()


### what should i write in there
if __name__ == "__main__":
    _demo()
