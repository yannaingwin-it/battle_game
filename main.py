import pygame
import random

pygame.init()

# ===================== 基础 =====================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

# ===================== 资源 =====================
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

warrior_img = pygame.image.load("warrior.png")
tanker_img = pygame.image.load("tanker.png")

warrior_img = pygame.transform.scale(warrior_img, (100, 100))
tanker_img = pygame.transform.scale(tanker_img, (100, 100))

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)

# ===================== 状态 =====================
state = "start"

player_names = ["", "", ""]
player_jobs = [None, None, None]
player_hp = [0, 0, 0]
player_atk = [0, 0, 0]

enemy_jobs = []
enemy_hp = []
enemy_atk = []

current_input = 0

selected_player = None
action_mode = None

logs = []

# ===================== AI =====================
def create_ai():
    jobs, hp, atk = [], [], []

    for _ in range(3):
        job = random.choice(["Warrior", "Tanker"])
        jobs.append(job)

        if job == "Warrior":
            hp.append(random.randint(100,130))
            atk.append(random.randint(15,25))
        else:
            hp.append(random.randint(140,180))
            atk.append(random.randint(8,18))

    return jobs, hp, atk

# ===================== 玩家 =====================
def create_player():
    for i in range(3):
        if player_jobs[i] == "Warrior":
            player_hp[i] = 120
            player_atk[i] = random.randint(15,25)
        else:
            player_hp[i] = 160
            player_atk[i] = random.randint(8,18)

# ===================== 血条 =====================
def draw_hp(x, y, hp, max_hp=150):
    hp = max(hp,0)
    ratio = hp / max_hp
    pygame.draw.rect(screen,(255,0,0),(x,y,100,8))
    pygame.draw.rect(screen,(0,255,0),(x,y,100*ratio,8))

# ===================== 攻击 =====================
def attack(target_list, i, dmg):
    real = random.randint(dmg-5,dmg+5)
    target_list[i] -= real
    if target_list[i] < 0:
        target_list[i] = 0
    return real

# ===================== AI回合（只打一人） =====================
def ai_turn():
    attacker = random.randint(0,2)
    target = random.randint(0,2)

    dmg = random.randint(8,20)
    player_hp[target] -= dmg

    if player_hp[target] < 0:
        player_hp[target] = 0

    logs.append(f"AI{attacker} hit Player{target} -{dmg}")

# ===================== 主循环 =====================
running = True

while running:

    screen.blit(bg,(0,0))

    # ===================== START =====================
    if state == "start":

        title = big_font.render("Setup 3 Players", True, (255,255,255))
        screen.blit(title,(420,50))

        txt = font.render(
            f"Player {current_input+1}: {player_names[current_input]}",
            True,(255,255,255)
        )
        screen.blit(txt,(420,150))

        # 职业按钮
        pygame.draw.rect(screen,(100,100,255),(400,250,200,50))
        pygame.draw.rect(screen,(255,100,100),(620,250,200,50))

        screen.blit(font.render("Warrior",True,(255,255,255)),(450,260))
        screen.blit(font.render("Tanker",True,(255,255,255)),(670,260))

        # 显示当前职业
        if player_jobs[current_input]:
            color = (0,255,0) if player_jobs[current_input]=="Warrior" else (255,0,0)
            show = font.render(f"Selected: {player_jobs[current_input]}",True,color)
            screen.blit(show,(420,200))

        # NEXT
        pygame.draw.rect(screen,(0,255,0),(500,350,200,60))
        screen.blit(font.render("NEXT",True,(0,0,0)),(570,370))

    # ===================== GAME =====================
    if state == "game":

        # ========== 玩家（左） ==========
        for i in range(3):
            x,y = 100,120+i*180

            img = warrior_img if player_jobs[i]=="Warrior" else tanker_img
            screen.blit(img,(x,y))

            draw_hp(x,y-10,player_hp[i])

            name = font.render(player_names[i],True,(255,255,255))
            screen.blit(name,(x,y+110))
            # ========== AI（右 + 翻转） ==========
        for i in range(3):
            x,y = 900,120+i*180

            img = warrior_img if enemy_jobs[i]=="Warrior" else tanker_img
            img = pygame.transform.flip(img,True,False)

            screen.blit(img,(x,y))

            draw_hp(x,y-10,enemy_hp[i])

        # ========== log（红色） ==========
        for i,l in enumerate(logs[-6:]):
            text = font.render(l,True,(255,0,0))
            screen.blit(text,(420,500+i*25))

        # ========== 胜负 ==========
        if sum(enemy_hp)<=0:
            win = big_font.render("YOU WIN!",True,(0,255,0))
            screen.blit(win,(500,300))
            state="end"

        if sum(player_hp)<=0:
            lose = big_font.render("YOU LOSE!",True,(255,0,0))
            screen.blit(lose,(500,300))
            state="end"

        # ========== 操作按钮 ==========
        if selected_player is not None:

            pygame.draw.rect(screen,(255,0,0),(450,600,150,50))
            pygame.draw.rect(screen,(0,255,0),(650,600,150,50))

            screen.blit(font.render("ATTACK",True,(255,255,255)),(470,615))
            screen.blit(font.render("HEAL",True,(255,255,255)),(690,615))

    # ===================== EVENTS =====================
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        # ===== START =====
        if state=="start":

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    player_names[current_input]=player_names[current_input][:-1]
                else:
                    player_names[current_input]+=event.unicode

            if event.type==pygame.MOUSEBUTTONDOWN:

                mx,my=pygame.mouse.get_pos()

                if 400<mx<600 and 250<my<300:
                    player_jobs[current_input]="Warrior"

                if 620<mx<820 and 250<my<300:
                    player_jobs[current_input]="Tanker"

                if 500<mx<700 and 350<my<410:

                    if player_names[current_input] and player_jobs[current_input]:

                        current_input+=1

                        if current_input>=3:
                            create_player()
                            enemy_jobs,enemy_hp,enemy_atk=create_ai()
                            state="game"

        # ===== GAME =====
        if state=="game":

            if event.type==pygame.MOUSEBUTTONDOWN:

                mx,my=pygame.mouse.get_pos()

                # 选玩家
                for i in range(3):
                    x,y=100,120+i*180
                    if x<mx<x+100 and y<my<y+100:
                        selected_player=i

                # HEAL
                if selected_player is not None:

                    if 650<mx<800 and 600<my<650:
                        player_hp[selected_player]+=random.randint(10,25)
                        logs.append(f"Player{selected_player} HEAL")

                        if player_hp[selected_player]>150:
                            player_hp[selected_player]=150

                    # ATTACK AI
                    if 450<mx<600 and 600<my<650:

                        for i in range(3):
                            x,y=900,120+i*180
                            if x<mx<x+100 and y<my<y+100:

                                dmg=attack(enemy_hp,i,player_atk[selected_player])
                                logs.append(f"Player{selected_player} hit AI{i} -{dmg}")

                                ai_turn()

    pygame.display.update()

pygame.quit()