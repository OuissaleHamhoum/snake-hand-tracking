import cv2
import mediapipe as mp
import numpy as np
import pygame
import random
import sys
import os

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sound")

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Set maximum volume for all future sounds
pygame.mixer.set_num_channels(16)
for i in range(pygame.mixer.get_num_channels()):
    pygame.mixer.Channel(i).set_volume(1.0)

WIDTH, HEIGHT = 900, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nokia Snake Hand Tracking")

# Fonts
try:
    font_style = pygame.font.Font("PressStart2P.ttf", 18)
except:
    font_style = pygame.font.SysFont("consolas", 24, bold=True)

try:
    font_small = pygame.font.Font("PressStart2P.ttf", 12)
except:
    font_small = pygame.font.SysFont("consolas", 16, bold=True)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SHADOW = (40, 40, 40)
BANNER = (30, 30, 30)
BANNER_LINE = (80, 80, 80)
TRANSPARENT_BG = (20, 20, 20, 180)

snake_block = 10
clock = pygame.time.Clock()
snake_speed = 8  # Start speed

LEVEL_MUSICS = [
    "motivation.mp3",  # Using your existing music file for all levels
    "motivation.mp3",
    "motivation.mp3",
    "motivation.mp3",
    "motivation.mp3"
]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# -------------------- DRAWING FUNCTIONS --------------------
def draw_gradient_background():
    for i in range(HEIGHT):
        color = (
            int(30 + (i / HEIGHT) * 60),
            int(30 + (i / HEIGHT) * 60),
            int(30 + (i / HEIGHT) * 80)
        )
        pygame.draw.line(win, color, (0, i), (WIDTH, i))

def draw_borders():
    border_rect = pygame.Rect(6, 46, WIDTH-12, HEIGHT-52)
    s = pygame.Surface((WIDTH-12, HEIGHT-52), pygame.SRCALPHA)
    s.fill(TRANSPARENT_BG)
    win.blit(s, (6, 46))
    pygame.draw.rect(win, GRAY, border_rect, 6, border_radius=18)

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(win, GREEN, [x[0], x[1], snake_block, snake_block], border_radius=3)

