import os
import shutil

from loguru import logger
from PIL import Image

from utils.utils import format_path

from nudenet import NudeDetector
nude_detector = NudeDetector()



def __mosaic(img, length):
    s = img.size
    img = img.resize((int(length * 0.01), int(length * 0.01)))
    img = img.resize(s)
    return img

def _mosaic(img, fx, fy, tx, ty):
    length = img.width if img.width > img.height else img.height
    c = img.crop((fx, fy, tx, ty))
    c = __mosaic(c, length)
    img.paste(c, (fx, fy, tx, ty))
    return img

def mosaic(img):
    body = nude_detector.detect(img)
    for part in body:
        image = Image.open(img)
        if part["class"] in ["FEMALE_GENITALIA_EXPOSED",  "MALE_GENITALIA_EXPOSED"]:
            _mosaic(image, part["box"][0], part["box"][1], part["box"][0] + part["box"][2], part["box"][1] + part["box"][3])
            image.save(img)



def main(file_path, input_img, open_button):
    if open_button:
        file_list: list = os.listdir(file_path)
        file_list.remove("temp.png") if "temp.png" in file_list else ...
        for file in file_list:
            logger.info(f"正在处理{file}...")
            # 这个库不能使用中文文件名
            shutil.copyfile(f"{file_path}/{file}", f"{file_path}/temp.png")
            mosaic(f"{file_path}/temp.png")
            shutil.copyfile(f"{file_path}/temp.png", f"{file_path}/{file}")
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
    main(format_path("./output/mosaic/"), None, True)