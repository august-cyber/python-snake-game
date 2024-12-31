import pygame
import sys
import json

WIDTH, HEIGHT = 1080, 720

# Цвета
BG_COLOR = (142, 79, 13)
TEXT_COLOR = (250, 205, 49)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
HOVER_COLOR = (88, 84, 146)

# Шрифт
pygame.init()

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'music_volume': 0.5, 'sfx_volume': 0.5}

def save_settings(music_volume, sfx_volume):
    settings = {'music_volume': music_volume, 'sfx_volume': sfx_volume}
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

settings = load_settings()
music_volume = settings['music_volume']
sfx_volume = settings['sfx_volume']
settings = load_settings()
font = pygame.font.Font('src/PixelFont.ttf', 40)

pygame.mixer.init()
click_sound = pygame.mixer.Sound('src/casual-click-pop-ui-1-262118.mp3')

fade_sound = pygame.mixer.Sound('src/casual-click-pop-ui-7-262127.mp3')
fade_sound.set_volume(sfx_volume)

def music_volume_control():
    settings = load_settings()
    music_volume = settings['music_volume']
    sfx_volume = settings['sfx_volume']
    pygame.mixer.music.set_volume(music_volume)
    fade_sound.set_volume(sfx_volume)
    fade_sound.play()

def load_music(file, volume):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)  # Настройка громкости
    pygame.mixer.music.play(-1)  # Воспроизведение бесконечно

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

def pause_menu(screen):    
    resume_button = Button("Продолжить", (WIDTH // 2 - 200, HEIGHT // 2 - 120), 400, 75)
    main_menu_button = Button("Главное меню", (WIDTH // 2 - 200, HEIGHT // 2 - 40), 400, 75)
    achievements_button = Button("Достижения", (WIDTH // 2 - 200, HEIGHT // 2 + 40), 400, 75)
    exit_button = Button("Выход", (WIDTH // 2 - 200, HEIGHT // 2 + 120), 400, 75)

    buttons = [resume_button, main_menu_button, achievements_button, exit_button]
    paused = True

    pygame.mixer.music.pause()
    
    while paused:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Возврат из паузы через Esc
                    pygame.mixer.music.unpause()
                    return "resume"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.check_click(event):
                    pygame.mixer.music.unpause()
                    return "resume"
                elif main_menu_button.check_click(event):
                    
                    music_volume_control()
                    
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
                elif achievements_button.check_click(event):
                    print("Открыть достижения")  # Логика достижения
                elif exit_button.check_click(event):
                    return "exit"

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
