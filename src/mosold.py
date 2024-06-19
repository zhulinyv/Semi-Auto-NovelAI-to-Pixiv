import shutil

from loguru import logger
from PIL import Image

from utils.imgtools import detector, revert_img_info
from utils.utils import file_namel2pathl, file_path2list, file_path2name


def __mosaic(img, length):
    s = img.size
    img = img.resize((int(length * 0.01), int(length * 0.01)))
    img = img.resize(s)
    return img


def _mosaic(img, fx, fy, tx, ty):
    length = img.width if img.width > img.height else img.height
    c = img.crop((fx, fy, tx, ty))
    c = __mosaic(c, length)
    img.paste(c, (fx, fy, tx, ty))
    return img


def mosaic(img):
    img = str(img)
    with Image.open(img) as image:
        box_list = detector(img)
        for box in box_list:
            image = _mosaic(
                image,
                box[0],
                box[1],
                box[0] + box[2],
                box[1] + box[3],
            )
            image.save(img)
        revert_img_info(None, img, image.info)


def main(file_path, input_img, open_button):
    if open_button:
        file_list = file_namel2pathl(file_path2list(file_path), file_path)
        for file in file_list:
            logger.info(f"正在处理 {file_path2name(file)}...")
            mosaic(file)
            shutil.move(file, f"./output/mosaic/{file_path2name(file)}")
            logger.success("处理完成!")
        return None, "处理完成! 图片已保存到 ./output/mosaic"
    else:
        input_img.save("./output/temp.png")
        input_img = "./output/temp.png"
        logger.info(f"正在处理 {input_img}...")
        mosaic(input_img)
        logger.success("处理完成!")
        return "./output/temp.png", None
