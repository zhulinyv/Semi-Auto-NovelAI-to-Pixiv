import subprocess
import platform
import random
import string
import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from loguru import logger
from utils.error import Waifu2xError
from utils.env import env


def waifu2x(file, output_dir, waifu2x_noise, waifu2x_scale):
    logger.info(f"正在放大 {file}...")
    if platform.system() == "Windows":
        code = rf".\files\waifu2x-ncnn-vulkan\waifu2x-ncnn-vulkan.exe -i {file} -o {output_dir} -n {waifu2x_noise} -s {waifu2x_scale}"
        logger.debug(code)
    else:
        logger.error("仅支持 Window 运行!")
        return "寄"
    try:
        p = subprocess.Popen(code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        result = (stdout or stderr).decode('gb2312').strip()
    except Waifu2xError:
        logger.error("放大失败!")
        return "寄"
    logger.info("\n" + result)
    logger.success("放大成功!")
    logger.info(f"图片已保存到 {output_dir}")
    
    logger.info("正在还原 pnginfo")
    old_img = Image.open(file)
    info = old_img.info
    metadata = PngInfo()
    metadata.add_text("Software", info["Software"])
    metadata.add_text("Comment", info["Comment"])
    new_img = Image.open(output_dir)
    new_img.save(output_dir, pnginfo=metadata)
    logger.success("还原成功")


def main(file, file_path, open_button, waifu2x_noise, waifu2x_scale):
    if open_button:
        file_path = file_path
        file_list = os.listdir(file_path)
        empty_list = []
        for i in file_list:
            empty_list.append(f"{file_path}/{i}")
        file_list = empty_list
    else:
        file_path = "./output"
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file.save(f"./output/upscale_{waifu2x_noise}n_{waifu2x_scale}s_{random_string}.png")
        file = f"./output/upscale_{waifu2x_noise}n_{waifu2x_scale}s_{random_string}.png"
        file_list = [file]

    for j in file_list:
        otp = "./output/upscale/" + j.replace(file_path, '').replace("/", '')
        waifu2x(j, otp, waifu2x_noise, waifu2x_scale)

    if open_button:
        return "图片已保存到 ./output/upscale...", None
    else:
        return None, f"./output/upscale/temp_{random_string}.png"



if __name__ == "__main__":
    main(None, "./output/choose_for_upscale", True, env.waifu2x_noise, env.waifu2x_scale)