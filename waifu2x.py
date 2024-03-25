import subprocess
import platform

from loguru import logger
from utils.error import Waifu2xError
from utils.env import env



def waifu2x():
    if platform.system() == "Windows":
        code = rf".\files\waifu2x-ncnn-vulkan\waifu2x-ncnn-vulkan.exe -i .\output\choose_for_upscale\ -o .\output\upscale\ -n {env.waifu2x_noise} -s {env.waifu2x_scale}"
        logger.debug(code)
    else:
        logger.error("仅支持 Window 运行!")
        return "寄"
    try:
        p = subprocess.Popen(code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        result = (stdout or stderr).decode('gb2312').strip()
    except Waifu2xError:
        return "寄"
    return result

logger.info("正在放大 .\\output\\choose_for_upscale\\...")
process_info = waifu2x()
logger.info("\n" + process_info)
if process_info != "寄":
    logger.success("放大成功!")
else:
    logger.error("放大失败!")