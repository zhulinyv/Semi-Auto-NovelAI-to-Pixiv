import os
import shutil

import cv2
from loguru import logger
from nudenet import NudeDetector
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.env import env
from utils.utils import format_path

nude_detector = NudeDetector()


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
    pil_img = Image.open(img_path)

    neighbor = int(pil_img.width * env.neighbor if pil_img.width > pil_img.height else pil_img.height * env.neighbor)

    body = nude_detector.detect(img_path)

    for part in body:
        if part["class"] in ["FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED"]:
            logger.debug("检测到: {}".format(part["class"]))

            cv2_img = cv2.imread(img_path)
            cv2_img = _mosaic(cv2_img, part["box"][0], part["box"][1], part["box"][2], part["box"][3], neighbor)
            cv2.imwrite(img_path, cv2_img)

    logger.info("正在还原 pnginfo")
    try:
        info = pil_img.info
        metadata = PngInfo()
        metadata.add_text("Software", info["Software"])
        metadata.add_text("Comment", info["Comment"])
        pil_img = Image.open(img_path)
        pil_img.save(img_path, pnginfo=metadata)
        logger.success("还原成功!")
    except Exception:
        logger.error("还原失败!")


def main(file_path, input_img, open_button):
    if open_button:
        file_list: list = os.listdir(file_path)
        file_list.remove("temp.png") if "temp.png" in file_list else ...
        for file in file_list:
            logger.info(f"正在处理{file}...")
            # 这个库不能使用中文文件名
            shutil.copyfile(f"{file_path}/{file}", f"{file_path}/temp.png")
            mosaic(f"{file_path}/temp.png")
            shutil.copyfile(f"{file_path}/temp.png", f"./output/mosaic/{file}")
            logger.success("处理完成!")
        return None, "处理完成!"

    else:
        input_img.save("./output/temp_.png")
        input_img = "./output/temp_.png"
        logger.info(f"正在处理{input_img}...")
        mosaic(input_img)
        logger.success("处理完成!")
        return "./output/temp_.png", None


if __name__ == "__main__":
    main(format_path("./output/choose_to_mosaic/"), None, True)
