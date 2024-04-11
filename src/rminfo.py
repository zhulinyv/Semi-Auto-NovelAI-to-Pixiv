import os

from loguru import logger
from PIL import Image

from utils.imgtools import revert_img_info
from utils.utils import format_path


def remove_info(input_path, output_path):
    file_list = os.listdir(input_path)
    for file in file_list:
        logger.warning(f"正在清除 {file} 的元数据...")
        img = Image.open(f"{format_path(input_path)}/{file}")
        img.save(f"{format_path(output_path)}/{file}")
        logger.success("清除成功!")
    return f"清除成功! 图片已保存到 {output_path}"


def revert_info(input_path, output_path):
    file_list = os.listdir(output_path)
    for file in file_list:
        if os.path.exists(f"{format_path(input_path)}/{file[:-4]}.txt"):
            revert_img_info(f"{format_path(input_path)}/{file[:-4]}.txt", f"{format_path(output_path)}/{file}")
        elif os.path.exists(f"{format_path(input_path)}/{file[:-4]}.png"):
            revert_img_info(f"{format_path(input_path)}/{file[:-4]}.png", f"{format_path(output_path)}/{file}")
        else:
            logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
    return f"还原成功! 图片已保存到 {output_path}"
