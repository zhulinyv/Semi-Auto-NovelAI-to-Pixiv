import os
import shutil

from loguru import logger
from PIL import Image

from nudenet import NudeDetector
nude_detector = NudeDetector()



def mosaic(img, fx, fy, tx, ty):
    length = image.width if img.width > image.height else image.height
    c = img.crop((fx, fy, tx, ty))
    c = _mosaic(c, length)
    img.paste(c, (fx, fy, tx, ty))
    return img

def _mosaic(img, length):
    s = img.size
    img = img.resize((int(length * 0.01), int(length *0.01)))
    img = img.resize(s)
    return img

file_path = "./output/mosaic/"
file_list = os.listdir(file_path)
file_list.remove("temp.png") if "temp.png" in file_list else ...

for file in file_list:
    logger.info(f"正在处理{file}...")
    # 这个库不能使用中文文件名
    shutil.copy(file_path + file, file_path + "temp.png")
    body = nude_detector.detect(file_path + "temp.png")
    for part in body:
        image = Image.open(file_path + "temp.png")
        if part["class"] in ["FEMALE_GENITALIA_EXPOSED",  "MALE_GENITALIA_EXPOSED"]:
            image_new = mosaic(image, part["box"][0], part["box"][1], part["box"][0] + part["box"][2], part["box"][1] + part["box"][3])
            image.save(file_path + "temp.png")
    shutil.copyfile(file_path + "temp.png", file_path + file)
    logger.success("处理完成!")