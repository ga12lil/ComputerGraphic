import pygame
from pygame.locals import *

# Настройки окна
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)  # Цвет фона (белый)
DRAW_COLOR = (0, 0, 0)  # Цвет рисования (черный)

def load_pattern(image_path):
    """Загружает изображение для заливки"""
    pattern_img = pygame.image.load(image_path)
    return pattern_img

def get_pattern_color(pattern, x, y, start_x, start_y):
    """Возвращает цвет паттерна с учетом смещения от точки начала заливки"""
    pattern_width, pattern_height = pattern.get_size()
    # Вычисляем смещение относительно точки начала заливки
    pattern_x = (x - start_x) % pattern_width
    pattern_y = (y - start_y) % pattern_height
    return pattern.get_at((pattern_x, pattern_y))

def fill_line_pattern(surface, pattern, x, y, target_color, start_x, start_y):
    """Алгоритм заливки строки пикселей с использованием паттерна"""
    width, height = surface.get_size()
    pixels = pygame.PixelArray(surface)

    # Если цвет пикселя не совпадает с целевым, не продолжаем заливку
    if surface.get_at((x, y))[:3] != target_color:
        return

    # Найдем границы строки для заливки
    left = x
    while left >= 0 and surface.get_at((left, y))[:3] == target_color:
        left -= 1
    left += 1

    right = x
    while right < width and surface.get_at((right, y))[:3] == target_color:
        right += 1
    right -= 1

    # Закрашиваем линию от left до right паттерном
    for i in range(left, right + 1):
        pattern_color = get_pattern_color(pattern, i, y, start_x, start_y)
        pixels[i, y] = pattern_color

    # Обрабатываем соседние строки
    if y > 0:
        for i in range(left, right + 1):
            if surface.get_at((i, y - 1))[:3] == target_color:
                fill_line_pattern(surface, pattern, i, y - 1, target_color, start_x, start_y)

    if y < height - 1:
        for i in range(left, right + 1):
            if surface.get_at((i, y + 1))[:3] == target_color:
                fill_line_pattern(surface, pattern, i, y + 1, target_color, start_x, start_y)

    del pixels

def flood_fill_pattern(surface, pattern, x, y):
    """Основная функция заливки с использованием паттерна"""
    target_color = surface.get_at((x, y))[:3]

    # Начинаем заливку с точки (x, y)
    fill_line_pattern(surface, pattern, x, y, target_color, x, y)

def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Рисование и заливка паттерном со смещением')
    clock = pygame.time.Clock()

    # Создаем поверхность для рисования
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_COLOR)

    # Загружаем паттерн
    pattern = load_pattern(r'C:\Users\mtz20\IdeaProjects\ComputerGraphic\lab 3\images.png')  # Путь к изображению паттерна

    drawing = False  # Флаг рисования
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши — начать рисование
                    drawing = True
                elif event.button == 3:  # Правая кнопка мыши — заливка паттерном
                    x, y = event.pos
                    flood_fill_pattern(canvas, pattern, x, y)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Отпустили левую кнопку мыши — завершить рисование
                    drawing = False
            elif event.type == MOUSEMOTION:
                if drawing:  # Если рисуем, то проводим линию
                    pygame.draw.circle(canvas, DRAW_COLOR, event.pos, 5)

        # Отображение на экране
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(60)

    # Сохраняем результат как изображение
    pygame.image.save(canvas, r'C:\Users\mtz20\IdeaProjects\ComputerGraphic\lab 3\output_image_with_pattern_offset.png')

    pygame.quit()

if __name__ == "__main__":
    main()
