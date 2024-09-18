import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image_path = 'C:/Users/ice/Downloads/111.jpg'  
image = Image.open(image_path)

image_array = np.array(image)

R, G, B = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]

red_image = np.zeros_like(image_array)
green_image = np.zeros_like(image_array)
blue_image = np.zeros_like(image_array)

red_image[:, :, 0] = R
green_image[:, :, 1] = G
blue_image[:, :, 2] = B

plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.imshow(red_image)
plt.title("Red Channel")

plt.subplot(2, 3, 2)
plt.imshow(green_image)
plt.title("Green Channel")

plt.subplot(2, 3, 3)
plt.imshow(blue_image)
plt.title("Blue Channel")

plt.subplot(2, 3, 4)
plt.hist(R.ravel(), bins=256, color='red', alpha=0.7)
plt.title("Red Histogram")

plt.subplot(2, 3, 5)
plt.hist(G.ravel(), bins=256, color='green', alpha=0.7)
plt.title("Green Histogram")

plt.subplot(2, 3, 6)
plt.hist(B.ravel(), bins=256, color='blue', alpha=0.7)
plt.title("Blue Histogram")

plt.tight_layout()
plt.show()











