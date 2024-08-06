import base64
from pathlib import Path, WindowsPath

import ujson as json
from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.env import env

# extract_data 修改自 https://github.com/NovelAI/novelai-image-metadata
from utils.naimeta import extract_data
from utils.utils import file_path2name

try:
    from ultralytics import YOLO

    logger.debug("使用 YOLO 进行图像预测")

    def detector(image):
        model = YOLO("./files/models/censor.pt")
        box_list = []
        results = model(image, verbose=False)
        result = json.loads((results[0]).tojson())
        for part in result:
            if part["name"] in ["penis", "pussy"]:
                logger.debug("检测到: {}".format(part["name"]))
                x = round(part["box"]["x1"])
                y = round(part["box"]["y1"])
                w = round(part["box"]["x2"] - part["box"]["x1"])
                h = round(part["box"]["y2"] - part["box"]["y1"])
                box_list.append([x, y, w, h])
        return box_list

except ModuleNotFoundError:
    from nudenet import NudeDetector

    logger.debug("使用 nudenet 进行图像检测")

    def detector(image):
        nude_detector = NudeDetector()
        # 这个库不能使用中文文件名
        # 写重复了, batch_mosaic 里已经写过了
        box_list = []
        body = nude_detector.detect("./output/temp.png")
        for part in body:
            if part["class"] in ["FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED"]:
                logger.debug("检测到: {}".format(part["class"]))
                x = part["box"][0]
                y = part["box"][1]
                w = part["box"][2]
                h = part["box"][3]
                box_list.append([x, y, w, h])
        return box_list


def get_img_info(img_path):
    with Image.open(img_path) as img:
        return img.info


def img_to_base64(img_path):
    if isinstance(img_path, str):
        pass
    elif isinstance(img_path, WindowsPath):
        pass
    else:
        img_path.save("./output/temp.png")
        img_path = "./output/temp.png"
    with open(img_path, "rb") as file:
        img_base64 = base64.b64encode(file.read()).decode("utf-8")
    return img_base64


def revert_img_info(img_path, output_dir, *args):
    if env.revert_info:
        logger.info("正在还原 pnginfo")
        try:
            if img_path:
                if img_path[-4:] == ".png":
                    with Image.open(img_path) as old_img:
                        info = old_img.info
                    software = info["Software"]
                    comment = info["Comment"]
                elif img_path[-4:] == ".txt":
                    with open(img_path) as f:
                        prompt = f.read()
                    software = "NovelAI"
                    comment = json.dumps({"prompt": prompt})
                else:
                    logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
                    return
            else:
                software = args[0]["Software"]
                comment = args[0]["Comment"]
            metadata = PngInfo()
            metadata.add_text("Software", software)
            metadata.add_text("Comment", comment)
            with Image.open(output_dir) as new_img:
                new_img.save(output_dir, pnginfo=metadata)
            logger.success("还原成功!")
        except Exception:
            with Image.open(output_dir) as new_img:
                new_img.save(output_dir)
            logger.error("还原失败!")
    else:
        with Image.open(output_dir) as new_img:
            new_img.save(output_dir)
        logger.warning("还原图片信息操作已关闭, 如有需要请在配置项中设置 revert_info=True")


def get_concat_h(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new("RGB", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def crop_image(path, otp_path):
    with Image.open(path) as img:
        w, h = img.size
        w_, h_ = 0, 0
        while w_ < w:
            w_ += 640
        while h_ < h:
            h_ += 640
        crop_img = img.crop((0, 0, w_, h_))
        crop_img = crop_img.convert("RGB")
        w, h = crop_img.size
        w_, h_ = 0, 0
        num, num_ = 0, 0
        while h_ < h:
            while w_ < w:
                num += 1
                tile = crop_img.crop((w_, h_, w_ + 640, h_ + 640))
                tile.save(Path(otp_path) / f"{num}.png")
                w_ += 320
            if num_ == 0:
                num_ = num
            h_ += 320
            w_ = 0
    return num_, int(num / num_)


def cut_img_w(path, otp_path):
    name = file_path2name(path)
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size
        crop_img = img.crop((0, 0, w, h / 2))
        crop_img.save(Path(otp_path) / name.replace(".png", "_u.png"))
        crop_img = img.crop((0, h / 2, w, h))
        crop_img.save(Path(otp_path) / name.replace(".png", "_d.png"))


def cut_img_h(path, otp_path):
    name = file_path2name(path)
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size
        crop_img = img.crop((0, 0, w / 2, h))
        crop_img.save(Path(otp_path) / name.replace(".png", "_l.png"))
        crop_img = img.crop((w / 2, 0, w, h))
        crop_img.save(Path(otp_path) / name.replace(".png", "_r.png"))


def change_the_mask_color_to_white(image_path):
    with Image.open(image_path) as image:
        image_array = image.load()
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                rgba = image_array[x, y]
                r, g, b, a = rgba
                if a != 0:
                    image_array[x, y] = (255, 255, 255)
        image.save(image_path)


def return_pnginfo(image: Image.Image):
    try:
        try:
            comment = json.loads((pnginfo := image.info)["Comment"])
        except Exception:
            comment = json.loads((pnginfo := extract_data(image))["Comment"])
        pnginfo["Comment"] = json.loads(pnginfo["Comment"])
    except Exception:
        return None, None, None, None, None, None, None, None, None, None, None, None
    return (
        comment["prompt"],
        comment["uc"],
        str(comment["width"]),
        str(comment["height"]),
        comment["steps"],
        comment["scale"],
        comment["noise_schedule"],
        comment["sampler"],
        comment["sm"],
        comment["sm_dyn"],
        comment["seed"],
        json.dumps(pnginfo, indent=4, ensure_ascii=False),
    )


def _return_pnginfo(
    positive_input,
    negative_input,
    width,
    height,
    steps,
    scale,
    noise_schedule,
    sampler,
    sm,
    sm_dyn,
    seed,
    pnginfo,
    *image,
):
    metadata = (
        positive_input,
        negative_input,
        width,
        height,
        steps,
        scale,
        noise_schedule,
        sampler,
        sm,
        sm_dyn,
        seed,
        pnginfo,
    )
    return metadata if not image else metadata + (image[0],)
