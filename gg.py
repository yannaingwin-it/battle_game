import pygame
import random
import os
import json
from datetime import datetime

from custom_cursor import CustomCursor

pygame.init()

try:
    pygame.mixer.init()
    AUDIO_READY = True
except pygame.error:
    AUDIO_READY = False

WIDTH = 1100
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (210, 210, 210)
DARK_GRAY = (80, 80, 80)
BLUE = (85, 190, 240)
GREEN = (130, 210, 130)
RED = (230, 100, 100)
YELLOW = (245, 205, 80)

CUSTOM_CURSOR = CustomCursor(pygame.image.load("hand_cursor.png"), (0, 0)).getCursor()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PSB Battle Game")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 22)
BIG_FONT = pygame.font.SysFont("arial", 38, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 17)

BASE_DIR = os.path.dirname(__file__)

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "music")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")
LOG_DIR = os.path.join(BASE_DIR, "logs")
SAVE_DIR = os.path.join(BASE_DIR, "saves")

SAVE_FILE = os.path.join(SAVE_DIR, "save_game.json")
LOG_FILE = os.path.join(LOG_DIR, "battle_log.txt")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SAVE_DIR, exist_ok=True)

ASSET_PATHS = {
    # PUT YOUR MENU BACKGROUND HERE
    "menu_background": os.path.join(IMAGE_DIR, "background.jpg"),
    # PUT YOUR IN-GAME BACKGROUND HERE
    "battle_background": os.path.join(IMAGE_DIR, "battle_background.png"),
    # PUT YOUR CHARACTER PHOTOS HERE
    "warrior": os.path.join(IMAGE_DIR, "warrior.png"),
    "tanker": os.path.join(IMAGE_DIR, "tanker.png"),
    "ai_warrior": os.path.join(IMAGE_DIR, "warrior.png"),
    "ai_tanker": os.path.join(IMAGE_DIR, "tanker.png"),
    # PUT YOUR SHIELD OR RANK ICON HERE
    "rank_icon": os.path.join(IMAGE_DIR, "rank_icon.png"),
    "hand_cursor": os.path.join(IMAGE_DIR, "hand_cursor.png"),
}

# PUT YOUR MUSIC AND SOUND HERE
MUSIC_PATH = os.path.join(MUSIC_DIR, "background_music.mp3")
ATTACK_SOUND_PATH = os.path.join(SOUND_DIR, "attack.wav")
CLICK_SOUND_PATH = os.path.join(SOUND_DIR, "click.wav")


def draw_text(text, x, y, color=BLACK, font=FONT):
    text_surface = font.render(str(text), True, color)
    screen.blit(text_surface, (x, y))


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def load_image(key, size, fallback_color):
    path = ASSET_PATHS[key]

    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image

    placeholder = pygame.Surface(size)
    placeholder.fill(fallback_color)
    pygame.draw.rect(placeholder, BLACK, placeholder.get_rect(), 2)

    label = SMALL_FONT.render(key, True, BLACK)
    placeholder.blit(label, (8, 8))

    return placeholder


def load_sound(path):
    if AUDIO_READY and os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None


images = {
    "menu_background": load_image("menu_background", (WIDTH, HEIGHT), (235, 245, 255)),
    "battle_background": load_image(
        "battle_background", (WIDTH, HEIGHT), (245, 245, 245)
    ),
    "warrior": load_image("warrior", (110, 120), (255, 220, 170)),
    "tanker": load_image("tanker", (110, 120), (180, 220, 255)),
    "ai_warrior": load_image("ai_warrior", (110, 120), (255, 180, 180)),
    "ai_tanker": load_image("ai_tanker", (110, 120), (190, 170, 230)),
    "rank_icon": load_image("rank_icon", (28, 28), YELLOW),
    "hand_cursor": load_image("hand_cursor", (64, 64), BLACK),
}

attack_sound = load_sound(ATTACK_SOUND_PATH)
click_sound = load_sound(CLICK_SOUND_PATH)

if AUDIO_READY and os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)


def play_click():
    if click_sound:
        click_sound.play()


def play_attack():
    if attack_sound:
        attack_sound.play()


class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.click_sound = pygame.mixer.Sound("click.wav")

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=12)

        label = FONT.render(self.text, True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_sound.play()
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            event.pos
        )


class InputBox:
    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 12 and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self):
        if self.active:
            border_color = BLUE
        else:
            border_color = GRAY

        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 3)
        draw_text(self.text, self.rect.x + 8, self.rect.y + 8)


