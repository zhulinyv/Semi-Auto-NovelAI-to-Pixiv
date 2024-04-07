import os
import shutil
import numpy as np

from utils.utils import format_path


def show_first_img(input_path):
    file_list: list = os.listdir(input_path)
    for file in file_list:
        if file[-4:] not in [".png", ".jpg"]:
            file_list.remove(file)
    new_list = []
    for file in file_list:
        new_list.append("{}/{}".format(format_path(input_path), file))
    file_list = new_list
    array_data = np.array(file_list)
    np.save("./output/array_data.npy", array_data)
    
    file_list = np.load("./output/array_data.npy")
    return str(file_list[0]), str(file_list[0])


def show_next_img():
    if os.path.exists("./output/array_data.npy"):
        file_list = np.load("./output/array_data.npy")
        file_list = list(file_list)
        new_list = []
        for file in file_list:
            new_list.append(str(file))
        file_list = new_list
        img = file_list[0]
        file_list.remove(file_list[0])
        if file_list != []:
            array_data = np.array(new_list)
            np.save("./output/array_data.npy", array_data)
            return img, img
        else:
            os.remove("./output/array_data.npy")
    return None, None


def move_current_img(current_img, output_path):
    img_name = os.path.basename(current_img)
    shutil.move(current_img, "{}/{}".format(format_path(output_path), img_name))
    return show_next_img()


def del_current_img(current_img):
    os.remove(current_img)
    return show_next_img()
