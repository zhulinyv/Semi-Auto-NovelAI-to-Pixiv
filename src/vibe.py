import random
from pathlib import Path

from loguru import logger

from src.batchtxt import prepare_input as batchtxt_input
from src.t2i import prepare_input as t2i_input
from utils.env import env
from utils.imgtools import img_to_base64
from utils.jsondata import json_for_vibe
from utils.utils import file_path2list, generate_image, read_json, save_image, sleep_for_cool


def vibe_by_hand(
    positive: str,
    negative: str,
    resolution: str,
    scale: float,
    sampler: str,
    noise_schedule: str,
    steps: int,
    sm: bool,
    sm_dyn: bool,
    seed: str,
    input_imgs: str,
):
    json_for_vibe["input"] = positive

    json_for_vibe["parameters"]["width"] = int(resolution.split("x")[0])
    json_for_vibe["parameters"]["height"] = int(resolution.split("x")[1])
    json_for_vibe["parameters"]["scale"] = scale
    json_for_vibe["parameters"]["sampler"] = sampler
    json_for_vibe["parameters"]["steps"] = steps
    json_for_vibe["parameters"]["sm"] = sm
    json_for_vibe["parameters"]["sm_dyn"] = sm_dyn if sm else False
    json_for_vibe["parameters"]["noise_schedule"] = noise_schedule
    seed = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
    json_for_vibe["parameters"]["seed"] = seed
    json_for_vibe["parameters"]["negative_prompt"] = negative

    json_for_vibe["parameters"]["add_original_image"] = True

    reference_image_multiple = []
    reference_information_extracted_multiple = []
    reference_strength_multiple = []
    img_list = file_path2list(Path(input_imgs))
    for img in img_list:
        reference_image_multiple.append(img_to_base64(Path(input_imgs) / img))
        reference_list = img.replace(".png", "").split("_")
        reference_information_extracted_multiple.append(float(reference_list[1]))
        reference_strength_multiple.append(float(reference_list[2]))

    logger.debug(
        f"""
基底图片: {img_list}
信息提取: {reference_information_extracted_multiple}
参考强度: {reference_strength_multiple}"""
    )

    json_for_vibe["parameters"]["reference_image_multiple"] = reference_image_multiple
    json_for_vibe["parameters"]["reference_information_extracted_multiple"] = reference_information_extracted_multiple
    json_for_vibe["parameters"]["reference_strength_multiple"] = reference_strength_multiple

    saved_path = save_image(generate_image(json_for_vibe), "vibe", seed, "None", "None")

    return saved_path


def prepare_json(input_, sm, scale, negative, input_imgs):
    json_for_vibe["input"] = input_
    if isinstance(env.img_size, int):
        resolution_list = [[832, 1216], [1024, 1024], [1216, 832]]
        resolution = random.choice(resolution_list)
    elif isinstance(env.img_size, list):
        resolution = env.img_size
    json_for_vibe["parameters"]["width"] = resolution[0]
    json_for_vibe["parameters"]["height"] = resolution[1]
    json_for_vibe["parameters"]["scale"] = env.scale if scale == 0 else scale
    json_for_vibe["parameters"]["sampler"] = env.sampler
    json_for_vibe["parameters"]["steps"] = env.steps
    json_for_vibe["parameters"]["sm"] = env.sm if sm == 0 else True
    json_for_vibe["parameters"]["sm_dyn"] = env.sm_dyn if (env.sm or (sm == 1)) and env.sm_dyn else False
    json_for_vibe["parameters"]["noise_schedule"] = env.noise_schedule
    seed = random.randint(1000000000, 9999999999) if env.seed == -1 else env.seed
    json_for_vibe["parameters"]["seed"] = seed
    json_for_vibe["parameters"]["negative_prompt"] = negative

    json_for_vibe["parameters"]["add_original_image"] = True

    reference_image_multiple = []
    reference_information_extracted_multiple = []
    reference_strength_multiple = []
    img_list = file_path2list(Path(input_imgs))
    for img in img_list:
        reference_image_multiple.append(img_to_base64(Path(input_imgs) / img))
        reference_list = img.replace(".png", "").split("_")
        reference_information_extracted_multiple.append(float(reference_list[1]))
        reference_strength_multiple.append(float(reference_list[2]))

    logger.debug(
        f"""
基底图片: {img_list}
信息提取: {reference_information_extracted_multiple}
参考强度: {reference_strength_multiple}"""
    )

    json_for_vibe["parameters"]["reference_image_multiple"] = reference_image_multiple
    json_for_vibe["parameters"]["reference_information_extracted_multiple"] = reference_information_extracted_multiple
    json_for_vibe["parameters"]["reference_strength_multiple"] = reference_strength_multiple

    return json_for_vibe, seed


def vibe(blue_imgs: bool, input_imgs):
    if blue_imgs:
        prompt, sm, scale, negative, choose_game, choose_character = t2i_input("随机(Random)")
    else:
        file, prompt = batchtxt_input("", "最前面(Top)")
        sm = env.sm
        scale = env.scale
        data = read_json("./files/favorite.json")
        negative = random.choice(data["negative_prompt"]["belief"])
        choose_game = choose_character = "None"
    json_for_vibe, seed = prepare_json(prompt, sm, scale, negative, input_imgs)
    saved_path = save_image(generate_image(json_for_vibe), "vibe", seed, choose_game, choose_character)
    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    return saved_path, saved_path
