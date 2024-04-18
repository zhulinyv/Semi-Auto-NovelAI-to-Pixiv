import os
from pathlib import Path

import ujson as json
from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.env import env
from utils.imgtools import get_img_info, revert_img_info
from utils.naimeta import inject_data
from utils.utils import file_path2list


def remove_info(input_path, output_path):
    metadata = PngInfo()
    metadata.add_text("None", env.meta_data)
    file_list = file_path2list(input_path)
    for file in file_list:
        logger.warning(f"正在清除 {file} 的元数据...")
        with Image.open(Path(input_path) / file) as img:
            img = inject_data(img, metadata)
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


def export_info(input_path, output_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        logger.info(f"正在导出: {file}...")
        info = get_img_info(f"{input_path}/{file}")
        prompt = json.loads(info["Comment"])["prompt"]
        file = file.replace(".png", ".txt")
        with open(f"{output_path}/{file}", "w", encoding="utf-8") as f:
            f.write(prompt)
        logger.success("导出成功!")
    return f"导出成功! 文件已保存到 {output_path}"
