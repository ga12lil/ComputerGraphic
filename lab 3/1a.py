import pygame
from pygame.locals import *
from PIL import Image

# Настройки окна
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)  # Цвет фона (белый)
DRAW_COLOR = (0, 0, 0)  # Цвет рисования (черный)
FILL_COLOR = (255, 0, 0)  # Цвет заливки (красный)

def fill_line(surface, x, y, target_color, replacement_color):
    """Алгоритм заливки строки пикселей."""
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

    # Закрашиваем линию от left до right
    for i in range(left, right + 1):
        pixels[i, y] = replacement_color

    # Обрабатываем соседние строки
    if y > 0:
        for i in range(left, right + 1):
            if surface.get_at((i, y - 1))[:3] == target_color:
                fill_line(surface, i, y - 1, target_color, replacement_color)

    if y < height - 1:
        for i in range(left, right + 1):
            if surface.get_at((i, y + 1))[:3] == target_color:
                fill_line(surface, i, y + 1, target_color, replacement_color)

    del pixels

def flood_fill(surface, x, y, replacement_color):
    """Основная функция заливки."""
    target_color = surface.get_at((x, y))[:3]

    # Если целевой цвет совпадает с цветом замены, выходим
    if target_color == replacement_color:
        return

    # Начинаем заливку с точки (x, y)
    fill_line(surface, x, y, target_color, replacement_color)

def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Рисование и заливка области')
    clock = pygame.time.Clock()

    # Создаем поверхность для рисования
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_COLOR)

    drawing = False  # Флаг рисования
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши — начать рисование
                    drawing = True
                elif event.button == 3:  # Правая кнопка мыши — заливка
                    x, y = event.pos
                    flood_fill(canvas, x, y, FILL_COLOR)
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
    pygame.image.save(canvas, 'output_image.png')

    pygame.quit()

if __name__ == "__main__":
    main()
