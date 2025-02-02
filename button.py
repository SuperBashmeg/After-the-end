import math

from config import *

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.size_timer = 0
        self.max_size_timer = 0.5

    def draw(self, screen):
        current_color = self.hover_color if self.hovered else self.color
        # if self.hovered:
        #     pygame.draw.rect(screen, current_color, pygame.Rect(self.rect.x-self.rect.width*0.1, self.rect.y, self.rect.width*1.2, self.rect.height), 0, 4)
        # else:
        pygame.draw.rect(screen, current_color, self.rect, 0, 4)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, dt):
        if self.hovered:
            if self.size_timer < self.max_size_timer:
                self.size_timer += dt
            elif self.size_timer > self.max_size_timer:
                self.size_timer = -0.05
        else:
            if self.size_timer > 0:
                self.size_timer -= dt
            elif self.size_timer < 0:
                self.size_timer = 0
        self.rect.width = round(self.base_rect.width + 10 * math.sin(self.size_timer * math.pi / self.max_size_timer))
        self.rect.height = round(self.base_rect.height + 10 * math.sin(self.size_timer * math.pi / self.max_size_timer))
        self.rect.x = self.base_rect.x - (self.rect.width - self.base_rect.width) // 2
        self.rect.y = self.base_rect.y - (self.rect.height - self.base_rect.height) // 2

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.hovered and mouse_pressed[0]