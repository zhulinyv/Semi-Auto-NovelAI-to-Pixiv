import os
import shutil

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
    "./files/else_merge_engine",
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
