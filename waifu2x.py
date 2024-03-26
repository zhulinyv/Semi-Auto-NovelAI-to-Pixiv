import subprocess
import platform
import random
import string

from loguru import logger
from utils.error import Waifu2xError
from utils.env import env



def waifu2x(file, file_path, open_button, waifu2x_noise, waifu2x_scale):
    if open_button:
        output_dir = "./output/upscale"
        file = file_path
    else:
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file.save(f"./output/temp_{random_string}.png")
        file = f"./output/temp_{random_string}.png"
        output_dir = f"./output/upscale/temp_{random_string}.png"
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
    logger.info("图片已保存到 ./output/upscale...")

    if open_button:
        return "图片已保存到 ./output/upscale...", None
    else:
        return None, f"./output/upscale/temp_{random_string}.png"



if __name__ == "__main__":
    waifu2x(None, "./output/choose_for_upscale/", True, env.waifu2x_noise, env.waifu2x_scale)