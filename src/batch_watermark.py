import os
import random
from pathlib import Path

from PIL import Image

from utils.env import env
from utils.imgtools import revert_img_info
from utils.prepare import logger
from utils.utils import file_path2list


def water(img_path, otp_path, watermark_dir="./files/watermarks"):
    # 打开原始图片
    base_img = Image.open(img_path).convert("RGBA")
    base_width, base_height = base_img.size

    # 随机选择一个水印文件
    watermarks = [f for f in os.listdir(watermark_dir) if f.lower().endswith(("png", "jpg", "jpeg"))]
    if not watermarks:
        raise FileNotFoundError("水印文件夹中没有有效的图片。")
    watermark_path = os.path.join(watermark_dir, random.choice(watermarks))
    watermark = Image.open(watermark_path).convert("RGBA")

    # 随机旋转
    angle = random.uniform(0, 360)
    watermark = watermark.rotate(angle, expand=True)

    # 随机调整透明度
    alpha = random.uniform(0.2, 0.8)
    alpha_mask = watermark.split()[3].point(lambda p: int(p * alpha))
    watermark.putalpha(alpha_mask)

    # 调整大小（使水印宽高小于原图的一定比例）
    scale_factor = random.uniform(0.1, 0.5)  # 比例范围可调
    new_width = int(base_width * scale_factor)
    aspect_ratio = watermark.width / watermark.height
    new_height = int(new_width / aspect_ratio)
    watermark = watermark.resize((new_width, new_height), Image.LANCZOS)

    # 随机位置（确保水印不会超出边界）
    max_x = base_width - new_width
    max_y = base_height - new_height
    position = (random.randint(0, max_x), random.randint(0, max_y))

    # 合并图像
    combined = base_img.copy()
    combined.paste(watermark, position, watermark)

    # 保存结果
    combined.convert("RGB").save(otp_path)


def main(input_path, output_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        logger.info(f"正在对 {file} 添加第 1 个水印...")
        water(Path(input_path) / file, f"{output_path}/{file}")
        for i in range(env.water_num - 1):
            logger.info(f"正在对 {file} 添加第 {i + 2} 个水印...")
            water(f"{output_path}/{file}", f"{output_path}/{file}")
        logger.success("处理完成!")
        revert_img_info(str(Path(input_path) / file), f"{output_path}/{file}")
    return "处理完成! 图片已保存到 ./output/water..."
