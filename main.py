import pygame
import random
import math
from custom_cursor import CustomCursor
from game_log import GameLog
from ui.button import Button
pygame.init()

# ===================== 基础 =====================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game A+ Final")

clock = pygame.time.Clock()

# ===================== 资源 =====================
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

warrior_img = pygame.image.load("warrior.png")
tanker_img = pygame.image.load("tanker.png")

warrior_img = pygame.transform.scale(warrior_img, (90, 90))
tanker_img = pygame.transform.scale(tanker_img, (90, 90))

font = pygame.font.SysFont(None, 26)
big_font = pygame.font.SysFont(None, 60)
gameLog = GameLog(x=0, y=0, width=240, height=HEIGHT)
restart_btn  = Button(
        "Restart",
        pygame.Rect(100, 100, 110, 32),
        pygame.font.Font(None, 32),
        "black",
        "red",
        "lightblue",
        radius=8,
        variant="filled",
    )
quit_btn  = Button(
        "Quit",
        pygame.Rect(100, 100, 110, 32),
        pygame.font.Font(None, 32),
        "black",
        "red",
        "lightblue",
        radius=8,
        variant="filled",
    )
# ===================== 状态 =====================
state = "start"

player_names = ["", "", ""]
player_jobs = [None, None, None]

player_hp = [0, 0, 0]
player_maxhp = [0, 0, 0]
player_atk = [0, 0, 0]

player_rank = [1, 1, 1]
player_exp = [0, 0, 0]
player_gold = [0, 0, 0]

enemy_names = []
enemy_jobs = []
enemy_hp = []
enemy_maxhp = []
enemy_atk = []
enemy_rank = [1, 1, 1]

current_input = 0

selected_player = None
action_mode = None

turn = "player"

logs = []

# ===================== 坐标 =====================
player_pos = []
enemy_pos = []

original_pos = [None, None, None]
enemy_original_pos = [None, None, None]

# ===================== 战斗 =====================
battle_state = "idle"

attacker = None
target = None

enemy_action = [0, 0]

# ===================== AI名字 =====================
def ai_name():
    return "AI" + str(random.randint(10, 99))

# ===================== 创建AI =====================
def create_ai():

    global enemy_names
    global enemy_pos

    enemy_names = []
    enemy_pos = []

    jobs = []
    hp = []
    maxhp = []
    atk = []

    for i in range(3):

        job = random.choice(["Warrior", "Tanker"])

        jobs.append(job)

        enemy_names.append(ai_name())

        enemy_pos.append([900, 120 + i * 180])

        if job == "Warrior":
            hp.append(150)
            maxhp.append(150)
            atk.append(random.randint(15, 25))

        else:
            hp.append(170)
            maxhp.append(170)
            atk.append(random.randint(8, 18))

    return jobs, hp, maxhp, atk

# ===================== 创建玩家 =====================
def create_player():

    global player_pos

    player_pos = []

    for i in range(3):

        player_pos.append([300, 120 + i * 180])

        if player_jobs[i] == "Warrior":

            player_hp[i] = 150
            player_maxhp[i] = 150
            player_atk[i] = random.randint(15, 25)

        else:

            player_hp[i] = 170
            player_maxhp[i] = 170
            player_atk[i] = random.randint(8, 18)

# ===================== EXP =====================
def add_exp(i, v):

    player_exp[i] += v

    if player_exp[i] >= 100:

        player_exp[i] -= 100

        player_rank[i] += 1
        player_atk[i] += 2
        player_gold[i] += 20

        # logs.append(f"{player_names[i]} Rank Up!")
        gameLog.addMessage(f"{player_names[i]} Rank Up!")

# ===================== 移动 =====================
def move(pos, tx, ty, speed=4):

    dx = tx - pos[0]
    dy = ty - pos[1]

    dist = math.sqrt(dx * dx + dy * dy)

    if dist < speed:

        pos[0] = tx
        pos[1] = ty

        return True

    pos[0] += speed * dx / dist
    pos[1] += speed * dy / dist

    return False

# ===================== HP条 =====================
def draw_hp(x, y, hp, maxhp):

    ratio = max(hp, 0) / maxhp

    pygame.draw.rect(screen, (255, 0, 0), (x, y, 90, 8))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 90 * ratio, 8))

# ===================== 伤害 =====================
def damage(atk):

    return random.randint(atk - 5, atk + 5)

# ===================== AI回合 =====================
def ai_turn():

    global battle_state

    alive_ai = []
    alive_player = []

    for i in range(3):
        if enemy_hp[i] > 0:
            alive_ai.append(i)

    for i in range(3):
        if player_hp[i] > 0:
            alive_player.append(i)

    if len(alive_ai) == 0 or len(alive_player) == 0:
        return

    a = random.choice(alive_ai)
    t = random.choice(alive_player)

    enemy_action[0] = a
    enemy_action[1] = t

    enemy_original_pos[a] = enemy_pos[a][:]

    battle_state = "enemy_move"

