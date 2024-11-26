import pygame
import random

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
LINE_COLOR = (173, 216, 230)
POINT_COLOR = (255, 255, 255)

# Параметры алгоритма
START_POINT = (50, SCREEN_HEIGHT // 2)
END_POINT = (SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)
INITIAL_ROUGHNESS =  150 # Амплитуда начального смещения
NUM_ITERATIONS = 8  # Максимальное количество итераций

def midpoint_displacement(start, end, roughness, iterations):
    """
    Генерация точек с помощью алгоритма Midpoint Displacement.
    Возвращает список точек для каждой итерации.
    """
    points = [start, end]
    all_iterations = [points.copy()]  # Сохраняем результаты каждой итерации
    
    for _ in range(iterations):
        new_points = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            
            # Средняя точка
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            
            # Смещение средней точки
            displacement = random.uniform(-roughness, roughness)
            new_mid = (mid_x, mid_y + displacement)
            
            # Добавляем точки: текущую и новую среднюю
            new_points.append(p1)
            new_points.append(new_mid)
        new_points.append(points[-1])  # Последняя точка
        
        points = new_points
        roughness *= 0.5  # Уменьшаем roughness для плавности
        all_iterations.append(points.copy())  # Сохраняем текущую итерацию
    
    return all_iterations

def draw_points(screen, points):
    #Отрисовка линии, соединяющей точки.
    
    # Рисуем линию
    for i in range(len(points) - 1):
        pygame.draw.line(screen, LINE_COLOR, points[i], points[i + 1], 2)
    # Рисуем точки
    for point in points:
        pygame.draw.circle(screen, POINT_COLOR, (int(point[0]), int(point[1])), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Midpoint Displacement Algorithm")
    clock = pygame.time.Clock()

    # Генерация точек для всех итераций
    all_iterations = midpoint_displacement(
        START_POINT,
        END_POINT,
        INITIAL_ROUGHNESS,
        NUM_ITERATIONS
    )
    current_iteration = 0

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Рисуем текущую итерацию
        draw_points(screen, all_iterations[current_iteration])

        # Обновление экрана
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Переключение итераций
                    current_iteration += 1
                    if current_iteration >= len(all_iterations):
                        current_iteration = 0  # Возврат к началу

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
