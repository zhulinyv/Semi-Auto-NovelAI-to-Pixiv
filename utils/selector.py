import os
import shutil
from pathlib import Path

import numpy as np
import send2trash

from utils.utils import file_path2list


def show_first_img(input_path):
    file_list: list = file_path2list(input_path)
    new_list = []
    for file in file_list:
        if file[-4:] in [".png", ".jpg"]:
            new_list.append(str(Path(input_path) / file))
    file_list = new_list[:]
    if file_list != []:
        img = file_list[0]
    else:
        img = None
    file_list.remove(img)
    array_data = np.array(file_list)
    np.save("./output/array_data.npy", array_data)

    return [img], img


def show_next_img():
    if os.path.exists("./output/array_data.npy"):
        file_list = np.load("./output/array_data.npy")
        file_list = list(file_list)
        new_list = []
        for file in file_list:
            new_list.append(str(file))
        file_list = new_list[:]
        try:
            img = file_list[0]
            if file_list != []:
                file_list.remove(file_list[0])
                array_data = np.array(file_list)
                np.save("./output/array_data.npy", array_data)
                return [img], img
        except Exception:
            os.remove("./output/array_data.npy")
    return None, None


def move_current_img(current_img, output_path):
    img_name = os.path.basename(current_img)
    shutil.move(current_img, str(Path(output_path) / img_name))
    return show_next_img()


def del_current_img(current_img):
    send2trash.send2trash(current_img)
    return show_next_img()


def copy_current_img(current_img, output_path):
    img_name = os.path.basename(current_img)
    shutil.copyfile(current_img, str(Path(output_path) / img_name))
    return show_next_img()
