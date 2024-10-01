import pygame
from collections import deque

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Обход границы области")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

drawing = False
boundary_started = False
points = []
start_point = None

def find_boundary(start, color, surface):
    stack = deque([start])
    visited = set([start])
    boundary = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while stack:
        x, y = stack.pop()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))

                    if surface.get_at((nx, ny)) == color:
                        is_boundary = any(
                            surface.get_at((nx + dx, ny + dy)) != color
                            for dx, dy in directions
                            if 0 <= nx + dx < WIDTH and 0 <= ny + dy < HEIGHT
                        )
                        if is_boundary:
                            boundary.append((nx, ny))
                        else:
                            stack.append((nx, ny))

    return boundary

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            start_point = pygame.mouse.get_pos()
            color = screen.get_at(start_point)
            points = find_boundary(start_point, color, screen)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, BLUE, mouse_pos, 5)

    if points:
        for point in points:
            pygame.draw.circle(screen, RED, point, 2)

    pygame.display.flip()
pygame.quit()
