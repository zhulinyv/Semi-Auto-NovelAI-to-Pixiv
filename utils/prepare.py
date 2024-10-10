import os
import shutil
import sys
from urllib.request import getproxies

from loguru import logger

VERSION = "3.0.0"


format_ = (
    f"<m>SANP:{VERSION} </m>"
    "| <c>{time:YY-MM-DD HH:mm:ss}</c> "
    "| <c>{module}:{line}</c> "
    "| <level>{level}</level> "
    "| <level>{message}</level>"
)

logger.remove()
logger.add(sys.stdout, format=format_, colorize=True)


try:
    proxies = getproxies()
    os.environ["http_proxy"] = proxies["http"]
    os.environ["https_proxy"] = proxies["https"]
    os.environ["no_proxy"] = proxies.get("no", "localhost, 127.0.0.1, ::1")
except KeyError:
    pass


need_dir_list = [
    "./output",
    "./output/t2i",
    "./output/t2i/grids",
    "./output/vibe",
    "./output/vibe/grids",
    "./output/i2i",
    "./output/enhance",
    "./output/inpaint",
    "./output/inpaint/img",
    "./output/inpaint/mask",
    "./output/pixiv",
    "./output/upscale",
    "./output/mosaic",
    "./output/water",
    "./output/bg-removal",
    "./output/lineart",
    "./output/sketch",
    "./output/declutter",
    "./output/colorize",
    "./output/emotion",
    "./files/else_upscale_engine",
    "./files/prompt",
    "./files/prompt/done",
    "./plugins",
    "./plugins/t2i",
    "./plugins/i2i",
    "./plugins/webui",
    "./plugins/inpaint",
]


if not os.path.exists(".env"):
    shutil.copyfile(".env.example", ".env")
for dir in need_dir_list:
    if not os.path.exists(dir):
        os.mkdir(dir)


if not os.path.exists("./files/favorites"):
    shutil.copytree("./files/favorites_example", "./files/favorites")


if not os.path.exists("./files/prompt/example.txt") and not os.path.exists("./files/prompt/done/example.txt"):
    with open("./files/prompt/example.txt", "w") as f:
        f.write(
            "[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,"
        )


if not os.path.exists("run_stand_alone_scripts.bat"):
    with open("run_stand_alone_scripts.bat", "w") as f:
        f.write(
            f"""@echo off
set PYTHON=\"{sys.executable}\"
%PYTHON% stand_alone_scripts.py
pause"""
        )


if __name__ == "__main__":
    from env import env

    logger.opt(colors=True).success(
        f"""<c>
███████╗ █████╗ ███╗   ██╗██████╗     <y>###################################################</y>
██╔════╝██╔══██╗████╗  ██║██╔══██╗    <y># This project is completely <r><i><u>OPEN SOURCE</u></i></r> and <r><i><u>FREE</u></i></r> #</y>
███████╗███████║██╔██╗ ██║██████╔╝    <y>###################################################</y>
╚════██║██╔══██║██║╚██╗██║██╔═══╝     Version:    {VERSION}
███████║██║  ██║██║ ╚████║██║         Author:     https://github.com/zhulinyv
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝         Repository: https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv</c>"""
    )

    if env.skip_start_sound:
        pass
    else:
        from playsound import playsound

        playsound("./files/webui/llss.mp3")
