import os
import random
from pathlib import Path

from utils.env import env
from utils.imgtools import get_img_info, img_to_base64

if "nai-diffusion-4" not in env.model:
    from utils.jsondata import json_for_i2i
else:
    from utils.jsondata import json_for_i2i_v4 as json_for_i2i
from utils.prepare import logger
from utils.utils import file_path2list, generate_image, position_to_float, return_x64, save_image, sleep_for_cool


def i2i_by_hand(
    input_img,
    input_path,
    open_button,
    positive: str,
    negative: str,
    image2image_width: str,
    image2image_height: str,
    scale: float,
    image2image_rescale: float,
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
    *args,
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
        json_for_i2i["parameters"]["cfg_rescale"] = image2image_rescale
        json_for_i2i["parameters"]["sampler"] = sampler
        json_for_i2i["parameters"]["steps"] = steps
        json_for_i2i["parameters"]["strength"] = strength
        json_for_i2i["parameters"]["noise"] = noise
        if "nai-diffusion-4" not in env.model:
            json_for_i2i["parameters"]["sm"] = False
            json_for_i2i["parameters"]["sm_dyn"] = False
        json_for_i2i["parameters"]["skip_cfg_above_sigma"] = 19.343056794463642 if variety else None
        json_for_i2i["parameters"]["dynamic_thresholding"] = decrisp
        if sampler != "ddim_v3":
            json_for_i2i["parameters"]["noise_schedule"] = noise_schedule
        seed = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
        json_for_i2i["parameters"]["seed"] = seed
        json_for_i2i["parameters"]["image"] = img_to_base64(input_img)
        json_for_i2i["parameters"]["extra_noise_seed"] = seed
        json_for_i2i["parameters"]["negative_prompt"] = negative

        if "nai-diffusion-4" in env.model:
            json_for_i2i["parameters"]["use_coords"] = not args[0]
            json_for_i2i["parameters"]["v4_prompt"]["caption"]["base_caption"] = positive
            json_for_i2i["parameters"]["v4_prompt"]["use_coords"] = not args[0]
            json_for_i2i["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = negative

            args = args[1:]
            components_list = []
            while args:
                components_list.append(args[0:4])
                args = args[4:]

            json_for_i2i["parameters"]["characterPrompts"] = [
                {
                    "prompt": components[1],
                    "uc": components[2],
                    "center": {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]},
                    "enabled": True,
                }
                for components in components_list
                if components[0]
            ]

            json_for_i2i["parameters"]["v4_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[1],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]

            json_for_i2i["parameters"]["v4_negative_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[2],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]

        saved_path = save_image(generate_image(json_for_i2i), "i2i", seed, "None", "None")

        return saved_path, None


def prepare_json(imginfo: dict, imgpath):
    if imginfo["Software"] != "NovelAI":
        logger.error("不是 NovelAI 生成的图片!")
        return
    img_comment = imginfo["Comment"]
    json_for_i2i["input"] = img_comment["prompt"]
    seed = random.randint(1000000000, 9999999999)
    width = return_x64(int(img_comment["width"] * env.magnification))
    height = return_x64(int(img_comment["height"] * env.magnification))
    if width > height:
        if width > 1920:
            height = return_x64(int(1920 / width * height))
            width = 1920
            if height > 1600:
                width = return_x64(int(1600 / height * width))
    else:
        if height > 1920:
            width = return_x64(int(1920 / height * width))
            height = 1920
            if width > 1600:
                height = return_x64(int(1600 / width * height))
    json_for_i2i["parameters"]["width"] = width
    json_for_i2i["parameters"]["height"] = height
    json_for_i2i["parameters"]["scale"] = img_comment["scale"]
    json_for_i2i["parameters"]["sampler"] = img_comment["sampler"]
    json_for_i2i["parameters"]["steps"] = img_comment["steps"]
    json_for_i2i["parameters"]["strength"] = env.hires_strength
    json_for_i2i["parameters"]["noise"] = env.hires_noise
    if "nai-diffusion-4" not in env.model:
        json_for_i2i["parameters"]["sm"] = False
        json_for_i2i["parameters"]["sm_dyn"] = False
    try:
        variety = img_comment["skip_cfg_above_sigma"]
    except KeyError:
        logger.warning("旧版图片不支持 variety 参数, 将使用配置设置中的 variety 参数")
        variety = env.variety
    json_for_i2i["parameters"]["skip_cfg_above_sigma"] = 19.343056794463642 if variety else None
    json_for_i2i["parameters"]["dynamic_thresholding"] = img_comment["dynamic_thresholding"]
    try:
        json_for_i2i["parameters"]["noise_schedule"] = img_comment["noise_schedule"]
    except KeyError:
        pass
    json_for_i2i["parameters"]["seed"] = seed
    json_for_i2i["parameters"]["image"] = img_to_base64(imgpath)
    json_for_i2i["parameters"]["extra_noise_seed"] = seed
    json_for_i2i["parameters"]["negative_prompt"] = img_comment["uc"]

    if "nai-diffusion-4" in env.model:
        try:
            json_for_i2i["parameters"]["use_coords"] = img_comment["v4_prompt"]["use_coords"]
            json_for_i2i["parameters"]["v4_prompt"]["caption"]["base_caption"] = img_comment["v4_prompt"]["caption"][
                "base_caption"
            ]
            json_for_i2i["parameters"]["v4_prompt"]["use_coords"] = img_comment["v4_prompt"]["use_coords"]
            json_for_i2i["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = img_comment["uc"]

            num = 0
            for char_captions in img_comment["v4_prompt"]["caption"]["char_captions"]:
                json_for_i2i["parameters"]["characterPrompts"] = []
                json_for_i2i["parameters"]["characterPrompts"].append(
                    {
                        "prompt": char_captions["char_caption"],
                        "uc": img_comment["v4_negative_prompt"]["caption"]["char_captions"][num]["char_caption"],
                        "center": {"x": char_captions["centers"][0]["x"], "y": char_captions["centers"][0]["y"]},
                    }
                )
                num += 1
        except KeyError:
            logger.warning("正在使用 NAI3 生成的图片使用 NAI4 生图!")
            json_for_i2i["parameters"]["use_coords"] = False
            json_for_i2i["parameters"]["v4_prompt"]["caption"]["base_caption"] = ""
            json_for_i2i["parameters"]["v4_prompt"]["use_coords"] = False
            json_for_i2i["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = ""

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
