import os
import shutil

from loguru import logger

need_dir_list = [
    "./output",
    "./output/t2i",
    "./output/choose_to_i2i",
    "./output/i2i/",
    "./output/pixiv",
    "./output/choose_to_upscale",
    "./output/upscale",
    "./output/mosaic",
    "./output/choose_to_mosaic",
    "./output/inpaint",
    "./output/inpaint/img",
    "./output/inpaint/mask",
    "./files/else_upscale_engine",
    "./files/prompt",
    "./files/prompt/done",
    "./output/choose_to_water",
    "./output/water",
    "./output/info_file",
    "./output/info_removed",
    "./output/info_reverted",
    "./output/vibe",
    "./output/t2i/grids",
    "./output/choose_to_enhance",
    "./output/enhance",
    "./plugins",
    "./plugins/t2i",
    "./plugins/i2i",
    "./plugins/webui",
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


for choose_folder in [
    "./output/choose_to_i2i",
    "./output/choose_to_upscale",
    "./output/choose_to_mosaic",
    "./output/choose_to_water",
    "./output/choose_to_enhance",
]:
    if len(os.listdir(choose_folder)) != 0:
        logger.warning(
            f"""
>>>>>>>>>>
{choose_folder} 文件夹将在下个大版本更新后弃用!
----------
The {choose_folder} folder will be deprecated with the next major version update!
<<<<<<<<<<"""
        )
    else:
        os.rmdir(choose_folder)