class Unit:
    def __init__(self, name, profession, team_name):
        self.name = name
        self.profession = profession
        self.team_name = team_name

        self.max_hp = 100
        self.hp = 100
        self.exp = 0
        self.rank = 1

        if profession == "Warrior":
            self.atk = random.randint(8, 24)
            self.defence = random.randint(1, 8)
        else:
            self.atk = random.randint(4, 14)
            self.defence = random.randint(6, 14)

        # AI is slightly weaker so the game is fairer for the player
        if team_name == "AI":
            self.atk -= 2
            self.defence -= 2

            if self.atk < 1:
                self.atk = 1

            if self.defence < 1:
                self.defence = 1

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, amount):
        self.exp += max(0, int(amount))

        while self.exp >= 100:
            self.exp -= 100
            self.rank += 1
            self.max_hp += 10
            self.hp = min(self.max_hp, self.hp + 25)
            self.atk += 2
            self.defence += 1
            log_event(f"{self.name} promoted to rank {self.rank}.")

    def image_key(self):
        if self.team_name == "AI":
            if self.profession == "Warrior":
                return "ai_warrior"
            else:
                return "ai_tanker"
        else:
            if self.profession == "Warrior":
                return "warrior"
            else:
                return "tanker"

    def to_dict(self):
        return {
            "name": self.name,
            "profession": self.profession,
            "team_name": self.team_name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "atk": self.atk,
            "defence": self.defence,
            "exp": self.exp,
            "rank": self.rank,
        }

    @classmethod
    def from_dict(cls, data):
        unit = cls(data["name"], data["profession"], data["team_name"])
        unit.max_hp = data["max_hp"]
        unit.hp = data["hp"]
        unit.atk = data["atk"]
        unit.defence = data["defence"]
        unit.exp = data["exp"]
        unit.rank = data["rank"]
        return unit


class Team:
    def __init__(self, name):
        self.name = name
        self.units = []

    def alive_units(self):
        alive = []

        for unit in self.units:
            if unit.is_alive():
                alive.append(unit)

        return alive

    def remove_defeated(self):
        self.units = [unit for unit in self.units if unit.is_alive()]

    def to_dict(self):
        return {
            "name": self.name,
            "units": [unit.to_dict() for unit in self.units],
        }

    @classmethod
    def from_dict(cls, data):
        team = cls(data["name"])
        team.units = [Unit.from_dict(unit_data) for unit_data in data["units"]]
        return team


