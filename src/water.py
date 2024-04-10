import os
import random

from loguru import logger
from PIL import Image, ImageFilter

from utils.env import env
from utils.imgtools import revert_img_info
from utils.utils import format_path


def water(img_path, otp_path):
    # 打开图片和水印
    water_list = os.listdir("./files/water")
    img = Image.open(img_path).convert("RGBA")
    water_img = random.choice(water_list)
    water = Image.open(f"./files/water/{water_img}").convert("RGBA")

    # 随机水印透明度
    new_png = water.copy()
    layer = Image.new("RGBA", water.size, color=(0, 0, 0, 0))
    new_png = Image.blend(new_png, layer, env.alpha)

    # 随机水印大小
    w, h = img.size
    w_, h_ = new_png.size
    new_height = env.water_height + random.randint(-20, 20)
    new_width = int(new_height / h_ * w_)
    new_png.resize((new_width, new_height))

    # 随机水印位置
    position = random.choice(env.position)
    if position == "左上":
        box = (100 + random.randint(-20, 20), 100 + random.randint(-20, 20))
    elif position == "右上":
        box = (w - new_width - 100 + random.randint(-20, 20), 100 + random.randint(-20, 20))
    elif position == "左下":
        box = (100 + random.randint(-20, 20), h - new_height - 100 + random.randint(-20, 20))
    elif position == "右下":
        box = (w - new_width - 100 + random.randint(-20, 20), h - new_height - 100 + random.randint(-20, 20))

    img = img.filter(ImageFilter.SMOOTH)
    img.paste(new_png, box, new_png)
    img = img.convert("RGBA")
    img.save(otp_path)
    revert_img_info(img_path, otp_path)


def main(input_path, output_path):
    file_list = os.listdir(input_path)
    for file in file_list:
        for i in range(env.water_num):
            logger.info(f"正在对 {file} 添加第 {i + 1} 个水印...")
            water("{}/{}".format(format_path(input_path), file), f"{output_path}/{file}")
            logger.success("处理完成!")
    return "处理完成! 图片已保存到 ./output/water..."


if __name__ == "__main__":
    main("./output/choose_to_water", "./output/water")
