import os
import shutil
import pyautogui
import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk

screen_width, screen_height = pyautogui.size()

class ImageSelectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("图片筛选器")

        self.image_dir = ""
        self.output_dir = ""
        self.image_list = []
        self.current_index = 0

        self.master.geometry(f"{screen_width}x{screen_height}")

        self.image_dir_label = tk.Label(master, text="图片目录:")
        self.image_dir_label.place(x=screen_width/5+65, y=10)

        self.output_dir_label = tk.Label(master, text="移动目录:")
        self.output_dir_label.place(x=screen_width/5+65, y=60)

        self.load_image_button = tk.Button(master, text="选择图片目录", command=self.load_image_directory)
        self.load_image_button.place(x=10, y=10)

        self.load_output_button = tk.Button(master, text="选择移动目录", command=self.load_output_directory)
        self.load_output_button.place(x=10, y=60)

        self.select_button = tk.Button(master, text="移动", command=self.move_selected_image, state=tk.DISABLED)
        self.select_button.place(x=10, y=110, width=screen_width/5-20, height=(screen_height-200)/2)

        self.next_button = tk.Button(master, text="跳过", command=self.show_next_image, state=tk.DISABLED)
        self.next_button.place(x=10, y=110+(screen_height-200)/2, width=screen_width/5-20, height=(screen_height-200)/2)

        self.image_label = tk.Label(master)
        self.image_label.place(x=screen_width/5+65, y=110)

    def load_image_directory(self):
        self.image_dir = filedialog.askdirectory(title="选择图片目录")
        if self.image_dir:
            self.image_list = [os.path.join(self.image_dir, filename) for filename in os.listdir(self.image_dir) if filename.endswith(('.jpg', '.png', '.jpeg'))]
            self.show_next_image()
            self.image_dir_label.config(text="图片筛选器: " + self.image_dir)
            self.load_image_button.config(state=tk.DISABLED)
            self.select_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)

    def load_output_directory(self):
        self.output_dir = filedialog.askdirectory(title="选择移动目录")
        if self.output_dir:
            self.output_dir_label.config(text="移动目录: " + self.output_dir)
            self.load_output_button.config(state=tk.DISABLED)

    def show_next_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_index]
            image = Image.open(image_path)
            w, h = image.size
            aspect_ratio = w / h
            new_height = self.master.winfo_height() - 100
            new_width = int(new_height * aspect_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.current_index = (self.current_index + 1) % len(self.image_list)

    def move_selected_image(self):
        if self.output_dir and self.image_list:
            selected_image_path = self.image_list[(self.current_index - 1) % len(self.image_list)]
            image_filename = os.path.basename(selected_image_path)
            output_path = os.path.join(self.output_dir, image_filename)
            shutil.move(selected_image_path, output_path)
            self.show_next_image()

def main():
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
