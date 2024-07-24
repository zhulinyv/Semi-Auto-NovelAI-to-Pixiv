import os
import random
import shutil
from pathlib import Path

from loguru import logger
from PIL import Image

from src.batch_waifu2x import run_cmd_
from src.image2image import i2i_by_hand
from utils.downloader import download, extract
from utils.env import env
from utils.imgtools import crop_image, cut_img_h, cut_img_w, get_concat_h, get_concat_v
from utils.utils import file_namel2pathl, file_path2abs, file_path2dir, file_path2list, file_path2name


def merge_img(model, img1, img2, otp_path):
    if model == "rife-v2.3":
        pass
    else:
        if not os.path.exists(f"./files/rife-ncnn-vulkan/{model}"):
            download(
                f"https://huggingface.co/datasets/Xytpz/Upscale-Software-Collection/resolve/main/{model}.zip?download=true"
            )
            extract("./files/temp.zip", "./files/rife-ncnn-vulkan")
    code = r".\files\rife-ncnn-vulkan\rife-ncnn-vulkan.exe -0 {} -1 {} -o {} -m {}".format(img1, img2, otp_path, model)
    logger.debug(code)
    result = run_cmd_(code)
    logger.info(f"\n{result}")


def tile_upscale(image, img_path, positive, negative, strength, engine):
    if img_path:
        pass
    else:
        image.save(img_path := "./output/temp.png")

    dir = Path(file_path2dir(img_path))

    logger.info("正在拆分图片...")
    tiles_dir = dir / "tiles"
    if not os.path.exists(tiles_dir):
        os.mkdir(tiles_dir)
    w_num, h_num = crop_image(img_path, tiles_dir)

    logger.info("正在重绘图片...")
    i2i_dir = dir / "tile_i2i"
    if not os.path.exists(i2i_dir):
        os.mkdir(i2i_dir)
    seed = random.randint(1000000000, 9999999999)
    for tile in file_namel2pathl(file_path2list(tiles_dir), tiles_dir):
        while 1:
            try:
                saved_path, _ = i2i_by_hand(
                    tile,
                    None,
                    False,
                    positive,
                    negative,
                    "1024x1024",
                    env.scale,
                    env.sampler,
                    env.noise_schedule,
                    28,
                    strength,
                    0,
                    env.sm,
                    env.sm_dyn,
                    str(seed),
                )
                shutil.move(saved_path, i2i_dir / file_path2name(tile))
                break
            except Exception as e:
                logger.error(f"出现错误: {e}")
                logger.warning("重试...")

    logger.info("纵向切开图片...")
    cuth_dir = dir / "tiles_cuth"
    if not os.path.exists(cuth_dir):
        os.mkdir(cuth_dir)
    for img in file_namel2pathl(file_path2list(i2i_dir), i2i_dir):
        cut_img_h(img, cuth_dir)

    logger.info("合并纵向切开的图片...")
    mergev_dir = dir / "tiles_mergev"
    if not os.path.exists(mergev_dir):
        os.mkdir(mergev_dir)
    row_dir = dir / "tiels_row"
    if not os.path.exists(row_dir):
        os.mkdir(row_dir)
    for j in range(1, h_num + 1):
        merged_image = Image.open(cuth_dir / f"{(j-1)*w_num+1}_l.png")
        for i in range(1, w_num + 1):
            if i == w_num:
                pass
            else:
                merge_img(
                    engine,
                    file_path2abs(cuth_dir / f"{j*w_num-w_num+i}_r.png"),
                    file_path2abs(cuth_dir / f"{j*w_num-w_num+i+1}_l.png"),
                    file_path2abs(mergev_dir / f"{j*w_num-w_num+i}_{j*w_num-w_num+i+1}.png"),
                )
                try:
                    with Image.open(file_path2abs(mergev_dir / f"{j*w_num-w_num+i}_{j*w_num-w_num+i+1}.png")) as img:
                        merged_image = get_concat_h(merged_image, img)
                except FileNotFoundError:
                    pass
        with Image.open(cuth_dir / f"{j*w_num}_r.png") as img:
            merged_image = get_concat_h(merged_image, img)
        merged_image.save(row_dir / f"{j}.png")
        merged_image.close()

    logger.info("横向切开图片...")
    cutw_dir = dir / "tiles_cutw"
    if not os.path.exists(cutw_dir):
        os.mkdir(cutw_dir)
    for img in file_namel2pathl(file_path2list(row_dir), row_dir):
        cut_img_w(img, cutw_dir)

    logger.info("合并横向切开的图片...")
    mergeh_dir = dir / "tiles_mergeh"
    if not os.path.exists(mergeh_dir):
        os.mkdir(mergeh_dir)
    merged_image = Image.open(cutw_dir / "1_u.png")
    for i in range(1, h_num + 1):
        merge_img(
            engine,
            file_path2abs(cutw_dir / f"{i}_d.png"),
            file_path2abs(cutw_dir / f"{i+1}_u.png"),
            file_path2abs(mergeh_dir / f"{i}_{i+1}.png"),
        )
        try:
            with Image.open(file_path2abs(mergeh_dir / f"{i}_{i+1}.png")) as img:
                merged_image = get_concat_v(merged_image, img)
        except FileNotFoundError:
            pass
    with Image.open(cutw_dir / f"{h_num}_d.png") as img:
        merged_image = get_concat_v(merged_image, img)

    logger.info("裁剪黑边...")
    with Image.open(img_path) as img:
        w, h = img.size
    merged_image = merged_image.crop((0, 0, int(w * 1.6), int(h * 1.6)))

    logger.info("保存图片...")
    merged_image.save(dir / file_path2name(img_path).replace(".png", "_tile_upscale.png"))
    merged_image.close()

    logger.warning("删除临时目录...")
    for dir_ in [tiles_dir, cuth_dir, mergev_dir, row_dir, cutw_dir, mergeh_dir, i2i_dir]:
        shutil.rmtree(dir_)

    logger.success("放大完成!")

    return dir / file_path2name(img_path).replace(".png", "_tile_upscale.png")
