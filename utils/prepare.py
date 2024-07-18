import os
import shutil
import sys
from urllib.request import getproxies

from loguru import logger

try:
    proxies = getproxies()
    os.environ["http_proxy"] = proxies["http"]
    os.environ["https_proxy"] = proxies["https"]
    os.environ["no_proxy"] = proxies.get("no", "localhost, 127.0.0.1, ::1")
except KeyError:
    pass


VERSION = "2.19.5"

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


if not os.path.exists("./files/prompt/example.txt") and not os.path.exists("./files/prompt/done/example.txt"):
    with open("./files/prompt/example.txt", "w") as f:
        f.write(
            "[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,"
        )

if not os.path.exists("./files/favorite.json"):
    shutil.copyfile("./files/favorite_example.json", "./files/favorite.json")

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
███████╗ █████╗ ███╗   ██╗██████╗     <r>######################</r>
██╔════╝██╔══██╗████╗  ██║██╔══██╗    <r># 本项目完全开源免费 #</r>
███████╗███████║██╔██╗ ██║██████╔╝    <r>######################</r>
╚════██║██╔══██║██║╚██╗██║██╔═══╝     Version:    {VERSION}
███████║██║  ██║██║ ╚████║██║         Author:     https://github.com/zhulinyv
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝         Repository: https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv</c>"""
    )

    if env.skip_start_sound:
        pass
    else:
        from playsound import playsound

        playsound("./files/webui/llss.mp3")
