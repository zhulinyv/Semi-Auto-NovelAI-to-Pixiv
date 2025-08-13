import os
import random
import time
from pathlib import Path

import cv2
import ujson as json
from PIL import Image
from playsound import playsound

from utils.env import env
from utils.imgtools import get_concat_h, get_concat_v, get_img_info, img_to_base64, revert_img_info

if "nai-diffusion-4" not in env.model:
    from utils.jsondata import json_for_i2i
else:
    from utils.jsondata import json_for_i2i_v4 as json_for_i2i
from utils.prepare import logger
from utils.utils import (
    file_path2list,
    generate_image,
    position_to_float,
    read_json,
    return_skip_cfg_above_sigma,
    return_x64,
    save_image,
    sleep_for_cool,
)


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
    times: int,
    *args,
):
    with open("./output/temp.json", "w") as f:
        json.dump({"break": False}, f)

    if open_button:
        main(input_path)
        return None, "处理完成!"
    else:
        if input_img is None:
            return None, "未输入图片!"

        imgs_list = []

        for i in range(times):
            data = read_json("./output/temp.json")
            if data["break"]:
                break

            if times != 1:
                logger.info(f"正在生成第 {i+1} 张图片...")
                sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

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
            json_for_i2i["parameters"]["skip_cfg_above_sigma"] = return_skip_cfg_above_sigma(variety)
            json_for_i2i["parameters"]["dynamic_thresholding"] = decrisp
            if sampler != "ddim_v3":
                json_for_i2i["parameters"]["noise_schedule"] = noise_schedule
            if isinstance(seed, int):
                seed = random.randint(1000000000, 9999999999)
            else:
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
                        "centers": [
                            {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}
                        ],
                    }
                    for components in components_list
                    if components[0]
                ]

                json_for_i2i["parameters"]["v4_negative_prompt"]["caption"]["char_captions"] = [
                    {
                        "char_caption": components[2],
                        "centers": [
                            {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}
                        ],
                    }
                    for components in components_list
                    if components[0]
                ]

            saved_path = save_image(generate_image(json_for_i2i), "i2i", seed, "None", "None")

            if saved_path != "寄":
                imgs_list.append(saved_path)
            else:
                pass
            _imgs_list = imgs_list[:]

        for img in imgs_list:
            if not os.path.exists(img):
                imgs_list.remove(img)

        if times != 1:
            if not env.skip_save_grid:
                num_list = []
                for row in range(3 if len(imgs_list) == 2 else len(imgs_list)):
                    for column in range(3 if len(imgs_list) == 2 else len(imgs_list)):
                        if row * column >= len(imgs_list):
                            num_list.append([row, column])
                row, column = num_list[0]
                for num in num_list[1:]:
                    if abs(num[0] - num[1]) < abs(row - column):
                        row, column = num

                imgs_list_list = [imgs_list[i : i + column] for i in range(0, len(imgs_list), column)]

                merged_imgs = []
                for imgs_list in imgs_list_list:
                    for img in imgs_list:
                        if img == imgs_list[0]:
                            merged_img = Image.open(img)
                        else:
                            merged_img = get_concat_h(merged_img, Image.open(img))
                    merged_imgs.append(merged_img)
                for img in merged_imgs:
                    if img == merged_imgs[0]:
                        merged_img = img
                    else:
                        merged_img = get_concat_v(merged_img, img)

                time_ = int(time.time())
                merged_img.save("./output/i2i/grids/{}.png".format(time_))
                merged_img.close()
            else:
                pass

            if not env.skip_finish_sound:
                playsound("./files/webui/download_finish.mp3")

            if env.skip_save_grid:
                return _imgs_list, None

            if times <= 10:
                revert_img_info(imgs_list[0], "./output/i2i/grids/{}.png".format(time_))
                return ["./output/i2i/grids/{}.png".format(time_)] + _imgs_list, None
            else:
                logger.warning("图片过大, 进行压缩...")
                cv2.imwrite(
                    "./output/i2i/grids/{}.jpg".format(time_),
                    cv2.imread("./output/i2i/grids/{}.png".format(time_)),
                    [cv2.IMWRITE_JPEG_QUALITY, 90],
                )
                with open("./output/i2i/grids/{}.txt".format(time_), "w") as infofile:
                    infofile.write(get_img_info(imgs_list[0])["Description"])
                logger.success("压缩完成!")
                return ["./output/i2i/grids/{}.jpg".format(time_)] + _imgs_list, None

        else:
            return [saved_path], None


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
    json_for_i2i["parameters"]["skip_cfg_above_sigma"] = (
        19.343056794463642
        if "nai-diffusion-4" in env.model and "nai-diffusion-4-5" not in env.model
        else 19 if "nai-diffusion-4-5" not in env.model else 58 if variety else None
    )
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
    data = read_json("./output/temp.json")
    if data["break"]:
        return

    i2i_path = Path(input_path)
    img_list = file_path2list(i2i_path)

    for img in img_list:
        data = read_json("./output/temp.json")
        if data["break"]:
            break

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
