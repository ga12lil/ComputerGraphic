import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


def update_image(hue, saturation, value):
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 0] = (hsv_image[..., 0].astype(int) + hue) % 360
    hsv_image[..., 1] = np.clip(hsv_image[..., 1].astype(int) + saturation, 0, 255)
    hsv_image[..., 2] = np.clip(hsv_image[..., 2].astype(int) + value, 0, 255)
    
    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    rgb_image = Image.fromarray(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
    tk_image = ImageTk.PhotoImage(image=rgb_image)
    
    label.config(image=tk_image)
    label.image = tk_image


def save_image():
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 0] = (hsv_image[..., 0].astype(int) + hue_slider.get()) % 360
    hsv_image[..., 1] = np.clip(hsv_image[..., 1].astype(int) + saturation_slider.get(), 0, 255)
    hsv_image[..., 2] = np.clip(hsv_image[..., 2].astype(int) + value_slider.get(), 0, 255)
    
    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filename:
        cv2.imwrite(filename, rgb_image)


def load_image():
    global original_image
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg"), ("All files", "*.*")])
    
    if filename:
        original_image = cv2.imread(filename)
        if original_image is None:  
            print("Ошибка: не удалось загрузить изображение.")
            return
        
        rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(image=image_pil)

        label.config(image=tk_image)
        label.image = tk_image
    else:
        print("Файл не выбран.")

root = Tk()
root.title("Image HSV Editor")

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=10, pady=10)

right_frame = Frame(root)
right_frame.pack(side=LEFT, padx=10, pady=10)

original_image = None
load_button = Button(left_frame, text="Load Image", command=load_image)
load_button.pack()

hue_slider = Scale(left_frame, from_=-180, to=180, orient=HORIZONTAL, label="Hue", command=lambda v: update_image(int(v), saturation_slider.get(), value_slider.get()))
hue_slider.pack()

saturation_slider = Scale(left_frame, from_=-255, to=255, orient=HORIZONTAL, label="Saturation", command=lambda v: update_image(hue_slider.get(), int(v), value_slider.get()))
saturation_slider.pack()

value_slider = Scale(left_frame, from_=-255, to=255, orient=HORIZONTAL, label="Value", command=lambda v: update_image(hue_slider.get(), saturation_slider.get(), int(v)))
value_slider.pack()

label = Label(right_frame)
label.pack()

save_button = Button(left_frame, text="Save Image", command=save_image)
save_button.pack()

root.mainloop()
