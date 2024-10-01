import numpy as np
import matplotlib.pyplot as plt

def barycentric_coordinates(p, a, b, c):
    area = 0.5 * (-b[1]*c[0] + a[1]*(-b[0]+c[0]) + a[0]*(b[1]-c[1]) + b[0]*c[1])
    s = 1/(2*area) * (a[1]*c[0] - a[0]*c[1] + (c[1]-a[1])*p[0] + (a[0]-c[0])*p[1])
    t = 1/(2*area) * (a[0]*b[1] - a[1]*b[0] + (a[1]-b[1])*p[0] + (b[0]-a[0])*p[1])
    return s, t

def draw_triangle(a, b, c, color_a, color_b, color_c):
    min_x = int(min(a[0], b[0], c[0])) #границы треугольника
    max_x = int(max(a[0], b[0], c[0]))
    min_y = int(min(a[1], b[1], c[1]))
    max_y = int(max(a[1], b[1], c[1]))

    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3), dtype=np.uint8)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = (x, y)
            s, t = barycentric_coordinates(p, a, b, c)
            if s >= 0 and t >= 0 and (s + t) <= 1:
                color = (s * np.array(color_a) + t * np.array(color_b) + (1 - s - t) * np.array(color_c)).astype(np.uint8) # Интерполяция цвета
                img[y - min_y, x - min_x] = color

    plt.imshow(img)
    plt.axis('on')
    plt.show()

A = (50, 100)
B = (175, 300)
C = (300, 100)
color_A = (255, 0, 0)   
color_B = (0, 255, 0)   
color_C = (0, 0, 255)  

draw_triangle(A, B, C, color_A, color_B, color_C)
