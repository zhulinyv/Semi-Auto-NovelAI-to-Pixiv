import os
from pathlib import Path

from loguru import logger
from PIL import Image

from utils.imgtools import revert_img_info
from utils.utils import file_path2list


def remove_info(input_path, output_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        logger.warning(f"正在清除 {file} 的元数据...")
        img = Image.open(Path(input_path) / file)
        img.save(Path(output_path) / file)
        logger.success("清除成功!")
    return f"清除成功! 图片已保存到 {output_path}"


def revert_info(input_path, output_path):
    file_list = file_path2list(output_path)
    for file in file_list:
        if os.path.exists(Path(input_path) / f"{file[:-4]}.txt"):
            revert_img_info(str(Path(input_path) / f"{file[:-4]}.txt"), Path(output_path) / file)
        elif os.path.exists(Path(input_path) / f"{file[:-4]}.png"):
            revert_img_info(str(Path(input_path) / f"{file[:-4]}.png"), Path(output_path) / file)
        else:
            logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
    return f"还原成功! 图片已保存到 {output_path}"
