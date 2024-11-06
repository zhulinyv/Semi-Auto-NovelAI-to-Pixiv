import os
import random
from pathlib import Path

from utils.env import env
from utils.imgtools import get_img_info, img_to_base64
from utils.jsondata import json_for_i2i
from utils.prepare import logger
from utils.utils import file_path2list, generate_image, return_x64, save_image, sleep_for_cool


def i2i_by_hand(
    input_img,
    input_path,
    open_button,
    positive: str,
    negative: str,
    image2image_width: str,
    image2image_height: str,
    scale: float,
    sampler: str,
    noise_schedule: str,
    steps: int,
    strength: float,
    noise: float,
    sm: bool,
    sm_dyn: bool,
    variety: bool,
    decrisp: bool,
    seed: str,
):
    if open_button:
        main(input_path)
        return None, "处理完成!"
    else:
        logger.info("正在生成...")

        json_for_i2i["input"] = positive
        json_for_i2i["parameters"]["width"] = return_x64(int(image2image_width))
        json_for_i2i["parameters"]["height"] = return_x64(int(image2image_height))
        json_for_i2i["parameters"]["scale"] = scale
        json_for_i2i["parameters"]["sampler"] = sampler
        json_for_i2i["parameters"]["steps"] = steps
        json_for_i2i["parameters"]["strength"] = strength
        json_for_i2i["parameters"]["noise"] = noise
        json_for_i2i["parameters"]["sm"] = False
        json_for_i2i["parameters"]["sm_dyn"] = False
        json_for_i2i["parameters"]["skip_cfg_above_sigma"] = 19.343056794463642 if variety else None
        json_for_i2i["parameters"]["dynamic_thresholding"] = decrisp
        json_for_i2i["parameters"]["noise_schedule"] = noise_schedule
        seed = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
        json_for_i2i["parameters"]["seed"] = seed
        json_for_i2i["parameters"]["image"] = img_to_base64(input_img)
        json_for_i2i["parameters"]["extra_noise_seed"] = seed
        json_for_i2i["parameters"]["negative_prompt"] = negative

        saved_path = save_image(generate_image(json_for_i2i), "i2i", seed, "None", "None")
        sleep_for_cool(2, 4)

        return saved_path, None


def prepare_json(imginfo: dict, imgpath):
    if imginfo["Software"] != "NovelAI":
        logger.error("不是 NovelAI 生成的图片!")
        return
    img_comment = imginfo["Comment"]
    json_for_i2i["input"] = img_comment["prompt"]
    seed = random.randint(1000000000, 9999999999)
    json_for_i2i["parameters"]["width"] = return_x64(int(img_comment["width"] * env.magnification))
    json_for_i2i["parameters"]["height"] = return_x64(int(img_comment["height"] * env.magnification))
    json_for_i2i["parameters"]["scale"] = img_comment["scale"]
    json_for_i2i["parameters"]["sampler"] = img_comment["sampler"]
    json_for_i2i["parameters"]["steps"] = img_comment["steps"]
    json_for_i2i["parameters"]["strength"] = env.hires_strength
    json_for_i2i["parameters"]["noise"] = env.hires_noise
    json_for_i2i["parameters"]["sm"] = False
    json_for_i2i["parameters"]["sm_dyn"] = False
    try:
        variety = img_comment["skip_cfg_above_sigma"]
    except KeyError:
        variety = env.variety
    json_for_i2i["parameters"]["skip_cfg_above_sigma"] = 19.343056794463642 if variety else None
    json_for_i2i["parameters"]["dynamic_thresholding"] = env.decrisp
    json_for_i2i["parameters"]["noise_schedule"] = img_comment["noise_schedule"]
    json_for_i2i["parameters"]["seed"] = seed
    json_for_i2i["parameters"]["image"] = img_to_base64(imgpath)
    json_for_i2i["parameters"]["extra_noise_seed"] = seed
    json_for_i2i["parameters"]["negative_prompt"] = img_comment["uc"]

    return json_for_i2i


def main(input_path):
    i2i_path = Path(input_path)
    img_list = file_path2list(i2i_path)

    for img in img_list:
        times = 1
        while times <= 5:
            try:
                logger.info(f"正在图生图: {img}...")
                img_path = i2i_path / img
                saved_path = save_image(
                    generate_image(prepare_json(get_img_info(img_path), img_path)),
                    "i2i",
                    None,
                    None,
                    None,
                    img.replace(".jpg", ""),
                )
                if saved_path != "寄":
                    logger.warning("删除小图...")
                    os.remove(img_path)
                else:
                    raise Exception
                sleep_for_cool(env.i2i_cool_time - 3, env.i2i_cool_time + 3)
                break
            except Exception as e:
                sleep_for_cool(4, 8)
                times += 1
                logger.error(f"出现错误: {e}")
                logger.warning(f"重试 {times-1}/5...")
