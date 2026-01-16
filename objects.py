import pygame
import settings

pygame.font.init()

try:
    font_btn = pygame.font.Font(settings.FONT_PATH, 28)
except:
    print("Lỗi: Không tìm thấy Font! Đang dùng Arial mặc định.")
    font_btn = pygame.font.SysFont('Arial', 28, bold=True)

class Button:
    def __init__(self, text, x, y, width, height, color=settings.WHITE, hover_color=settings.PINK_PASTEL):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        
    def draw(self, surface, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, settings.BLACK, self.rect, 2, border_radius=15)
        
        text_surf = font_btn.render(self.text, True, settings.BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Zombie:
    sprites = {} 
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.state = 0; self.y_offset = 100; self.rise_speed = 5 
        self.wait_time = 0; self.max_wait_time = 60; self.smashed_time = 0 

    def popup(self, difficulty_multiplier):
        if self.state == 0:
            self.state = 1; self.y_offset = 100
            self.rise_speed = 5 + difficulty_multiplier
            self.max_wait_time = max(20, 60 - difficulty_multiplier * 2)

    def hit(self):
        self.state = 4; self.smashed_time = 15; return True

    def update(self):
        if self.state == 1:
            self.y_offset -= self.rise_speed
            if self.y_offset <= 0: self.y_offset = 0; self.state = 2; self.wait_time = 0
        elif self.state == 2:
            self.wait_time += 1
            if self.wait_time > self.max_wait_time: self.state = 3 
        elif self.state == 3:
            self.y_offset += self.rise_speed
            if self.y_offset >= 100: self.y_offset = 100; self.state = 0 
        elif self.state == 4:
            self.smashed_time -= 1
            if self.smashed_time <= 0: self.state = 3; self.rise_speed = 10 

    def draw(self, surface):
        hole_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 70, 80, 30)
        pygame.draw.ellipse(surface, settings.HOLE_COLOR, hole_rect)
        if self.state != 0:
            clip_rect = pygame.Rect(self.rect.x, self.rect.y, 100, 100)
            surface.set_clip(clip_rect)
            draw_y = self.rect.y + self.y_offset
            current_img = Zombie.sprites.get('smashed') if self.state == 4 else Zombie.sprites.get('normal')
            if current_img: surface.blit(current_img, (self.rect.x, draw_y))
            else:
                color = settings.YELLOW if self.state == 4 else settings.GREEN
                pygame.draw.circle(surface, color, (self.rect.x + 50, draw_y + 50), 45)
            surface.set_clip(None)

    def check_click(self, mouse_pos):
        if self.state in [1, 2, 3]:
            visible_rect = pygame.Rect(self.rect.x, self.rect.y + self.y_offset, 100, 100 - self.y_offset)
            if visible_rect.collidepoint(mouse_pos): return self.hit()
        return False