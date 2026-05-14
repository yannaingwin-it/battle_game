import pygame
import random

from charactor import Charactor
from custom_cursor import CustomCursor
from game_log import GameLog
from state import State
from ui.button import Button
from ui.hp_bar import HPBar
from ui.input_box import InputBox
from ui.label import Label

pygame.init()

# ===================== 基础 =====================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)
hand_cursor = CustomCursor(
    pygame.image.load("hand_cursor.png").convert_alpha()
).getCursor()
pygame.mouse.set_cursor(hand_cursor)

# ===================== 资源 =====================
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

gameLog = GameLog(
    x=0,
    y=0,
    width=240,
    height=HEIGHT,
)


atkbtn = Button("Attack", pygame.Rect(0, 0, 80, 30), font, "red", "darkred")
healbtn = Button("Heal", pygame.Rect(0, 0, 80, 30), font, "green", "darkgreen")


warrior_btn = Button(
    "Warrior",
    pygame.Rect(400, 250, 200, 50),
    font,
    "red",
    "lightblue",
    "white",
    variant="filled",
    radius=4,
)
tanker_btn = Button(
    "Tanker",
    pygame.Rect(620, 250, 200, 50),
    font,
    "lightblue",
    "red",
    "white",
    variant="filled",
    radius=4,
)
next_btn = Button(
    "Next",
    pygame.Rect(500, 350, 200, 60),
    font,
    "green",
    "lightgreen",
    "white",
    variant="filled",
    radius=4,
)

label = Label("Player Name", 420, 155, font, "white")
inputBox = InputBox(
    "",
    pygame.Rect(420, 150, 210, 32),
    pygame.font.Font(None, 32),
    "white",
    (130, 130, 130),
    "white",
    radius=10,
)

# ===================== 状态 =====================
state = "start"

player_names = ["", "", ""]
player_jobs: list[str] = [None, None, None]
player_hp: list[HPBar] = [None, None, None]

players: list[Charactor] = []
enemies: list[Charactor] = []

player_atk = [0, 0, 0]

enemy_jobs = []
enemy_hp = []
enemy_atk = []

current_input: int = 0

selected_player = None
action_mode = None

logs = []


def create_players():
    for i, job in enumerate(player_jobs):
        max_hp = 0
        atk = 0
        if job == "Warrior":
            max_hp = random.randint(100, 130)
            # atk = random.randint(15, 25)
            atk = 300
            defe = 10
        else:
            max_hp = random.randint(140, 180)
            # atk = random.randint(8, 18)
            atk = 300
            defe = 30
        char = Charactor(
            x=0,
            y=0,
            name=player_names[i],
            job=job,
            level=1,
            hp=max_hp,
            atk=atk,
            defe=defe,
            exp=0,
            is_alive=True,
            is_player=True,
        )
        players.append(char)


# ===================== AI =====================
def create_ai():
    for i, _ in enumerate(players):
        rand_ids: list[int] = []
        max_hp = 0
        atk = 0
        job = random.choice(["Warrior", "Tanker"])
        rand_id = random.randint(10, 99)
        # checking if the random id is already in the list
        while rand_id in rand_ids:
            rand_id = random.randint(10, 99)
        rand_ids.append(rand_id)

        enemyName = "AI" + str(rand_id)
        if job == "Warrior":
            max_hp = random.randint(100, 130)
            atk = random.randint(15, 25)
            defe = 10
        else:
            max_hp = random.randint(140, 180)
            atk = random.randint(8, 18)
            defe = 20

        char = Charactor(
            0,
            0,
            enemyName,
            job,
            1,
            max_hp,
            atk,
            defe,
            0,
            True,
            False,
        )
        enemies.append(char)


def heal(palyer: Charactor):
    palyer.hpBar.currentHp = palyer.hpBar.currentHp + player.exp * 2 + 1
    gameLog.addMessage(f"{palyer.name} healed")


# ===================== 攻击 =====================
def attackTo(target: Charactor):
    attacker = State.active_charactor
    real = random.randint(attacker.atk - 5, attacker.atk + 5)
    dmg = real - target.defe
    target.hpBar.currentHp -= dmg

    gameLog.addMessage(f"{attacker.name} hit {target.name} -{dmg}: {real} damage")

    return real


# ===================== AI回合（只打一人） =====================
def ai_turn():
    # attacker = random.randint(0, 2)
    # target = random.randint(0, 2)

    # dmg = random.randint(8, 20)
    # player_hp[target] -= dmg

    # if player_hp[target] < 0:
    #     player_hp[target] = 0

    # logs.append(f"AI{attacker} hit Player{target} -{dmg}")
    pass


counter = 0
# ===================== 主循环 =====================
running = True
clock = pygame.time.Clock()

