import matplotlib.pyplot as plt
import numpy as np

def bresenham(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx >= dy:
        d = 2 * dy - dx
        y = y0
        for x in range(x0, x1 + sx, sx):
            points.append((x, y))
            if d > 0:
                y += sy
                d -= 2 * dx
            d += 2 * dy
    else:
        d = 2 * dx - dy
        x = x0
        for y in range(y0, y1 + sy, sy):
            points.append((x, y))
            if d > 0:
                x += sx
                d -= 2 * dy
            d += 2 * dx

    return points


def wu_line(x0, y0, x1, y1):
    points = []

    def plot_pixel(x, y, c):
        points.append((x, y, c))

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0, x1, y1 = y0, x0, y1, x1

    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 0

    plot_pixel(x0, y0, 1)

    y = y0 + gradient
    for x in range(x0 + 1, x1):
        plot_pixel(x, int(y), 1 - (y - int(y)))
        plot_pixel(x, int(y) + 1, y - int(y))
        y += gradient

    plot_pixel(x1, y1, 1)

    return points


x0, y0 = 2, 3
x1, y1 = 15, 12
points_wu = wu_line(x0, y0, x1, y1)

fig, ax = plt.subplots()
for (x, y, c) in points_wu:
    ax.plot(x, y, 'o', color=(c, c, c), markersize=10) 

plt.title("Wu's Line Algorithm (Zoomed)")
plt.xlim(0, 20) 
plt.ylim(0, 20) 
plt.grid()
plt.show()

x0, y0 = 2, 3
x1, y1 = 8, 5
points = bresenham(x0, y0, x1, y1)

plt.plot(*zip(*points), marker='o')
plt.title("Bresenham's Line Algorithm")
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()
plt.show()
