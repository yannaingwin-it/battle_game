import pygame
import random

from charactor import Charactor
from custom_cursor import CustomCursor
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

hand_cursor = CustomCursor(
    pygame.image.load("hand_cursor.png").convert_alpha()
).getCursor()
pygame.mouse.set_cursor(hand_cursor)

# ===================== 资源 =====================
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# warrior_img = pygame.image.load("warrior.png")
# tanker_img = pygame.image.load("tanker.png")

# warrior_img = pygame.transform.scale(warrior_img, (100, 100))
# tanker_img = pygame.transform.scale(tanker_img, (100, 100))


font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)


atkbtn = Button("Attack", pygame.Rect(0, 0, 80, 30), font, "red", "darkred")
healbtn = Button("Heal", pygame.Rect(0, 0, 80, 30), font, "green", "darkgreen")


"""
        pygame.draw.rect(screen, (100, 100, 255), (400, 250, 200, 50))
        pygame.draw.rect(screen, (255, 100, 100), (620, 250, 200, 50))
"""
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


# ===================== AI =====================
def create_ai():
    for i, _ in enumerate(players):
        max_hp = 0
        atk = 0
        job = random.choice(["Warrior", "Tanker"])
        enemyName = "AI" + str(i + 20)
        if job == "Warrior":
            max_hp = random.randint(100, 130)
            atk = random.randint(15, 25)
            defe = 10
        else:
            max_hp = random.randint(140, 180)
            atk = random.randint(8, 18)
            defe = 30

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


# ===================== 攻击 =====================
def attack(target_list, i, dmg):
    real = random.randint(dmg - 5, dmg + 5)
    target_list[i] -= real
    if target_list[i] < 0:
        target_list[i] = 0
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

# pygame.mixer.music.load("technotronic.ogg")
# pygame.mixer.music.play(loops=-1, start=0.0)


while running:

    clock.tick(30)
    screen.blit(bg, (0, 0))
    events = pygame.event.get()

    # ===================== START =====================
    if state == "start":

        title = big_font.render("Setup 3 Players", True, (255, 255, 255))
        screen.blit(title, (420, 50))

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
            show = font.render(f"Selected: {player_jobs[current_input]}", True, color)
            screen.blit(show, (420, 200))

        # NEXT

        next_btn.draw(screen, events)
        if next_btn.onclick(events):
            player_names[current_input] = inputBox.text
            if player_names[current_input] and player_jobs[current_input]:
                current_input += 1
                if current_input >= 3:
                    # create_player()
                    for i, job in enumerate(player_jobs):
                        max_hp = 0
                        atk = 0
                        if job == "Warrior":
                            max_hp = random.randint(100, 130)
                            atk = random.randint(15, 25)
                            defe = 10
                        else:
                            max_hp = random.randint(140, 180)
                            atk = random.randint(8, 18)
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

                    create_ai()
                    state = "game"

    # ===================== GAME =====================
    if state == "game":

        if (
            State.isActive
            and State.active_charactor.is_active
            and State.active_charactor is not None
            and State.active_charactor.is_alive
            and State.active_charactor.is_player
        ):
            char = State.active_charactor
            atkbtn.draw(screen, events)
            healbtn.draw(screen, events)
            atkbtn.rect.x = char.char_surface_rect.x + 110
            atkbtn.rect.y = char.char_surface_rect.y
            healbtn.rect.x = char.char_surface_rect.x + 110
            healbtn.rect.y = char.char_surface_rect.y + 50
            pass

        if atkbtn.onclick(events):
            print(State.active_charactor.name, "someone is Attack")
        if healbtn.onclick(events):
            print(State.active_charactor.name, "someone is heal")

        # ========== 玩家（左） ==========
        for i, player in enumerate(players):
            x, y = 100, 120 + i * 180

            player.x = x
            player.y = y
            player.draw(
                screen,
            )
            if player.onclick(events):
                State.active_charactor = player
                State.isActive = True

        for i, enemy in enumerate(enemies):
            enemy.draw(screen)
            x, y = 900, 120 + i * 180
            enemy.x = x
            enemy.y = y

            if enemy.onclick(events):
                State.target_charactor = enemy
                State.isTargeting = True

            # ========== AI（右 + 翻转） ==========

        # img = warrior_img if enemy_jobs[i] == "Warrior" else tanker_img
        # img = pygame.transform.flip(img, True, False)

        # screen.blit(img, (x, y))

        # draw_hp(x, y - 10, enemy_hp[i])

        # ========== log（红色） ==========
        # for i, log in enumerate(logs[-6:]):
        #     text = font.render(log, True, (255, 0, 0))
        #     screen.blit(text, (420, 500 + i * 25))

        # ========== 胜负 ==========
        # if sum(enemy_hp) <= 0:
        #     win = big_font.render("YOU WIN!", True, (0, 255, 0))
        #     screen.blit(win, (500, 300))
        #     state = "end"

        # if sum(map(lambda char: char.maxHp, player_hp)) <= 0:
        #     lose = big_font.render("YOU LOSE!", True, (255, 0, 0))
        #     screen.blit(lose, (500, 300))
        #     state = "end"

        # ========== 操作按钮 ==========
        # if selected_player is not None:

        #     pygame.draw.rect(screen, (255, 0, 0), (450, 600, 150, 50))
        #     pygame.draw.rect(screen, (0, 255, 0), (650, 600, 150, 50))

        #     screen.blit(font.render("ATTACK", True, (255, 255, 255)), (470, 615))
        #     screen.blit(font.render("HEAL", True, (255, 255, 255)), (690, 615))

    # ===================== EVENTS =====================
    for event in events:
        # mouse_pos = pygame.mouse.get_pos()
        # screen.blit(cursor_surface, mouse_pos)
        if event.type == pygame.QUIT:
            running = False

        # ===== GAME =====
        if state == "game":
            pass
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     # State.isActive = False
            #     pass

            # # 选玩家
            # for i in range(3):
            #     x, y = 100, 120 + i * 180
            #     if x < mx < x + 100 and y < my < y + 100:
            #         selected_player = i

            # HEAL
            # if selected_player is not None:

            # if 650 < mx < 800 and 600 < my < 650:
            # pass
            # player_hp[selected_player] += random.randint(10, 25)
            # logs.append(f"Player{selected_player} HEAL")

            # if player_hp[selected_player] > 150:
            #     player_hp[selected_player] = 150

            # ATTACK AI
            # if 450 < mx < 600 and 600 < my < 650:

            #     for i in range(3):
            #         x, y = 900, 120 + i * 180
            #         if x < mx < x + 100 and y < my < y + 100:

            #             dmg = attack(enemy_hp, i, player_atk[selected_player])
            #             logs.append(f"Player{selected_player} hit AI{i} -{dmg}")

            #             ai_turn()
    pygame.display.update()

pygame.quit()
print("Game Closed")