pygame.mixer.music.load("technotronic.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1, start=0.0)

click_sound = pygame.mixer.Sound("click.wav")

while running:

    clock.tick(30)
    # print(clock.get_fps())
    screen.blit(bg, (0, 0))
    events = pygame.event.get()

    # ===================== START =====================
    if state == "start":

        # title = big_font.render("Setup 3 Players", True, (255, 255, 255))
        # screen.blit(title, (420, 50))
        title = Label("Setup 3 Players", 420, 50, big_font, (255, 255, 255))
        title.draw(screen)

        label.draw(screen)
        label.setText(f"Player {current_input+1}:")
        inputBox.rect.x = 420 + 10 + label.getWidth()
        inputBox.draw(screen)
        inputBox.onchange(events)

        warrior_btn.draw(screen, events)
        tanker_btn.draw(screen, events)
        if warrior_btn.onclick(events):
            player_jobs[current_input] = "Warrior"
            pass
        if tanker_btn.onclick(events):
            player_jobs[current_input] = "Tanker"
            pass

        # 显示当前职业
        if current_input <= 2:
            color = (
                (0, 255, 0)
                if player_jobs[current_input - 1] == "Warrior"
                else (255, 0, 0)
            )
            display_job: str = (
                player_jobs[current_input] if player_jobs[current_input] else ""
            )
            show = font.render(f"Selected: {display_job}", True, color)
            screen.blit(show, (420, 200))

        # NEXT

        next_btn.draw(screen, events)
        if next_btn.onclick(events):
            player_names[current_input] = inputBox.text
            if player_names[current_input] and player_jobs[current_input]:
                current_input += 1
                if current_input >= 3:
                    # create_player()
                    create_players()
                    create_ai()
                    state = "game"

    # ===================== GAME =====================
    if state == "game":

        # game log
        gameLog.handleEvent(events)
        gameLog.draw(screen)
        if (
            State.isActive
            and State.active_charactor.is_active
            and State.active_charactor is not None
            and State.active_charactor.is_alive
            and State.active_charactor.is_player
        ):
            # draw char and buttons
            char = State.active_charactor
            atkbtn.draw(screen, events)
            healbtn.draw(screen, events)
            atkbtn.rect.x = char.char_surface_rect.x + 110
            atkbtn.rect.y = char.char_surface_rect.y
            healbtn.rect.x = char.char_surface_rect.x + 110
            healbtn.rect.y = char.char_surface_rect.y + 50

        if State.isAttacking:
            for i, enemy in enumerate(enemies):
                if (
                    State.active_charactor is not None
                    and State.isActive
                    and enemy.is_alive
                    and State.isAttacking
                    and State.active_charactor.is_player
                    and State.active_charactor.is_alive
                    and enemy.onclick(events)
                ):
                    attackTo(enemy)
                    State.isAttacking = False
            State.active_charactor.is_active = False

        if atkbtn.onclick(events):
            print(State.active_charactor.name, "is Attack")
            print(
                State.isActive,
                State.active_charactor.is_active,
                State.active_charactor is not None,
                State.active_charactor.is_alive,
                State.active_charactor.is_player,
            )
            State.isAttacking = True

        if healbtn.onclick(events):
            heal(State.active_charactor)
            print(
                State.isActive,
                State.active_charactor.is_active,
                State.active_charactor is not None,
                State.active_charactor.is_alive,
                State.active_charactor.is_player,
            )
            print(State.active_charactor.name, "is Heal")

        # ========== 玩家（左） ==========
        for i, player in enumerate(players):
            x, y = gameLog.width + 100, 120 + (i * 180)

            player.x = x
            player.y = y

            if player.hpBar.currentHp <= 0:
                player.hpBar.currentHp = 0
                player.is_alive = False
            player.draw(
                screen,
            )
            if player.onclick(events):
                State.active_charactor = player
                State.isActive = True

        for i, enemy in enumerate(enemies):
            if enemy.hpBar.currentHp <= 0:
                enemy.hpBar.currentHp = 0
                enemy.is_alive = False
            enemy.draw(screen)
            x, y = 900, 120 + i * 180
            enemy.x = x
            enemy.y = y

            # ========== AI（右 + 翻转） ==========

        # ========== 胜负 ==========
        if sum(map(lambda enemy: enemy.hpBar.currentHp, enemies)) <= 0:
            win = big_font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(win, (500, 300))
            state = "end"

        if sum(map(lambda player: player.hpBar.currentHp, players)) <= 0:
            lose = big_font.render("YOU LOSE!", True, (255, 0, 0))
            screen.blit(lose, (500, 300))
            state = "end"

    if state == "end":
        screen.fill((0, 0, 0))
        win = big_font.render("YOU WIN!", True, (0, 255, 0))
        screen.blit(win, (500, 300))
    # ===================== EVENTS =====================
    for event in events:

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # example of adding a message
                gameLog.addMessage("[Game Message] New attack happened!")

            if (
                event.key == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and event.pos[1] < gameLog.y
            ):  # scroll up
                gameLog.scroll(-gameLog.lineHeight)
    pygame.display.update()

pygame.quit()
print("Game Closed")
