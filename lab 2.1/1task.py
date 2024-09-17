import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('image.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray1 = 0.299 * image[:, :, 2] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 0]
gray2 = 0.2126 * image[:, :, 2] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 0]

gray1 = np.clip(gray1, 0, 255).astype(np.uint8)
gray2 = np.clip(gray2, 0, 255).astype(np.uint8)

difference = cv2.absdiff(gray1, gray2)

plt.figure(figsize=(12, 8))

plt.subplot(3, 3, 1)
plt.imshow(image_rgb)
plt.title("Оригинальное изображение")
plt.axis('off')

plt.subplot(3, 3, 2)
plt.imshow(gray1, cmap='gray')
plt.title('Оттенки серого (формула 1)')
plt.axis('off')

plt.subplot(3, 3, 3)
plt.imshow(gray2, cmap='gray')
plt.title('Оттенки серого (формула 2)')
plt.axis('off')

plt.subplot(3, 3, 4)
plt.imshow(difference, cmap='gray')
plt.title('Разность изображений')
plt.axis('off')

plt.figure(figsize=(10,4))

plt.subplot(1, 2, 1)
plt.hist(gray1.ravel(), bins=256, color='blue', alpha=0.7, label='Формула 1')
plt.hist(gray2.ravel(), bins=256, color='red', alpha=0.7, label='Формула 2')
plt.title('Гистограмма (Формула 1 и Формула 2)')
plt.legend()

plt.tight_layout()
plt.show()

