import os
import shutil

from loguru import logger
from PIL import Image, ImageDraw

from utils.env import env
from utils.imgtools import detector, revert_img_info
from utils.utils import file_namel2pathl, file_path2list, file_path2name

# -------------------- #


def __mosaic_blurry(img, length):
    s = img.size
    img = img.resize((int(length * 0.01), int(length * 0.01)))
    img = img.resize(s)
    return img


def _mosaic_blurry(img, fx, fy, tx, ty):
    length = img.width if img.width > img.height else img.height
    c = img.crop((fx, fy, tx, ty))
    c = __mosaic_blurry(c, length)
    img.paste(c, (fx, fy, tx, ty))
    return img


def mosaic_blurry(img):
    img = str(img)
    with Image.open(img) as image:
        box_list = detector(img)
        for box in box_list:
            image = _mosaic_blurry(
                image,
                box[0],
                box[1],
                box[0] + box[2],
                box[1] + box[3],
            )
            image.save(img)
        revert_img_info(None, img, image.info)


# -------------------- #


def _mosaic_pixel(image, region, block_size):
    left, upper, right, lower = region

    cropped_image = image.crop(region)

    small = cropped_image.resize(
        (int((right - left) / block_size), int((lower - upper) / block_size)), resample=Image.Resampling.NEAREST
    )
    mosaic_image = small.resize(cropped_image.size, Image.Resampling.NEAREST)

    image.paste(mosaic_image, region)
    return image


def mosaic_pixel(img_path):
    img_path = str(img_path)
    box_list = detector(img_path)

    for box in box_list:
        with Image.open(img_path) as pil_img:
            neighbor = int(
                pil_img.width * env.neighbor if pil_img.width > pil_img.height else pil_img.height * env.neighbor
            )
            image = _mosaic_pixel(pil_img, (box[0], box[1], box[0] + box[2], box[1] + box[3]), neighbor)
            image.save(img_path)
            revert_img_info(None, img_path, pil_img.info)


# -------------------- #


def mosaic_lines(img_path):
    img_path = str(img_path)
    box_list = detector(img_path)
    with Image.open(img_path) as image:
        draw = ImageDraw.Draw(image)
        for box in box_list:
            x, y, w, h = box

            while y <= box[1] + box[3]:
                xy = [(x, y), (x + w, y)]
                draw.line(
                    xy,
                    fill="black",
                    width=10,
                )
                y += int(box[3] * 0.1145141919810)
        image.save(img_path)
        revert_img_info(None, img_path, image.info)


# -------------------- #


def main(file_path, input_img, open_button, mode):
    if open_button:
        file_list = file_namel2pathl(file_path2list(file_path), file_path)
    else:
        input_img.save("./output/_temp.png")
        file_list = ["./output/_temp.png"]
    for file in file_list:
        logger.info(f"正在处理 {file_path2name(file)}...")
        if os.path.exists("./output/temp.png"):
            os.remove("./output/temp.png")
        shutil.copyfile(file, "./output/temp.png")
        if mode == "pixel":
            mosaic_pixel("./output/temp.png")
        elif mode == "blurry":
            mosaic_blurry("./output/temp.png")
        elif mode == "lines":
            mosaic_lines("./output/temp.png")
        logger.success("处理完成!")
    if open_button:
        shutil.move("./output/temp.png", f"./output/mosaic/{file_path2name(file)}")
        return None, "处理完成! 图片已保存到 ./output/mosaic"
    else:
        os.remove("./output/_temp.png")
        return "./output/temp.png", None