class BattleGame:
    def __init__(self):
        self.state = "menu"

        self.player_team = Team("Player")
        self.ai_team = Team("AI")

        self.messages = []
        self.selected_attacker = None
        self.selected_target = None
        self.running = True
        self.name_boxes = [
            InputBox(420, 190, 220, 44, "Hero1"),
            InputBox(420, 260, 220, 44, "Hero2"),
            InputBox(420, 330, 220, 44, "Hero3"),
        ]

        self.professions = ["Warrior", "Warrior", "Tanker"]

        self.start_button = Button(440, 420, 180, 50, "Start Game", GREEN)
        self.load_button = Button(440, 490, 180, 50, "Load Game", BLUE)

        self.save_button = Button(30, 650, 110, 42, "Save", BLUE)
        self.restart_button = Button(155, 650, 120, 42, "Restart", GRAY)
        self.exit_button = Button(290, 650, 100, 42, "Exit", RED)

    def add_message(self, message):
        self.messages.insert(0, message)
        self.messages = self.messages[:12]
        log_event(message)

    def create_teams(self):
        self.player_team = Team("Player")
        self.ai_team = Team("AI")

        for i in range(3):
            name = self.name_boxes[i].text.strip()

            if name == "":
                name = f"Hero{i + 1}"

            profession = self.professions[i]
            self.player_team.units.append(Unit(name, profession, "Player"))

        for i in range(3):
            ai_name = "AI" + str(random.randint(10, 99))
            ai_profession = random.choice(["Warrior", "Tanker"])
            self.ai_team.units.append(Unit(ai_name, ai_profession, "AI"))

        self.messages = []
        self.selected_attacker = None
        self.selected_target = None

        self.add_message("Game started. Select your unit, then select an AI target.")
        self.state = "battle"

    def calculate_attack(self, attacker, target):
        random_bonus = random.randint(-3, 12)

        damage = attacker.atk + random_bonus - (target.defence // 2)

        if damage < 3:
            damage = 3

        target.hp -= damage

        attacker_exp = damage
        target_exp = target.defence

        if damage > 15:
            target_exp = int(target_exp * 1.2)

        attacker.gain_exp(attacker_exp)
        target.gain_exp(target_exp)

        return damage, random_bonus

    def player_attack(self):
        if self.selected_attacker is None or self.selected_target is None:
            self.add_message("Select one player unit and one AI target first.")
            return

        play_attack()

        damage, random_bonus = self.calculate_attack(
            self.selected_attacker, self.selected_target
        )

        self.add_message(
            f"{self.selected_attacker.name} attacked {self.selected_target.name}: "
            f"damage {damage}, random {random_bonus}."
        )

        self.ai_team.remove_defeated()
        self.selected_target = None

        if self.check_winner():
            return

        self.ai_turn()
        self.check_winner()

    def ai_turn(self):
        if len(self.ai_team.alive_units()) == 0:
            return

        if len(self.player_team.alive_units()) == 0:
            return

        ai_attacker = max(self.ai_team.alive_units(), key=lambda unit: unit.atk)
        player_target = min(self.player_team.alive_units(), key=lambda unit: unit.hp)

        play_attack()

        damage, random_bonus = self.calculate_attack(ai_attacker, player_target)

        self.add_message(
            f"{ai_attacker.name} attacked {player_target.name}: "
            f"damage {damage}, random {random_bonus}."
        )

        self.player_team.remove_defeated()
        self.selected_attacker = None

    def check_winner(self):
        if len(self.ai_team.alive_units()) == 0:
            self.add_message("Player wins! All AI units are defeated.")
            self.state = "game_over"
            return True

        if len(self.player_team.alive_units()) == 0:
            self.add_message("AI wins! All player units are defeated.")
            self.state = "game_over"
            return True

        return False

    def save_game(self):
        data = {
            "player_team": self.player_team.to_dict(),
            "ai_team": self.ai_team.to_dict(),
            "messages": self.messages,
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        self.add_message("Game saved.")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.add_message("No save file found.")
            return

        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.player_team = Team.from_dict(data["player_team"])
        self.ai_team = Team.from_dict(data["ai_team"])
        self.messages = data.get("messages", [])

        self.selected_attacker = None
        self.selected_target = None

        self.state = "battle"
        self.add_message("Game loaded.")

    def get_unit_rects(self, team, left_side):
        rects = []

        if left_side:
            start_x = 455
        else:
            start_x = 820

        start_y = 100
        gap_y = 185

        for index, unit in enumerate(team.units):
            row = index % 3
            col = index // 3

            x = start_x + col * 125
            y = start_y + row * gap_y

            rect = pygame.Rect(x, y, 130, 165)
            rects.append((unit, rect))

        return rects

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == "menu":
                self.handle_menu_events(event)
            elif self.state == "battle" or self.state == "game_over":
                self.handle_battle_events(event)

        return True

    def handle_menu_events(self, event):
        for box in self.name_boxes:
            box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            for i in range(3):
                warrior_rect = pygame.Rect(670, 190 + i * 70, 110, 44)
                tanker_rect = pygame.Rect(790, 190 + i * 70, 110, 44)

                if warrior_rect.collidepoint(mouse_pos):
                    self.professions[i] = "Warrior"
                    play_click()

                if tanker_rect.collidepoint(mouse_pos):
                    self.professions[i] = "Tanker"
                    play_click()

        if self.start_button.clicked(event):
            play_click()
            self.create_teams()

        if self.load_button.clicked(event):
            play_click()
            self.load_game()

    def handle_battle_events(self, event):
        if self.exit_button.clicked(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.restart_button.clicked(event):
            play_click()
            self.state = "menu"

        if self.save_button.clicked(event) and self.state == "battle":
            play_click()
            self.save_game()

        if self.state != "battle":
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            for unit, rect in self.get_unit_rects(self.player_team, True):
                if rect.collidepoint(mouse_pos):
                    self.selected_attacker = unit
                    self.add_message(f"Selected attacker: {unit.name}.")

            for unit, rect in self.get_unit_rects(self.ai_team, False):
                if rect.collidepoint(mouse_pos):
                    self.selected_target = unit
                    self.add_message(f"Selected target: {unit.name}.")

            # Attack button moved down so it does not cover Hero 3
            attack_button_rect = pygame.Rect(655, 665, 120, 45)

            if attack_button_rect.collidepoint(mouse_pos):
                self.player_attack()

    def draw_menu(self):
        screen.blit(images["menu_background"], (0, 0))

        draw_text("PSB Turn-Based Battle Game", 325, 70, BLACK, BIG_FONT)
        draw_text(
            "Enter 3 player units and choose each profession.", 345, 125, DARK_GRAY
        )

        for i, box in enumerate(self.name_boxes):
            draw_text(f"Unit {i + 1} name:", 270, 200 + i * 70)
            box.draw()

            if self.professions[i] == "Warrior":
                warrior_color = GREEN
            else:
                warrior_color = GRAY

            if self.professions[i] == "Tanker":
                tanker_color = GREEN
            else:
                tanker_color = GRAY

            warrior_button = Button(
                670, 190 + i * 70, 110, 44, "Warrior", warrior_color
            )
            tanker_button = Button(790, 190 + i * 70, 110, 44, "Tanker", tanker_color)

            warrior_button.draw()
            tanker_button.draw()

        self.start_button.draw()
        self.load_button.draw()

    def draw_battle(self):
        screen.blit(images["battle_background"], (0, 0))

        pygame.draw.rect(screen, WHITE, (20, 20, 390, 680))
        pygame.draw.rect(screen, BLACK, (20, 20, 390, 680), 2)

        draw_text("PSB Battle Game", 40, 38, BLACK, FONT)
        draw_text("Game Log", 40, 78, BLACK, FONT)

        pygame.draw.line(screen, BLACK, (20, 110), (410, 110), 2)

        y = 125

        for message in self.messages:
            draw_text(message[:42], 35, y, DARK_GRAY, SMALL_FONT)
            y += 38

        self.save_button.draw()
        self.restart_button.draw()
        self.exit_button.draw()

        draw_text("Player Team", 500, 30, BLACK, FONT)
        draw_text("AI Team", 875, 30, BLACK, FONT)

        self.draw_team(self.player_team, True)
        self.draw_team(self.ai_team, False)

        # Attack button moved down so it does not cover Hero 3
        attack_button = Button(655, 665, 120, 45, "Attack", RED)
        attack_button.draw()

        if self.state == "game_over":
            pygame.draw.rect(screen, WHITE, (455, 250, 410, 130))
            pygame.draw.rect(screen, BLACK, (455, 250, 410, 130), 3)

            draw_text("Game Over", 560, 275, BLACK, BIG_FONT)
            draw_text("Click Restart to play again.", 535, 335, DARK_GRAY)

    def draw_team(self, team, left_side):
        for unit, rect in self.get_unit_rects(team, left_side):
            if unit == self.selected_attacker or unit == self.selected_target:
                border_color = YELLOW
            else:
                border_color = BLACK

            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, border_color, rect, 3)

            screen.blit(images[unit.image_key()], (rect.x + 10, rect.y + 5))
            # screen.blit(images["rank_icon"], (rect.x + 95, rect.y + 8))

            draw_text(unit.name, rect.x + 5, rect.y + 128, BLACK, SMALL_FONT)
            draw_text(
                f"Lv {unit.rank} {unit.profession}",
                rect.x + 5,
                rect.y + 146,
                DARK_GRAY,
                SMALL_FONT,
            )

            self.draw_hp_bar(rect.x + 5, rect.y + 170, 120, 12, unit.hp, unit.max_hp)

            draw_text(
                f"ATK {unit.atk} DEF {unit.defence} EXP {unit.exp}",
                rect.x + 5,
                rect.y + 186,
                DARK_GRAY,
                SMALL_FONT,
            )

    def draw_hp_bar(self, x, y, width, height, hp, max_hp):
        pygame.draw.rect(screen, GRAY, (x, y, width, height))

        hp_ratio = max(0, hp) / max_hp
        pygame.draw.rect(screen, BLUE, (x, y, int(width * hp_ratio), height))

        pygame.draw.rect(screen, BLACK, (x, y, width, height), 1)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_battle()

    def run(self):
        cus_cursor = pygame.cursors.Cursor((0, 0), images["hand_cursor"])
        pygame.mouse.set_cursor(cus_cursor)
        pygame.mixer.music.load("technotronic.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1, start=0.0)

        while self.running:
            clock.tick(FPS)

            self.running = self.handle_events()

            self.draw()

            pygame.display.flip()

        pygame.quit()


game = BattleGame()
game.run()
