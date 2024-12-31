import pygame
import sys

from settings import sfx_volume

WIDTH, HEIGHT = 1080, 720

# Цвета
BG_COLOR = (142, 79, 13)
BLACK = (0, 0, 0)
TEXT_COLOR = (250, 205, 49)
WHITE = (255, 255, 255)
HOVER_COLOR = (88, 84, 146)

# Шрифт
pygame.init()
font = pygame.font.Font('src/PixelFont.ttf', 40)
large_font = pygame.font.Font('src/PixelFont.ttf', 150)

# Звуковые эффекты
pygame.mixer.init()
click_sound = pygame.mixer.Sound('src/casual-click-pop-ui-1-262118.mp3')

def play_game_over_music():
    pygame.mixer.music.load('src/game_over_bg.mp3')
    pygame.mixer.music.play(-1)

class Button:
    def __init__(self, text, pos, width, height, color_active=HOVER_COLOR, color_idle=WHITE):
        self.text = text
        self.pos = pos
        self.width = width
        self.height = height
        self.color_active = color_active
        self.color_idle = color_idle
        self.rect = pygame.Rect(pos, (width, height))
        self.is_hovered = False

    def draw(self, screen):
        color = self.color_active if self.is_hovered else self.color_idle
        pygame.draw.rect(screen, color, self.rect, 0 if self.is_hovered else 2)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, event):
        if self.rect.collidepoint(event.pos):
            click_sound.play()  # Играть звук при нажатии
            return True
        return False

click_sound.set_volume(sfx_volume)

def death_screen(screen, clock):
    """Экран смерти с улучшенным функционалом."""
    play_game_over_music()

    restart_button = Button("ПЕРЕЗАПУСТИТЬ", (WIDTH // 2 - 200, HEIGHT // 2 - 40), 400, 75)
    menu_button = Button("В МЕНЮ", (WIDTH // 2 - 200, HEIGHT // 2 + 40), 400, 75)
    exit_button = Button("ВЫХОД", (WIDTH // 2 - 200, HEIGHT // 2 + 120), 400, 75)

    buttons = [restart_button, menu_button, exit_button]
    running = True

    while running:
        screen.fill(BG_COLOR)

        # Рендер заголовка
        game_over_text = large_font.render("GAME OVER", True, TEXT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(game_over_text, game_over_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.check_click(event):
                    pygame.mixer.music.stop()
                    
                    fade_surface = pygame.Surface((WIDTH, HEIGHT))
                    fade_surface.fill(BLACK)

                    for alpha in range(0, 256, 5):  # Плавное увеличение прозрачности
                        fade_surface.set_alpha(alpha)
                        screen.fill(BG_COLOR)  # Перерисовка фона паузы
                        for button in buttons:
                            button.draw(screen)  # Отображение кнопок
                        screen.blit(fade_surface, (0, 0))  # Наложение затемняющего слоя
                        pygame.display.flip()
                        pygame.time.delay(15)  # Задержка для плавности эффекта
                    
                    return "restart"
                elif menu_button.check_click(event):
                    pygame.mixer.music.stop()
                    
                    fade_surface = pygame.Surface((WIDTH, HEIGHT))
                    fade_surface.fill(BLACK)

                    for alpha in range(0, 256, 5):  # Плавное увеличение прозрачности
                        fade_surface.set_alpha(alpha)
                        screen.fill(BG_COLOR)  # Перерисовка фона паузы
                        for button in buttons:
                            button.draw(screen)  # Отображение кнопок
                        screen.blit(fade_surface, (0, 0))  # Наложение затемняющего слоя
                        pygame.display.flip()
                        pygame.time.delay(15)  # Задержка для плавности эффекта
                    
                    
                    return "main_menu"
                elif exit_button.check_click(event):
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
