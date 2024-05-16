import os
import random
import time

from loguru import logger
from PIL import Image

from utils.env import env
from utils.imgtools import get_concat_h, get_concat_v, revert_img_info
from utils.jsondata import json_for_t2i
from utils.utils import format_str, generate_image, list_to_str, read_json, save_image, sleep_for_cool


def t2i_by_hand(
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
    times: int,
):
    imgs_list = []
    for i in range(times):
        if times != 1:
            logger.info(f"正在生成第 {i+1} 张图片...")
        json_for_t2i["input"] = positive

        json_for_t2i["parameters"]["width"] = int(resolution.split("x")[0])
        json_for_t2i["parameters"]["height"] = int(resolution.split("x")[1])
        json_for_t2i["parameters"]["scale"] = scale
        json_for_t2i["parameters"]["sampler"] = sampler
        json_for_t2i["parameters"]["steps"] = steps
        json_for_t2i["parameters"]["sm"] = sm
        json_for_t2i["parameters"]["sm_dyn"] = sm_dyn if sm else False
        json_for_t2i["parameters"]["noise_schedule"] = noise_schedule
        if isinstance(seed, int):
            seed = random.randint(1000000000, 9999999999)
        else:
            seed = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
        json_for_t2i["parameters"]["seed"] = seed
        json_for_t2i["parameters"]["negative_prompt"] = negative

        logger.debug(json_for_t2i)

        saved_path = save_image(generate_image(json_for_t2i), "t2i", seed, "None", "None")

        imgs_list.append(saved_path)

    for img in imgs_list:
        if not os.path.exists(img):
            imgs_list.remove(img)

    if times != 1:
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
        merged_img.save("./output/t2i/grids/{}.png".format(time_))
        merged_img.close()

        revert_img_info(imgs_list[0], "./output/t2i/grids/{}.png".format(time_))

        return "./output/t2i/grids/{}.png".format(time_)
    else:
        return saved_path


def prepare_input():
    data = read_json("./files/favorite.json")

    weight_list = list(data["artists"]["belief"].keys())
    artist = ""
    while artist == "":
        possibility = random.random()
        for weight in weight_list:
            if possibility >= float(weight):
                artist_list = list(data["artists"]["belief"][weight].keys())
                if artist_list != []:
                    style_name = random.choice(artist_list)
                    style = data["artists"]["belief"][weight][style_name]
                    artist = style[0]
                    sm = style[1]
                    scale = style[2]
                    break
    pref = random.choice(data["quality_pref"]["belief"])
    negative = format_str(random.choice(data["negative_prompt"]["belief"]))
    choose_game = random.choice(list(data["character"].keys()))
    choose_character = random.choice(list(data["character"][choose_game].keys()))
    character = list_to_str(data["character"][choose_game][choose_character])
    action_type = (
        "巨乳"
        if any(char in character for char in ["huge breasts", "large breasts", "medium breasts"])
        else random.choice(["普通", "自慰"])
    )
    choose_action: list = random.choice(list(data["R18"]["动作"][f"{action_type}动作"].keys()))
    action = list_to_str(data["R18"]["动作"][f"{action_type}动作"][choose_action])
    emotion_type = "口交" if "oral" in action else "普通"
    choose_emotion = random.choice(list(data["R18"]["表情"][f"{emotion_type}表情"].keys()))
    emotion = (
        list_to_str(data["R18"]["表情"][f"{emotion_type}表情"][choose_emotion])
        if any(view not in action for view in ["from behind", "sex from behind"])
        else ""
    )
    choose_surrounding = random.choice(list(data["R18"]["场景"]["仅场景"].keys()))
    surrounding = (
        list_to_str(data["R18"]["场景"]["仅场景"][choose_surrounding])
        if "multiple views" not in action
        else "{white background},"
    )
    if action_type == "自慰":
        cum = ""
        censored = ""
    else:
        cum = random.choice(data["R18"]["污渍"])
        censored = data["R18"]["去码"] if not env.censor else data["R18"]["打码"]

    logger.info(
        f"""
>>>>>>>>>>
出处: {choose_game}: {choose_character}
角色: {character}
画风: {style_name}: {style}
审查: {censored}
表情: {emotion}
动作: {choose_action}: {action}
场景: {surrounding}
污渍: {cum}
正面: {pref}
负面: {negative}
<<<<<<<<<<"""
    )

    input_ = format_str(character + artist + censored + emotion + action + surrounding + cum + pref)

    return input_, sm, scale, negative, choose_game, choose_character


def prepare_json(input_, sm, scale, negative):
    json_for_t2i["input"] = input_
    if isinstance(env.img_size, int):
        resolution_list = [[832, 1216], [1024, 1024], [1216, 832]]
        resolution = random.choice(resolution_list)
    elif isinstance(env.img_size, list):
        resolution = env.img_size
    json_for_t2i["parameters"]["width"] = resolution[0]
    json_for_t2i["parameters"]["height"] = resolution[1]
    json_for_t2i["parameters"]["scale"] = env.scale if scale == 0 else scale
    json_for_t2i["parameters"]["sampler"] = env.sampler
    json_for_t2i["parameters"]["steps"] = env.steps
    json_for_t2i["parameters"]["sm"] = env.sm if sm == 0 else True
    json_for_t2i["parameters"]["sm_dyn"] = env.sm_dyn if (env.sm or (sm == 1)) and env.sm_dyn else False
    json_for_t2i["parameters"]["noise_schedule"] = env.noise_schedule
    seed = random.randint(1000000000, 9999999999) if env.seed == -1 else env.seed
    json_for_t2i["parameters"]["seed"] = seed
    json_for_t2i["parameters"]["negative_prompt"] = negative

    return json_for_t2i, seed


times = 0


def t2i(forever: bool):
    global times
    times += 1
    logger.info(f"正在生成第 {times} 张图片...")
    input_, sm, scale, negative, choose_game, choose_character = prepare_input()
    json_for_t2i, seed = prepare_json(input_, sm, scale, negative)
    saved_path = save_image(generate_image(json_for_t2i), "t2i", seed, choose_game, choose_character)
    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    if forever:
        return t2i(True)
    else:
        return saved_path


if __name__ == "__main__":
    try:
        t2i(True)
    except KeyboardInterrupt:
        logger.warning("程序退出...")
