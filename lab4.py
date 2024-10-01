import pygame
import numpy as np
from pygame.locals import *
import math

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Полигональный редактор")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Хранение полигонов
polygons = []
current_polygon = []

# Матрицы для аффинных преобразований
def translation_matrix(dx, dy):
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]])

def rotation_matrix(angle, cx=0, cy=0):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return np.array([[cos_a, -sin_a, cx*(1-cos_a) + cy*sin_a],
                     [sin_a, cos_a, cy*(1-cos_a) - cx*sin_a],
                     [0, 0, 1]])

def scaling_matrix(sx, sy, cx=0, cy=0):
    return np.array([[sx, 0, cx*(1-sx)],
                     [0, sy, cy*(1-sy)],
                     [0, 0, 1]])

def apply_matrix(points, matrix):
    result = []
    for point in points:
        vector = np.array([point[0], point[1], 1])
        transformed = np.dot(matrix, vector)
        result.append((transformed[0], transformed[1]))
    return result

# Проверка на пересечение ребер
def edges_intersect(p1, p2, p3, p4):
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

# Определение положения точки относительно ребра
def classify_point_relative_to_edge(point, edge_start, edge_end):
    cross_product = (edge_end[0] - edge_start[0]) * (point[1] - edge_start[1]) - (edge_end[1] - edge_start[1]) * (point[0] - edge_start[0])
    if cross_product > 0:
        return "Слева от ребра"
    elif cross_product < 0:
        return "Справа от ребра"
    else:
        return "На ребре"

# Проверка принадлежности точки выпуклому/невыпуклому полигону (алгоритм с обходом вершин)
def is_point_in_polygon(point, polygon):
    inside = False
    n = len(polygon)
    x, y = point
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[(i + 1) % n]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
    return inside

# Основной цикл
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши — добавление точки
                pos = pygame.mouse.get_pos()
                current_polygon.append(pos)
            elif event.button == 3:  # Правая кнопка мыши — завершение полигона
                if current_polygon:
                    polygons.append(current_polygon)
                    current_polygon = []

        if event.type == KEYDOWN:
            if event.key == K_c:  # Очистка сцены
                polygons = []
                current_polygon = []
            elif event.key == K_t:  # Применение смещения (пример dx = 100, dy = 50)
                if polygons:
                    translation = translation_matrix(100, 50)
                    polygons[-1] = apply_matrix(polygons[-1], translation)
            elif event.key == K_r:  # Поворот вокруг центра полигона (пример на 45 градусов)
                if polygons:
                    centroid = np.mean(polygons[-1], axis=0)
                    rotation = rotation_matrix(45, centroid[0], centroid[1])
                    polygons[-1] = apply_matrix(polygons[-1], rotation)
            elif event.key == K_s:  # Масштабирование относительно центра полигона (пример sx = 1.5, sy = 1.5)
                if polygons:
                    centroid = np.mean(polygons[-1], axis=0)
                    scaling = scaling_matrix(1.5, 1.5, centroid[0], centroid[1])
                    polygons[-1] = apply_matrix(polygons[-1], scaling)
    
    # Рисуем полигоны
    for polygon in polygons:
        if len(polygon) > 1:
            pygame.draw.polygon(screen, BLACK, polygon, 1)
        else:
            pygame.draw.circle(screen, BLACK, polygon[0], 3)
    
    # Рисуем текущий полигон
    if len(current_polygon) > 1:
        pygame.draw.lines(screen, RED, False, current_polygon, 1)
    elif len(current_polygon) == 1:
        pygame.draw.circle(screen, RED, current_polygon[0], 3)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
