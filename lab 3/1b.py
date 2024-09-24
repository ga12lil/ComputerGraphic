import pygame
from pygame.locals import *
from PIL import Image

# Настройки окна
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)  # Цвет фона (белый)
DRAW_COLOR = (0, 0, 0)  # Цвет рисования (черный)

def load_pattern(image_path):
    """Загружает изображение для заливки"""
    pattern_img = pygame.image.load(image_path)
    return pattern_img

def get_pattern_color(pattern, x, y):
    """Возвращает цвет паттерна с координатами x, y, повторяясь циклически"""
    pattern_width, pattern_height = pattern.get_size()
    # Координаты в пределах изображения паттерна (циклично)
    pattern_x = x % pattern_width
    pattern_y = y % pattern_height
    return pattern.get_at((pattern_x, pattern_y))

def fill_line_pattern(surface, pattern, x, y, target_color):
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
        pattern_color = get_pattern_color(pattern, i, y)
        pixels[i, y] = pattern_color

    # Обрабатываем соседние строки
    if y > 0:
        for i in range(left, right + 1):
            if surface.get_at((i, y - 1))[:3] == target_color:
                fill_line_pattern(surface, pattern, i, y - 1, target_color)

    if y < height - 1:
        for i in range(left, right + 1):
            if surface.get_at((i, y + 1))[:3] == target_color:
                fill_line_pattern(surface, pattern, i, y + 1, target_color)

    del pixels

def flood_fill_pattern(surface, pattern, x, y):
    """Основная функция заливки с использованием паттерна"""
    target_color = surface.get_at((x, y))[:3]

    # Начинаем заливку с точки (x, y)
    fill_line_pattern(surface, pattern, x, y, target_color)

def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Рисование и заливка паттерном')
    clock = pygame.time.Clock()

    # Создаем поверхность для рисования
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_COLOR)

    # Загружаем паттерн
    pattern = load_pattern(r'C:\Users\mtz20\IdeaProjects\ComputerGraphic\lab 3\input_image.png')  # Путь к изображению паттерна

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
        clock.tick(1400000)

    # Сохраняем результат как изображение
    pygame.image.save(canvas, r'C:\Users\mtz20\IdeaProjects\ComputerGraphic\lab 3\output_image_with_pattern.png')

    pygame.quit()

if __name__ == "__main__":
    main()
