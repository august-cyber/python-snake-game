import pygame
import sys
import math
import json  # для сохранения и загрузки настроек
from snake import game_loop

pygame.init()

# Константы экрана
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Загрузка пиксельного шрифта
font_pixel = pygame.font.Font('src/PixelFont.ttf', 30)  # Загружаем пиксельный шрифт

# Заголовок шрифт
title_font = pygame.font.Font('src/PixelFont.ttf', 150)  # Увеличенный заголовок пиксельного шрифта

# Звуковые эффекты
pygame.mixer.init()
click_sound = pygame.mixer.Sound('src/casual-click-pop-ui-1-262118.mp3')
game_start_click = pygame.mixer.Sound('src/game-start-6104.mp3')

# Файл для сохранения настроек громкости
SETTINGS_FILE = "settings.json"

# Кнопка класс
class Button:
    def __init__(self, text, pos, width, height, color_active=RED, color_idle=WHITE):
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
        text_surf = font_pixel.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def check_click(self, event):
        if self.rect.collidepoint(event.pos):
            click_sound.play()  # Играть звук при нажатии
            return True
        return False

# Фоновое движение
def dynamic_background():
    time_elapsed = pygame.time.get_ticks() * 0.002
    red = int(80 + 70 * math.sin(time_elapsed))
    green = int(70 + 70 * math.sin(time_elapsed + 2))
    blue = int(90 + 70 * math.sin(time_elapsed + 4))
    return (red, green, blue)

# Звуковая настройка
def load_music(file, volume):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)  # Настройка громкости
    pygame.mixer.music.play(-1)  # Воспроизведение бесконечно

# Загрузка настроек громкости из файла
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'music_volume': 0.5 , 'sfx_volume': 0.5}  # Default values

# Сохранение настроек громкости в файл
def save_settings(music_volume, sfx_volume):
    settings = {'music_volume': music_volume, 'sfx_volume': sfx_volume}
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

