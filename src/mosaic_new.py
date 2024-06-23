import shutil

import cv2
from loguru import logger
from PIL import Image

from utils.env import env
from utils.imgtools import detector, revert_img_info
from utils.utils import file_namel2pathl, file_path2list, file_path2name


def _mosaic(img, x, y, w, h, neighbor):
    for i in range(0, h, neighbor):
        for j in range(0, w, neighbor):
            rect = [j + x, i + y]
            color = img[i + y][j + x].tolist()
            left_up = (rect[0], rect[1])
            x2 = rect[0] + neighbor - 1
            y2 = rect[1] + neighbor - 1
            if x2 > x + w:
                x2 = x + w
            if y2 > y + h:
                y2 = y + h
            right_down = (x2, y2)
            cv2.rectangle(img, left_up, right_down, color, -1)
    return img


def mosaic(img_path):
    img_path = str(img_path)
    with Image.open(img_path) as pil_img:
        neighbor = int(
            pil_img.width * env.neighbor if pil_img.width > pil_img.height else pil_img.height * env.neighbor
        )
    box_list = detector(img_path)
    for box in box_list:
        cv2_img = cv2.imread(img_path)
        if not cv2_img:
            pass
        else:
            cv2_img = _mosaic(cv2_img, box[0], box[1], box[2], box[3], neighbor)
            cv2.imwrite(img_path, cv2_img)
    revert_img_info(None, img_path, pil_img.info)


def main(file_path, input_img, open_button):
    if open_button:
        file_list = file_namel2pathl(file_path2list(file_path), file_path)
        for file in file_list:
            logger.info(f"正在处理 {file_path2name(file)}...")
            mosaic(file)
            shutil.move(file, f"./output/mosaic/{file_path2name(file)}")
            logger.success("处理完成!")
        return None, "处理完成! 图片已保存到 ./output/mosaic"
    else:
        input_img.save("./output/temp.png")
        input_img = "./output/temp.png"
        logger.info(f"正在处理 {input_img}...")
        mosaic(input_img)
        logger.success("处理完成!")
        return "./output/temp.png", None
