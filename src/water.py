import random
from pathlib import Path

from loguru import logger
from PIL import Image, ImageFilter

from utils.env import env
from utils.imgtools import revert_img_info
from utils.utils import file_path2list


def water(img_path, otp_path):
    # 打开图片和水印
    water_list = file_path2list("./files/water")
    water_img = random.choice(water_list)
    with Image.open(img_path) as img, Image.open(f"./files/water/{water_img}") as water:
        img = img.convert("RGBA")
        water = water.convert("RGBA")

        # 随机水印旋转度数
        water = water.rotate(random.randint(-env.rotate, env.rotate), expand=True)

        # 随机水印透明度
        new_png = water.copy()
        layer = Image.new("RGBA", water.size, color=(0, 0, 0, 0))
        new_png = Image.blend(new_png, layer, env.alpha + random.uniform(-0.15, 0.15))

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
        revert_img_info(str(img_path), otp_path)


def main(input_path, output_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        for i in range(env.water_num):
            logger.info(f"正在对 {file} 添加第 {i + 1} 个水印...")
            water(Path(input_path) / file, f"{output_path}/{file}")
            logger.success("处理完成!")
    return "处理完成! 图片已保存到 ./output/water..."
