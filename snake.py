import pygame
import sys
import random
import json

from pause import pause_menu  # Подключаем меню паузы
from death_screen import death_screen  # Подключаем экран смерти

pygame.init()

# Константы экрана
WIDTH, HEIGHT = 1080, 720
CELL_SIZE = 20
FPS = 12

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Звуки
SETTINGS_FILE = "settings.json"

def load_music(file, volume):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)  # Настройка громкости
    pygame.mixer.music.play(-1)  # Воспроизведение бесконечно

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
fade_sound = pygame.mixer.Sound('src/casual-click-pop-ui-7-262127.mp3')
fade_sound.set_volume(sfx_volume)

pygame.mixer.init()
eat_sound = pygame.mixer.Sound('src/eat_sound.mp3')
crash_sound = pygame.mixer.Sound('src/game_over.mp3')
def play_game_over_music():
    pygame.mixer.music.load('src/game_over_bg.mp3')
    pygame.mixer.music.play(-1)

# Фон
background_image = pygame.image.load('src/background.jpg')  # Файл с текстурой фона
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Змейка и еда
def init_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = generate_food(snake)
    return snake, direction, food

# Улучшение рендеринга
def render_snake(snake):
    for index, segment in enumerate(snake):
        shade = 50 + index * 10  # Постепенное затемнение хвоста
        color = (0, 255 - shade, 0)
        pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)  # Рамка

def render_score(score):
    font = pygame.font.Font('src/PixelFont.ttf', 36)
    score_text = font.render(f"СЧЕТ: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def blink_snake(snake, duration=2000, interval=100):
    """
    Эффект мигания змейки перед экраном смерти.
    :param snake: Список сегментов змейки.
    :param duration: Общее время мигания в миллисекундах.
    :param interval: Интервал между миганиями в миллисекундах.
    """
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(background_image, (0, 0))  # Рендеринг фона

        # Переключение видимости
        if (pygame.time.get_ticks() // interval) % 2 == 0:
            render_snake(snake)  # Показываем змейку

        pygame.display.flip()
        pygame.time.delay(interval // 2)  # Задержка для эффекта

# Загрузка изображений фруктов (увеличиваем размер в 2 раза)
fruit_images = [
    pygame.image.load('src/apple.png'),
    pygame.image.load('src/banana.png'),
    pygame.image.load('src/pear.png'),
    pygame.image.load('src/pineapple.png')
]
fruit_images = [pygame.transform.scale(img, (CELL_SIZE * 2, CELL_SIZE * 2)) for img in fruit_images]

# Функция для генерации еды
def generate_food(snake):
    """
    Генерация случайного расположения и типа еды.
    :param snake: Текущие координаты змейки.
    :return: Координаты еды и её тип.
    """
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            fruit_type = random.choice(fruit_images)  # Выбор случайного фрукта
            return (x, y), fruit_type

# Функция рендеринга еды
def render_food(food):
    """
    Рендеринг еды на экране.
    :param food: Кортеж из координат еды и её изображения.
    """
    position, fruit_image = food
    # Смещаем изображение еды на пол клетки, чтобы выровнять центр
    offset_x = CELL_SIZE // 2
    offset_y = CELL_SIZE // 2
    screen.blit(fruit_image, (position[0] - offset_x, position[1] - offset_y))

# Основной игровой цикл
def game_loop():
    clock = pygame.time.Clock()
    snake, direction, food = init_game()
    score = 0

    pygame.mixer.music.load('src/background_music.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                elif event.key == pygame.K_ESCAPE:
                    
                    
                    
                    
                    action = pause_menu(screen)
                    if action == "exit":
                        pygame.quit()
                        sys.exit()
                    elif action == "main_menu":
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('src/loop-menu-preview-109594.mp3')
                        pygame.mixer.music.play(-1)
                        return

        # Движение змейки
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Проверка на столкновение
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT) or new_head in snake:
            pygame.mixer.music.pause()
            crash_sound.play()
            blink_snake(snake)  # Эффект мигания
            pygame.time.delay(800)
            action = death_screen(screen, clock)
            if action == "restart":
                pygame.mixer.music.stop()
                return game_loop()
            elif action == "main_menu":
                pygame.mixer.music.stop()
                load_music('src/loop-menu-preview-109594.mp3', music_volume)
                return

        # Проверка на еду
        if new_head == food[0]:
            score += 1
            food = generate_food(snake)  # Случайный фрукт
            eat_sound.play()
        else:
            snake.pop()

        snake.insert(0, new_head)

        # Рендеринг
        screen.blit(background_image, (0, 0))  # Рендеринг фона
        render_snake(snake)
        render_food(food)
        render_score(score)

        pygame.display.flip()
        clock.tick(FPS)

# Основное меню игры
def main():
    while True:
        game_loop()

if __name__ == "__main__":
    main()