def draw_food(x, y, color):
    pygame.draw.ellipse(win, color, [x, y, snake_block, snake_block])
    highlight = (255, 255, 255)
    pygame.draw.ellipse(win, highlight, [x+2, y+2, snake_block//3, snake_block//3])

def draw_banner(score, level):
    pygame.draw.rect(win, BANNER, [0, 0, WIDTH, 46])
    pygame.draw.line(win, BANNER_LINE, (0, 46), (WIDTH, 46), 2)
    title = font_style.render("SNAKE NOKIA HAND", True, (0, 255, 180))
    win.blit(title, (WIDTH//2 - title.get_width()//2, 8))
    score_text = font_small.render(f"SCORE: {score}", True, WHITE)
    level_text = font_small.render(f"LEVEL: {level}", True, WHITE)
    win.blit(score_text, (30, 14))
    win.blit(level_text, (WIDTH - 170, 14))

def draw_text_center(msg, color, y_offset=0, font=None):
    if font is None:
        font = font_style
    mesg = font.render(msg, True, color)
    shadow = font.render(msg, True, SHADOW)
    rect = mesg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    win.blit(shadow, (rect.x+2, rect.y+2))
    win.blit(mesg, rect)

def next_level_screen(level):
    win.fill(BLACK)
    draw_borders()
    draw_text_center(f"LEVEL {level}", GREEN)
    pygame.display.update()
    pygame.time.delay(1200)

def play_sound(filename):
    try:
        # Full path to sound file in sound folder
        full_path = os.path.join(SOUND_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"❌ Sound file not found: {full_path}")
            return
        
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(1.0)
        sound.play()
        print(f"🔊 Playing sound: {filename}")
    except Exception as e:
        print(f"❌ Error playing sound {filename}: {e}")

def play_music(filename):
    try:
        # Full path to music file in sound folder
        full_path = os.path.join(SOUND_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"❌ Music file not found: {full_path}")
            return
        
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(-1)
        print(f"🎵 Playing music: {filename}")
    except Exception as e:
        print(f"❌ Error playing music {filename}: {e}")

def detect_hand_gesture(results):
    if not results or not results.multi_hand_landmarks:
        return None
    hand_landmarks = results.multi_hand_landmarks[0]
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    for i, tip_id in enumerate(tips_ids):
        if i == 0:  # pouce
            if hand_landmarks.landmark[tip_id].x < hand_landmarks.landmark[tip_id - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
    if sum(fingers) >= 4:
        return 'open'
    if sum(fingers) == 0:
        return 'fist'
    return None

def get_random_food_color():
    colors = [
        (255, 0, 0),    # Rouge
        (255, 255, 0),  # Jaune
        (0, 0, 255),    # Bleu
        (255, 128, 0),  # Orange
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (128, 0, 255),  # Violet
    ]
    return random.choice(colors)

def game_over_screen(score, cap, hands):
    win.fill(BLACK)
    draw_borders()
    draw_text_center("GAME OVER", RED, y_offset=-40)
    score_text = font_style.render(f"FINAL SCORE: {score}", True, WHITE)
    rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    shadow = font_style.render(f"FINAL SCORE: {score}", True, SHADOW)
    win.blit(shadow, (rect.x+2, rect.y+2))
    win.blit(score_text, rect)

    btn_width, btn_height = 200, 60
    btn_replay = pygame.Rect(WIDTH//2 - btn_width - 30, HEIGHT//2 + 80, btn_width, btn_height)
    btn_quit = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 80, btn_width, btn_height)
    pygame.draw.rect(win, SHADOW, btn_replay.move(4,4), border_radius=12)
    pygame.draw.rect(win, SHADOW, btn_quit.move(4,4), border_radius=12)
    pygame.draw.rect(win, GREEN, btn_replay, border_radius=12)
    pygame.draw.rect(win, RED, btn_quit, border_radius=12)
    txt_replay = font_style.render("REJOUER", True, BLACK)
    txt_quit = font_style.render("QUITTER", True, BLACK)
    win.blit(txt_replay, (btn_replay.x + 30, btn_replay.y + 15))
    win.blit(txt_quit, (btn_quit.x + 40, btn_quit.y + 15))
    pygame.display.update()

    play_sound("gameover.wav")
    pygame.mixer.music.stop()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        try:
            success, img = cap.read()
            if not success:
                break
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            gesture = detect_hand_gesture(results)
            if gesture == 'open':
                play_sound("start.wav")
                return True
            elif gesture == 'fist':
                play_sound("quit.wav")
                pygame.quit()
                sys.exit()
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame = np.rot90(frame)
            frame_surface = pygame.surfarray.make_surface(frame)
            draw_gradient_background()
            win.blit(frame_surface, (0, 0))
            draw_borders()
            draw_text_center("GAME OVER", RED, y_offset=-40)
            win.blit(shadow, (rect.x+2, rect.y+2))
            win.blit(score_text, rect)
            pygame.draw.rect(win, SHADOW, btn_replay.move(4,4), border_radius=12)
            pygame.draw.rect(win, SHADOW, btn_quit.move(4,4), border_radius=12)
            pygame.draw.rect(win, GREEN, btn_replay, border_radius=12)
            pygame.draw.rect(win, RED, btn_quit, border_radius=12)
            win.blit(txt_replay, (btn_replay.x + 30, btn_replay.y + 15))
            win.blit(txt_quit, (btn_quit.x + 40, btn_quit.y + 15))
            pygame.display.update()
            clock.tick(10)
        except Exception as e:
            print(f"Error in game over screen: {e}")
            break

def gameLoop():
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Print debug info
    print(f"📁 Current directory: {SCRIPT_DIR}")
    print(f"🎵 Sound directory: {SOUND_DIR}")
    if os.path.exists(SOUND_DIR):
        print(f"📋 Sound files found: {os.listdir(SOUND_DIR)}")
    else:
        print(f"❌ Sound folder not found at: {SOUND_DIR}")
    
    x, y = WIDTH // 2, HEIGHT // 2
    snake_list = []
    length_of_snake = 3
    score = 0
    level = 1
    max_level = 5
    snake_speed_local = snake_speed

    foodx = round(random.randrange(12, WIDTH - snake_block - 12) / 10.0) * 10.0
    foody = round(random.randrange(52, HEIGHT - snake_block - 12) / 10.0) * 10.0
    food_color = get_random_food_color()

    direction = "RIGHT"
    direction_cooldown = 0
    COOLDOWN_FRAMES = 5

    play_sound("start.wav")
    play_music(LEVEL_MUSICS[level-1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        # --- Hand direction detection ---
        if results and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                wrist = hand_landmarks.landmark[0]
                index_tip = hand_landmarks.landmark[8]

                vx = index_tip.x - wrist.x
                vy = index_tip.y - wrist.y
                threshold = 0.08

                if direction_cooldown == 0:
                    if abs(vx) > abs(vy):
                        if vx > threshold and direction != "LEFT":
                            direction = "RIGHT"
                            direction_cooldown = COOLDOWN_FRAMES
                        elif vx < -threshold and direction != "RIGHT":
                            direction = "LEFT"
                            direction_cooldown = COOLDOWN_FRAMES
                    else:
                        if vy > threshold and direction != "UP":
                            direction = "DOWN"
                            direction_cooldown = COOLDOWN_FRAMES
                        elif vy < -threshold and direction != "DOWN":
                            direction = "UP"
                            direction_cooldown = COOLDOWN_FRAMES

        if direction_cooldown > 0:
            direction_cooldown -= 1

        # Draw background + camera
        draw_gradient_background()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)
        win.blit(frame_surface, (0, 0))

        draw_borders()
        draw_banner(score, level)

        # Snake movement
        if direction == "RIGHT":
            x += snake_block
        elif direction == "LEFT":
            x -= snake_block
        elif direction == "UP":
            y -= snake_block
        elif direction == "DOWN":
            y += snake_block

        # Wrap around screen
        if x < 12:
            x = WIDTH - snake_block - 12
        elif x > WIDTH - snake_block - 12:
            x = 12
        if y < 52:
            y = HEIGHT - snake_block - 12
        elif y > HEIGHT - snake_block - 12:
            y = 52

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Collision with self
        if snake_head in snake_list[:-1]:
            replay = game_over_screen(score, cap, hands)
            if replay:
                return gameLoop()
            else:
                break

        draw_snake(snake_block, snake_list)
        draw_food(foodx, foody, food_color)
        pygame.display.update()

        # Food eaten
        snake_rect = pygame.Rect(x, y, snake_block, snake_block)
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)
        if snake_rect.colliderect(food_rect):
            play_sound("eat.wav")
            foodx = round(random.randrange(12, WIDTH - snake_block - 12) / 10.0) * 10.0
            foody = round(random.randrange(52, HEIGHT - snake_block - 12) / 10.0) * 10.0
            food_color = get_random_food_color()
            length_of_snake += 1 + level
            score += 5

            # Next level every 5 foods
            if (score // 5) % 5 == 0 and level < max_level:
                level += 1
                snake_speed_local += 2
                play_sound("levelup.wav")
                play_music(LEVEL_MUSICS[level-1])
                next_level_screen(level)
            elif level == max_level and (score // 5) % 5 == 0:
                # Win game
                win.fill(BLACK)
                draw_borders()
                draw_text_center("CONGRATULATIONS!", (0,255,0), y_offset=-40)
                draw_text_center(f"FINAL SCORE: {score}", WHITE, y_offset=30, font=font_small)
                pygame.display.update()
                play_sound("win.wav")
                pygame.mixer.music.stop()
                pygame.time.delay(4000)
                cap.release()
                pygame.quit()
                sys.exit()

        clock.tick(snake_speed_local)

    cap.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    gameLoop()