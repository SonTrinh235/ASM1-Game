import pygame
import sys
import settings 
import random
from objects import Zombie, Button 

pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("BTL1: Whack-a-Miku")
clock = pygame.time.Clock()

try:
    font_title = pygame.font.Font(settings.FONT_PATH, 50)
    font_tos_title = pygame.font.Font(settings.FONT_PATH, 40)
    font_game = pygame.font.Font(settings.FONT_PATH, 24)
    font_text = pygame.font.Font(settings.FONT_PATH, 20) 
except:
    print(f"Lỗi font: {settings.FONT_PATH}. Dùng Arial mặc định.")
    font_title = pygame.font.SysFont('Arial', 50, bold=True)
    font_tos_title = pygame.font.SysFont('Arial', 40, bold=True)
    font_game = pygame.font.SysFont('Arial', 24, bold=True)
    font_text = pygame.font.SysFont('Arial', 20) 

game_settings = { "difficulty": "Normal", "sound_on": True, "diff_offset": 0 }

def load_image(path, scale=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale: img = pygame.transform.scale(img, scale)
        return img
    except: return None

bg_img = load_image('assets/images/background.png', (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
hammer_idle = load_image('assets/images/hammer_idle.png', (80, 80))
hammer_smash = load_image('assets/images/hammer_smash.png', (80, 80))

try: hit_sound = pygame.mixer.Sound('assets/sounds/hit.ogg')
except: hit_sound = None

Zombie.sprites = {
    'normal': load_image('assets/images/miku_idle.png', (100, 100)),
    'smashed': load_image('assets/images/miku_smashed.png', (100, 100))
}

def draw_custom_mouse(surface, is_clicking=False):
    mx, my = pygame.mouse.get_pos()
    current_hammer = hammer_smash if is_clicking else hammer_idle
    if current_hammer:
        surface.blit(current_hammer, (mx - 40, my - 40))
    else:
        color = settings.RED if is_clicking else settings.WHITE
        pygame.draw.circle(surface, color, (mx, my), 10)
        pygame.draw.circle(surface, settings.BLACK, (mx, my), 10, 1)

def tos_screen():
    running = True
    agree_w = 220
    agree_h = 60
    center_a_x = 150 + agree_w // 2 
    center_a_y = 530 + agree_h // 2
    disagree_w = 220
    disagree_h = 60
    
    b_positions = [
        (450, 530), 
        (50, 150), 
        (500, 150), 
        (50, 550),  
        (280, 100),
        (450, 640),
        (400, 640),
        (750, 840)
    ]

    disagree_levels = [
        "khong dong tinh", 
        "Chắc chắn chứ", 
        "Nghĩ kỹ chưa", 
        "100% chắc chắn à", 
        "Ấn nút kia i", 
        "Ấn nút kia i mò",
        "Không đc đou",
        "Ehe"
    ]
    current_level = 0 

    while running:
        screen.fill(settings.BLUE_PASTEL)
        if bg_img: screen.blit(bg_img, (0, 0))

        paper_rect = pygame.Rect(100, 80, 600, 540)
        pygame.draw.rect(screen, settings.WHITE, paper_rect, border_radius=10)
        pygame.draw.rect(screen, settings.HOLE_COLOR, paper_rect, 3, border_radius=10)

        title = font_tos_title.render("ĐIỀU KHOẢN SỬ DỤNG", True, settings.HOLE_COLOR)
        screen.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 110))

        start_y = 180
        for line in settings.TOS_CONTENT:
            text_surf = font_game.render(line, True, settings.BLACK)
            screen.blit(text_surf, (settings.SCREEN_WIDTH//2 - text_surf.get_width()//2, start_y))
            start_y += 40

        mx, my = pygame.mouse.get_pos()
        is_clicking = False
        pos_idx = min(current_level, len(b_positions) - 1)
        disagree_x, disagree_y = b_positions[pos_idx]
        text_idx = min(current_level, len(disagree_levels) - 1)
        btn_text = disagree_levels[text_idx]
        
        btn_disagree = Button(btn_text, disagree_x, disagree_y, disagree_w, disagree_h, color=(200, 100, 100))

        current_a_x = center_a_x - agree_w // 2
        current_a_y = center_a_y - agree_h // 2
        btn_agree = Button("toi dong tinh", current_a_x, current_a_y, agree_w, agree_h, color=settings.GREEN)

        btn_disagree.draw(screen, (mx, my)) 
        btn_agree.draw(screen, (mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
                    
                    if btn_agree.is_clicked((mx, my)):
                        running = False
                    
                    elif btn_disagree.is_clicked((mx, my)):
                        current_level += 1 
                        
                        agree_w *= 1.4
                        agree_h *= 1.4
                        
                        center_a_x += (settings.SCREEN_WIDTH//2 - center_a_x) * 0.25
                        center_a_y += (settings.SCREEN_HEIGHT//2 - center_a_y) * 0.25
                        

        draw_custom_mouse(screen, is_clicking)
        pygame.display.flip()
        clock.tick(settings.FPS)

def settings_menu():
    running = True
    while running:
        screen.fill(settings.BLUE_PASTEL)
        if bg_img: screen.blit(bg_img, (0, 0))

        s = pygame.Surface((400, 300)); s.set_alpha(200); s.fill(settings.WHITE)
        screen.blit(s, (200, 200))

        title = font_title.render("CÀI ĐẶT", True, settings.HOLE_COLOR)
        screen.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 100))

        mx, my = pygame.mouse.get_pos(); is_clicking = False
        
        sound_text = "Âm thanh: BẬT" if game_settings["sound_on"] else "Âm thanh: TẮT"
        btn_sound = Button(sound_text, 250, 250, 300, 50)
        btn_back = Button("Quay Lại", 250, 350, 300, 50, color=(200, 200, 200))

        btn_sound.draw(screen, (mx, my)); btn_back.draw(screen, (mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
                    if btn_sound.is_clicked((mx, my)):
                        game_settings["sound_on"] = not game_settings["sound_on"]
                        if hit_sound: hit_sound.set_volume(1.0 if game_settings["sound_on"] else 0.0)
                    if btn_back.is_clicked((mx, my)): running = False

        draw_custom_mouse(screen, is_clicking)
        pygame.display.flip()
        clock.tick(settings.FPS)

def game_loop():
    zombies = [Zombie(settings.START_X + c * settings.GAP_X, settings.START_Y + r * settings.GAP_Y) 
               for r in range(3) for c in range(3)]
    score = 0; missed = 0; is_smashing = False; timer_spawn = 0
    if hit_sound: hit_sound.set_volume(1.0 if game_settings["sound_on"] else 0.0)

    running = True
    while running:
        base_diff = min(score // 5, 10) 
        total_diff = base_diff + game_settings["diff_offset"]
        spawn_rate = max(10, 60 - total_diff * 3) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_smashing = True; hit_success = False; mouse_pos = pygame.mouse.get_pos()
                    for z in reversed(zombies): 
                        if z.check_click(mouse_pos):
                            score += 1; hit_success = True
                            if hit_sound and game_settings["sound_on"]: hit_sound.play()
                            break 
                    if not hit_success: missed += 1
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: is_smashing = False

        timer_spawn += 1
        if timer_spawn >= spawn_rate:
            timer_spawn = 0
            available = [z for z in zombies if z.state == 0]
            if available: random.choice(available).popup(total_diff)

        for z in zombies: z.update()

        if bg_img: screen.blit(bg_img, (0, 0))
        else: screen.fill(settings.BLUE_PASTEL)

        s = pygame.Surface((settings.SCREEN_WIDTH, 50)); s.set_alpha(128); s.fill(settings.BLACK) 
        screen.blit(s, (0,0))
        
        mode_vi = "Thường"
        if game_settings['difficulty'] == "Easy": mode_vi = "Dễ"
        elif game_settings['difficulty'] == "Hard": mode_vi = "Khó"
        
        info = f"Điểm: {score} | Trượt: {missed} | Độ khó: {mode_vi} (ESC để thoát)"
        screen.blit(font_game.render(info, True, settings.WHITE), (20, 10))

        for z in zombies: z.draw(screen)
        draw_custom_mouse(screen, is_smashing)
        pygame.display.flip(); clock.tick(settings.FPS)

def main_menu():
    while True:
        screen.fill(settings.BLUE_PASTEL)
        if bg_img: screen.blit(bg_img, (0, 0))

        title = font_title.render("MIKU WHACK-A-MOLE", True, settings.WHITE)
        screen.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 90))

        mx, my = pygame.mouse.get_pos(); is_clicking = False
        
        diff_vi = "Thường"
        if game_settings['difficulty'] == "Easy": diff_vi = "Dễ"
        elif game_settings['difficulty'] == "Hard": diff_vi = "Khó"

        btn_start = Button("BẮT ĐẦU", 250, 200, 300, 60, color=settings.GREEN)
        btn_diff = Button(f"Độ khó: {diff_vi}", 250, 280, 300, 60, color=settings.YELLOW)
        btn_sets = Button("CÀI ĐẶT", 250, 360, 300, 60)
        btn_exit = Button("THOÁT GAME", 250, 440, 300, 60, color=(200, 100, 100))

        for b in [btn_start, btn_diff, btn_sets, btn_exit]: b.draw(screen, (mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
                    if btn_start.is_clicked((mx, my)): game_loop()
                    elif btn_diff.is_clicked((mx, my)):
                        if game_settings["difficulty"] == "Easy":
                            game_settings["difficulty"] = "Normal"; game_settings["diff_offset"] = 0
                        elif game_settings["difficulty"] == "Normal":
                            game_settings["difficulty"] = "Hard"; game_settings["diff_offset"] = 5
                        else:
                            game_settings["difficulty"] = "Easy"; game_settings["diff_offset"] = -3
                    elif btn_sets.is_clicked((mx, my)): settings_menu()
                    elif btn_exit.is_clicked((mx, my)): pygame.quit(); sys.exit()

        draw_custom_mouse(screen, is_clicking)
        pygame.display.flip(); clock.tick(settings.FPS)

if __name__ == "__main__":
    tos_screen()
    main_menu()