# Кнопки
start_button = Button("СТАРТ", (WIDTH // 2 - 200, HEIGHT // 2 - 120), 400, 75)
settings_button = Button("НАСТРОЙКИ", (WIDTH // 2 - 200, HEIGHT // 2 - 40), 400, 75)
achievements_button = Button("ДОСТИЖЕНИЯ", (WIDTH // 2 - 200, HEIGHT // 2 + 40), 400, 75)
exit_button = Button("ВЫХОД", (WIDTH // 2 - 200, HEIGHT // 2 + 120), 400, 75)

def settings_menu():
    running_settings = True
    settings = load_settings()
    volume_music = settings['music_volume']
    volume_sfx = settings['sfx_volume']
    volume_slider_width = 300
    volume_slider_height = 20

    music_slider_rect = pygame.Rect(WIDTH // 2 - volume_slider_width // 2, HEIGHT // 2 - 100, volume_slider_width, volume_slider_height)
    sfx_slider_rect = pygame.Rect(WIDTH // 2 - volume_slider_width // 2, HEIGHT // 2, volume_slider_width, volume_slider_height)

    back_button = Button("Назад", (WIDTH // 2 - 150, HEIGHT // 2 + 100), 300, 50)

    dragging_music = False
    dragging_sfx = False

    while running_settings:
        screen.fill(dynamic_background())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_click(event):
                    running_settings = False
                elif music_slider_rect.collidepoint(event.pos):
                    dragging_music = True
                elif sfx_slider_rect.collidepoint(event.pos):
                    dragging_sfx = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False
                dragging_sfx = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_settings = False

        if dragging_music:
            mouse_x, _ = pygame.mouse.get_pos()
            volume_music = (mouse_x - music_slider_rect.x) / music_slider_rect.width
            volume_music = max(0.0, min(1.0, volume_music))
            pygame.mixer.music.set_volume(volume_music)

        if dragging_sfx:
            mouse_x, _ = pygame.mouse.get_pos()
            volume_sfx = (mouse_x - sfx_slider_rect.x) / sfx_slider_rect.width
            volume_sfx = max(0.0, min(1.0, volume_sfx))
            click_sound.set_volume(volume_sfx)
            game_start_click.set_volume(sfx_volume)

        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)

        # Рисуем ползунки
        def draw_slider(slider_rect, fill_ratio, color):
            # Фон ползунка
            pygame.draw.rect(screen, (50, 50, 50), slider_rect, border_radius=10)
            # Заполненная часть
            fill_width = int(slider_rect.width * fill_ratio)
            fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
            pygame.draw.rect(screen, color, fill_rect, border_radius=10)
            # Хватка (ползунок-круг)
            grip_x = slider_rect.x + fill_width
            grip_y = slider_rect.y + slider_rect.height // 2
            pygame.draw.circle(screen, (200, 200, 200), (grip_x, grip_y), slider_rect.height // 2)

        draw_slider(music_slider_rect, volume_music, BLUE)
        draw_slider(sfx_slider_rect, volume_sfx, GREEN)

        # Надписи для ползунков
        music_text = font_pixel.render(f"Музыка: {int(volume_music * 100)}%", True, WHITE)
        sfx_text = font_pixel.render(f"Эффекты: {int(volume_sfx * 100)}%", True, WHITE)
        music_text_rect = music_text.get_rect(center=(music_slider_rect.centerx, music_slider_rect.y - 30))
        sfx_text_rect = sfx_text.get_rect(center=(sfx_slider_rect.centerx, sfx_slider_rect.y - 30))

        screen.blit(music_text, music_text_rect)
        screen.blit(sfx_text, sfx_text_rect)
        back_button.draw(screen)

        pygame.display.flip()

    # Сохранение настроек перед выходом из меню
    save_settings(volume_music, volume_sfx)
   
# Основной цикл
running = True

# Загрузка настроек перед запуском игры
settings = load_settings()
music_volume = settings['music_volume']
sfx_volume = settings['sfx_volume']

# Установка громкости музыки и эффектов
load_music('src/loop-menu-preview-109594.mp3', music_volume)
click_sound.set_volume(sfx_volume)
game_start_click.set_volume(sfx_volume)

while running:
    screen.fill(dynamic_background())  # Динамический фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.check_click(event):
                pygame.mixer.music.stop()
                click_sound.stop()
                game_start_click.play()

                pygame.mixer.music.stop()
                click_sound.stop()
                game_start_click.play()

                # Эффект затемнения
                fade_surface = pygame.Surface((WIDTH, HEIGHT))
                fade_surface.fill(BLACK)

                for alpha in range(0, 256, 5):  # Плавное увеличение прозрачности
                    fade_surface.set_alpha(alpha)
                    screen.fill(dynamic_background())  # Перерисовка фона
                    start_button.draw(screen)
                    settings_button.draw(screen)
                    achievements_button.draw(screen)
                    exit_button.draw(screen)
                    title_surf = title_font.render("ЗМЕЙКА", True, WHITE)
                    screen.blit(title_surf, title_rect)
                    screen.blit(fade_surface, (0, 0))  # Наложение затемняющего слоя
                    pygame.display.flip()
                    pygame.time.delay(30)  # Задержка для плавности эффекта
                
                game_loop()
                # Логика запуска игры или уровня
            elif settings_button.check_click(event):
                settings_menu()  # Вызов меню настроек
                # После возвращения из меню настроек обновляем громкость
                settings = load_settings()
                music_volume = settings['music_volume']
                sfx_volume = settings['sfx_volume']
                pygame.mixer.music.set_volume(music_volume)
                click_sound.set_volume(sfx_volume)
                game_start_click.set_volume(sfx_volume)
            elif achievements_button.check_click(event):
                print("ДОСТИЖЕНИЯ")
                # Вызвать окно достижений
            elif exit_button.check_click(event):
                pygame.time.delay(100)
                running = False  # Выход из игры

    # Обновление состояния кнопок
    mouse_pos = pygame.mouse.get_pos()
    start_button.check_hover(mouse_pos)
    settings_button.check_hover(mouse_pos)
    achievements_button.check_hover(mouse_pos)
    exit_button.check_hover(mouse_pos)

    # Рисование кнопок
    start_button.draw(screen)
    settings_button.draw(screen)
    achievements_button.draw(screen)
    exit_button.draw(screen)

    # Рисование заголовка "Змейка"
    title_surf = title_font.render("ЗМЕЙКА", True, WHITE)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 7))  # Высокое положение заголовка
    screen.blit(title_surf, title_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
