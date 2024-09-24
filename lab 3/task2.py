import matplotlib.pyplot as plt
import numpy as np

def bresenham(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x0 += sx
        if err2 < dx:
            err += dx
            y0 += sy

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
    dy = abs(y1 - y0)
    gradient = dy / dx if dx != 0 else 0

    y = y0
    for x in range(x0, x1 + 1):
        if steep:
            plot_pixel(y, x, 1 - (y - int(y)))
            plot_pixel(y + 1, x, (y - int(y)))
        else:
            plot_pixel(x, y, 1 - (y - int(y)))
            plot_pixel(x, y + 1, (y - int(y)))

        y += gradient

    return points


#WU
x0, y0 = 2, 3
x1, y1 = 8, 5
points_wu = wu_line(x0, y0, x1, y1)

fig, ax = plt.subplots()
for (x, y, c) in points_wu:
    ax.plot(x, y, 'o', color=(c, c, c))  # Используем цвет в градациях серого

plt.title("Wu's Line Algorithm")
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()
plt.show()

#Brezenham
x0, y0 = 2, 3
x1, y1 = 8, 5
points = bresenham(x0, y0, x1, y1)

plt.plot(*zip(*points), marker='o')
plt.title("Bresenham's Line Algorithm")
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()
plt.show()
