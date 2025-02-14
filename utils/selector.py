import os
import shutil
from pathlib import Path

import numpy as np
import send2trash
from PIL import Image

from utils.prepare import logger
from utils.utils import PATH, file_path2list


def show_first_img(input_path):
    try:
        file_list: list = file_path2list(input_path)
        new_list = []
        for file in file_list:
            if file[-4:] in [".png", ".jpg"]:
                new_list.append(str(Path(input_path) / file))
        file_list = new_list[:]
        if file_list != []:
            img_path = file_list[0]
        else:
            img_path = None
        file_list.remove(img_path)
        array_data = np.array(file_list)
        np.save("./output/array_data.npy", array_data)
        with Image.open(img_path) as img:
            return [np.array(img)], img_path
    except Exception:
        logger.error("未输入图片目录或输入的目录为空!")
        return None, None


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
                img_path = file_list[0]
                if file_list != []:
                    file_list.remove(file_list[0])
                    array_data = np.array(file_list)
                    np.save("./output/array_data.npy", array_data)
                    with Image.open(img_path) as img:
                        return [np.array(img)], img_path
            except Exception:
                os.remove("./output/array_data.npy")
        return None, None
    except Exception:
        logger.error("未输入图片目录或输入的目录为空!")
        return None, None


def move_current_img(current_img, output_path):
    try:
        img_name = os.path.basename(current_img)
        shutil.move(current_img, str(Path(output_path) / img_name))
        logger.info(f"\n已将 {current_img} 移动到 {output_path}")
        return show_next_img()
    except Exception:
        logger.error("未输入要移动的目录!")
        return None, None


def del_current_img(current_img):
    try:
        if current_img:
            send2trash.send2trash(current_img)
            logger.info(f"已将 {current_img} 移动到回收站")
            return show_next_img()
        else:
            logger.error("当前未选择图片!")
            pass
    except Exception:
        logger.error("当前未选择图片!")
        return None, None
    os.chdir(PATH)


def copy_current_img(current_img, output_path):
    try:
        img_name = os.path.basename(current_img)
        shutil.copyfile(current_img, str(Path(output_path) / img_name))
        logger.info(f"已将 {current_img} 复制到 {output_path}")
        return show_next_img()
    except Exception:
        logger.error("未输入要复制的目录!")
        return None, None
