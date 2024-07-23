import os
import shutil
from pathlib import Path

import numpy as np
import send2trash
from loguru import logger

from utils.utils import file_path2list


def show_first_img(input_path):
    try:
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
    except Exception:
        logger.error("未输入图片目录或输入的目录为空!")


def show_next_img():
    try:
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
    except Exception:
        logger.error("未输入图片目录或输入的目录为空!")


def move_current_img(current_img, output_path):
    try:
        img_name = os.path.basename(current_img)
        shutil.move(current_img, str(Path(output_path) / img_name))
        logger.info(f"已将 {current_img} 移动到 {output_path}")
        return show_next_img()
    except Exception:
        logger.error("未输入要移动的目录!")


def del_current_img(current_img):
    send2trash.send2trash(current_img)
    logger.info(f"\n已将 {current_img} 删除")
    return show_next_img()


def copy_current_img(current_img, output_path):
    try:
        img_name = os.path.basename(current_img)
        shutil.copyfile(current_img, str(Path(output_path) / img_name))
        logger.info(f"\n已将 {current_img} 复制到 {output_path}")
        return show_next_img()
    except Exception:
        logger.error("未输入要复制的目录!")
