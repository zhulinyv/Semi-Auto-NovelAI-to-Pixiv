import base64
from pathlib import Path, WindowsPath

import ujson as json
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.env import env

# extract_data 修改自 https://github.com/NovelAI/novelai-image-metadata
from utils.naimeta import extract_data
from utils.prepare import logger
from utils.utils import file_path2name, float_to_position

logger.info("正在检查图像检测模型...")

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


def img_to_base64(image):
    if isinstance(image, str):
        pass
    elif isinstance(image, WindowsPath):
        pass
    else:
        image.save("./output/temp.png")
        image = "./output/temp.png"
    with open(image, "rb") as file:
        img_base64 = base64.b64encode(file.read()).decode("utf-8")
    return img_base64


def revert_img_info(img_path, output_dir, *args):
    if env.revert_info:
        logger.info("正在还原 pnginfo")
    else:
        with Image.open(output_dir) as new_img:
            new_img.save(output_dir)
        logger.warning("还原图片信息操作已关闭, 如有需要请在配置项中设置 revert_info=True")
        return
    try:
        key_list = ["Software", "Comment", "parameters", "prompt"]
        value_list = []
        if img_path:
            if img_path[-4:] == ".png":
                with Image.open(img_path) as old_img:
                    info = old_img.info
                for key in key_list:
                    try:
                        value_list.append(info[key])
                    except KeyError:
                        pass
            elif img_path[-4:] == ".txt":
                with open(img_path) as f:
                    prompt = f.read()
                value_list = ["NovelAI", json.dumps({"prompt": prompt})]
            else:
                logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
                return
        else:
            for key in key_list:
                try:
                    value_list.append(args[0][key])
                except KeyError:
                    pass
        metadata = PngInfo()
        if len(value_list) == 1:
            if isinstance(value_list[0], str):
                metadata.add_text("parameters", value_list[0])
            elif isinstance(value_list[0], dict):
                metadata.add_text("prompt", json.dumps(value_list[0]))
        else:
            metadata.add_text("Software", value_list[0])
            metadata.add_text("Comment", value_list[1])
        with Image.open(output_dir) as new_img:
            new_img.save(output_dir, pnginfo=metadata)
        logger.success("还原成功!")
    except Exception:
        with Image.open(output_dir) as new_img:
            new_img.save(output_dir)
        logger.error("还原失败!")


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
    logger.error("change_the_mask_color_to_white 方法已弃用! 请更新插件!")


def change_the_mask_color(image_path):
    with Image.open(image_path) as image:
        image_array = image.load()
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                rgba = image_array[x, y]
                r, g, b, a = rgba
                if a != 0:
                    image_array[x, y] = (255, 255, 255)
                elif a == 0:
                    image_array[x, y] = (0, 0, 0)
        image.save(image_path)


def check_all_corners_black(image_path):
    with Image.open(image_path) as img:
        width, height = img.size

        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]

        return all(img.getpixel(pos) == (0, 0, 0) for pos in corners)


def return_pnginfo(image):
    if not image:
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    try:
        try:
            comment = json.loads((pnginfo := image.info)["Comment"])
        except Exception:
            comment = json.loads((pnginfo := extract_data(image))["Comment"])
        pnginfo["Comment"] = json.loads(pnginfo["Comment"])
    except Exception:
        try:
            return (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                json.dumps(pnginfo, indent=4, ensure_ascii=False),
            )
        except Exception:
            return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    try:
        skip_cfg_above_sigma = True if comment["skip_cfg_above_sigma"] else False
    except KeyError:
        skip_cfg_above_sigma = False

    return (
        comment["prompt"],
        comment["uc"],
        str(comment["width"]),
        str(comment["height"]),
        comment["steps"],
        comment["scale"],
        comment["cfg_rescale"],
        (
            "karras"
            if "nai-diffusion-4" in env.model and comment["noise_schedule"] == "native"
            else comment["noise_schedule"]
        ),
        comment["sampler"],
        comment["sm"],
        comment["sm_dyn"],
        skip_cfg_above_sigma,
        comment["dynamic_thresholding"],
        comment["seed"],
        json.dumps(pnginfo, indent=4, ensure_ascii=False),
    )


def get_img_info(img_path):
    with Image.open(img_path) as img:
        try:
            return json.loads((return_pnginfo(img))[-1])
        except Exception as e:
            logger.error(f"读取图片生成信息失败: {e}")
            return None


def _return_pnginfo(
    positive_input,
    negative_input,
    width,
    height,
    steps,
    scale,
    cfg_rescale,
    noise_schedule,
    sampler,
    sm,
    sm_dyn,
    variety,
    decrisp,
    seed,
    pnginfo,
    *image,
):
    try:
        pnginfo = json.loads(pnginfo)
        v4_prompt = pnginfo["Comment"]["v4_prompt"]
        v4_negative_prompt = pnginfo["Comment"]["v4_negative_prompt"]

        use_coords = v4_prompt["use_coords"]

        character_list = []
        character_num = len(v4_prompt["caption"]["char_captions"])
        for num in range(character_num):
            character_list.append(True)
            character_list.append(v4_prompt["caption"]["char_captions"][num]["char_caption"])
            character_list.append(v4_negative_prompt["caption"]["char_captions"][num]["char_caption"])
            character_list.append(
                float_to_position(
                    v4_prompt["caption"]["char_captions"][num]["centers"][0]["x"],
                    v4_prompt["caption"]["char_captions"][num]["centers"][0]["y"],
                )
            )
        for num in range(6 - character_num):
            character_list.append(False)
            character_list.append("")
            character_list.append("")
            character_list.append("A1")
    except KeyError:
        use_coords = True
        character_list = []
        for _ in range(6):
            character_list.append(False)
            character_list.append("")
            character_list.append("")
            character_list.append("A1")
    metadata = (
        positive_input,
        negative_input,
        width,
        height,
        steps,
        scale,
        cfg_rescale,
        noise_schedule,
        sampler,
        sm,
        sm_dyn,
        variety,
        decrisp,
        seed,
    )

    metadata = metadata if not image else metadata + (image[0],)

    metadata += (use_coords,)
    metadata += tuple(character_list)

    return metadata