def game_restart():
    player_names = ["", "", ""]
    player_jobs = [None, None, None]
    player_hp = [0, 0, 0]
    player_maxhp = [0, 0, 0]
    player_atk = [0, 0, 0]
    player_rank = [1, 1, 1]
    player_exp = [0, 0, 0]
    player_gold = [0, 0, 0]
    current_input = 0
    selected_player = None
    action_mode = None
    turn = "player"
    gameLog.messages = []

# ===================== 主循环 =====================
running = True
pygame.mixer.music.load("technotronic.ogg")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(loops=-1, start=0.0)

hand_cursor = CustomCursor(
    pygame.image.load("hand_cursor.png")
).getCursor()
pygame.mouse.set_cursor(hand_cursor)
click_sound = pygame.mixer.Sound("click.wav")   
click_healsound = pygame.mixer.Sound("spell1_0.wav")
while running:

    screen.blit(bg, (0, 0))
    events = pygame.event.get()

    # ===================== START =====================
    if state == "start":

        screen.blit(
            big_font.render("SETUP", True, (255, 255, 255)),
            (500, 50)
        )

        txt = font.render(
            f"Player {current_input+1}: {player_names[current_input]}",
            True,
            (255, 255, 255)
        )

        screen.blit(txt, (420, 150))

        pygame.draw.rect(screen, (80, 80, 200), (400, 250, 180, 50))
        pygame.draw.rect(screen, (200, 80, 80), (600, 250, 180, 50))

        screen.blit(
            font.render("Warrior", True, (255, 255, 255)),
            (440, 265)
        )

        screen.blit(
            font.render("Tanker", True, (255, 255, 255)),
            (640, 265)
        )

        # 显示职业
        if player_jobs[current_input] is not None:

            color = (
                (0, 255, 0)
                if player_jobs[current_input] == "Warrior"
                else (255, 0, 0)
            )

            screen.blit(
                font.render(
                    f"Selected: {player_jobs[current_input]}",
                    True,
                    color
                ),
                (420, 200)
            )

        pygame.draw.rect(screen, (0, 255, 0), (500, 350, 180, 60))

        screen.blit(
            font.render("NEXT", True, (0, 0, 0)),
            (565, 370)
        )

    # ===================== GAME =====================
    if state == "game":

        gameLog.handleEvent(events)
        gameLog.draw(screen)
        restart_btn.draw(screen,events)
        restart_btn.rect.x = 20
        restart_btn.rect.y = HEIGHT - HEIGHT - 60
        if restart_btn.draw(screen,events):
            game_restart()
        # ===================== 玩家 =====================
        for i in range(3):

            if player_hp[i] <= 0:
                continue

            img = (
                warrior_img
                if player_jobs[i] == "Warrior"
                else tanker_img
            )

            screen.blit(img, (player_pos[i][0], player_pos[i][1]))

            draw_hp(
                player_pos[i][0],
                player_pos[i][1] - 10,
                player_hp[i],
                player_maxhp[i]
            )

            screen.blit(
                font.render(
                    f"{player_names[i]}  HP:{player_hp[i]}  R{player_rank[i]}  EXP:{player_exp[i]}",
                    True,
                    (255, 255, 255)
                ),
                (player_pos[i][0], player_pos[i][1] + 95)
            )

        # ===================== AI =====================
        for i in range(3):

            if enemy_hp[i] <= 0:
                continue

            img = (
                warrior_img
                if enemy_jobs[i] == "Warrior"
                else tanker_img
            )

            img = pygame.transform.flip(img, True, False)

            screen.blit(img, (enemy_pos[i][0], enemy_pos[i][1]))

            draw_hp(
                enemy_pos[i][0],
                enemy_pos[i][1] - 10,
                enemy_hp[i],
                enemy_maxhp[i]
            )

            screen.blit(
                font.render(
                    f"{enemy_names[i]}  HP:{enemy_hp[i]}  R{enemy_rank[i]}",
                    True,
                    (255, 255, 255)
                ),
                (enemy_pos[i][0], enemy_pos[i][1] + 95)
            )

        # ===================== LOG =====================
        # for i, l in enumerate(logs[-6:]):

        #     screen.blit(
        #         font.render(l, True, (255, 200, 0)),
        #         (420, 500 + i * 22)
        #     )

        # ===================== WIN LOSE =====================
        if sum(enemy_hp) <= 0:
            state = "win"

        if sum(player_hp) <= 0:
            state = "lose"

        # ===================== 按钮 =====================
        if selected_player is not None:

            pygame.draw.rect(screen, (255, 0, 0), (450, 600, 150, 50))
            pygame.draw.rect(screen, (0, 255, 0), (650, 600, 150, 50))
            screen.blit(
                font.render("ATTACK", True, (255, 255, 255)),
                (470, 615)
            )

            screen.blit(
                font.render("HEAL", True, (255, 255, 255)),
                (690, 615)
            )

        # ===================== 玩家移动 =====================
        if battle_state == "player_move":

            p = attacker
            e = target

            tx = enemy_pos[e][0] - 80
            ty = enemy_pos[e][1]

            if move(player_pos[p], tx, ty):

                dmg = damage(player_atk[p])

                # enemy_hp[e] -= 
                enemy_hp[e] -= dmg+ player_rank[p] * 2

                if enemy_hp[e] < 0:
                    enemy_hp[e] = 0

                add_exp(p, 10)

                # logs.append(
                #     f"{player_names[p]} hit {enemy_names[e]} -{dmg}"
                # )
                gameLog.addMessage(f"{player_names[p]} hit {enemy_names[e]} for {dmg} damage!")

                battle_state = "player_return"

        # ===================== 玩家返回 =====================
        if battle_state == "player_return":

            p = attacker

            ox, oy = original_pos[p]

            if move(player_pos[p], ox, oy):

                battle_state = "idle"

        # ===================== AI移动 =====================
        if battle_state == "enemy_move":

            a = enemy_action[0]
            t = enemy_action[1]

            tx = player_pos[t][0] + 80
            ty = player_pos[t][1]

            if move(enemy_pos[a], tx, ty):

                dmg = damage(enemy_atk[a])

                player_hp[t] -= dmg

                if player_hp[t] < 0:
                    player_hp[t] = 0

               
                gameLog.addMessage(f"{enemy_names[a]} hit {player_names[t]} for {dmg} damage!")
                battle_state = "enemy_return"

        # ===================== AI返回 =====================
        if battle_state == "enemy_return":

            a = enemy_action[0]

            ox, oy = enemy_original_pos[a]

            if move(enemy_pos[a], ox, oy):

                battle_state = "idle"

        # ===================== AI回合 =====================
        if turn == "enemy" and battle_state == "idle":

            ai_turn()

            turn = "player"

    # ===================== WIN =====================
    if state == "win":
        restart_btn.draw(screen,events)
        quit_btn.draw(screen,events)
        if quit_btn.onclick(events):
            running = False
        # place button
        restart_btn.rect.x = 550
        restart_btn.rect.y = 400
        quit_btn.rect.x = 550   
        quit_btn.rect.y = 450   
        if restart_btn.onclick(events):
            state = "start"
            # restart all state to default
            game_restart()


        screen.blit(
            big_font.render("YOU WIN!", True, (0, 255, 0)),
            (450, 300)
        )

    # ===================== LOSE =====================
    if state == "lose":

        screen.blit(
            big_font.render("YOU LOSE!", True, (255, 0, 0)),
            (450, 300)
        )

    # ===================== EVENTS =====================
    for event in events:

        if event.type == pygame.QUIT:
            running = False

        # ===================== START =====================
        if state == "start":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    click_sound.play(1, )
                    player_names[current_input] = (
                        player_names[current_input][:-1]
                    )

                else:
                    click_sound.play(1, )
                    player_names[current_input] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:    
                mx, my = pygame.mouse.get_pos()
                click_sound.play(1, )  
                # Warrior
                if 400 < mx < 580 and 250 < my < 300:

                    player_jobs[current_input] = "Warrior"

                # Tanker
                if 600 < mx < 780 and 250 < my < 300:

                    player_jobs[current_input] = "Tanker"

                # NEXT
                if 500 < mx < 680 and 350 < my < 410:

                    if (
                        player_names[current_input]
                        and player_jobs[current_input]
                    ):

                        current_input += 1

                        if current_input >= 3:

                            create_player()

                            (
                                enemy_jobs,
                                enemy_hp,
                                enemy_maxhp,
                                enemy_atk
                                ) = create_ai()

                            state = "game"

        # ===================== GAME =====================
        if state == "game":

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = pygame.mouse.get_pos()

                # 选择角色
                for i in range(3):

                    x, y = player_pos[i]

                    if (
                        x < mx < x + 90
                        and y < my < y + 90
                        and player_hp[i] > 0
                    ):

                        selected_player = i
                        click_sound.play(1, )
                # ATTACK按钮
                if selected_player is not None:

                    if 450 < mx < 600 and 600 < my < 650:

                        action_mode = "attack"
                        click_sound.play(1, )
                    # HEAL按钮
                    if 650 < mx < 800 and 600 < my < 650:
                        action_mode = "heal"
                        player_hp[selected_player] += 20
                        click_healsound.play(1, )
                        if (
                            player_hp[selected_player]
                            > player_maxhp[selected_player]
                        ):

                            player_hp[selected_player] = (
                                player_maxhp[selected_player]
                            )

                        # logs.append(
                        #     f"{player_names[selected_player]} HEAL +20"
                        # )
                        gameLog.addMessage(f"{player_names[selected_player]} HEAL +20")
                        # turn = "enemy"

                # 攻击敌人
                if action_mode == "attack":

                    for i in range(3):

                        x, y = enemy_pos[i]

                        if (
                            x < mx < x + 90 
                            and y < my < y + 90
                            and enemy_hp[i] > 0
                        ):
                            gameLog.addMessage(f"{player_names[selected_player]} attacks {enemy_names[i]}!")
                    
                            attacker = selected_player
                            target = i

                            original_pos[attacker] = (
                                player_pos[attacker][:]
                            )

                            battle_state = "player_move"

                            action_mode = None
                            turn = "enemy"
                            click_sound.play(1, )   
    pygame.display.update()
    clock.tick(300)
    # print(clock.get_fps())

pygame.quit()