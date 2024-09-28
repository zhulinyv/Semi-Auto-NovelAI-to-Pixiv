import os
import random
import time

import cv2
from PIL import Image

from utils.env import env
from utils.imgtools import get_concat_h, get_concat_v, get_img_info, revert_img_info
from utils.jsondata import json_for_t2i
from utils.prepare import logger
from utils.utils import (
    cancel_probabilities_for_item,
    choose_item,
    format_str,
    generate_image,
    read_yaml,
    return_source_or_type_dict,
    return_x64,
    save_image,
    sleep_for_cool,
)


def return_resolution(resolution: str, width: str, height: str):
    if resolution == "自定义(Custom)":
        return width, height
    else:
        resolution = resolution.split("x")
        return resolution[0], resolution[1]


def t2i_by_hand(
    positive: str,
    negative: str,
    text2image_width: str,
    text2image_height: str,
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
            sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)
        json_for_t2i["input"] = positive

        json_for_t2i["parameters"]["width"] = return_x64(int(text2image_width))
        json_for_t2i["parameters"]["height"] = return_x64(int(text2image_height))
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

        if saved_path != "寄":
            imgs_list.append(saved_path)
        else:
            pass

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

        try:
            revert_img_info(imgs_list[0], "./output/t2i/grids/{}.png".format(time_))
            return "./output/t2i/grids/{}.png".format(time_)
        except Image.DecompressionBombError:
            logger.warning("图片过大, 进行压缩...")
            cv2.imwrite(
                "./output/t2i/grids/{}.jpg".format(time_),
                cv2.imread("./output/t2i/grids/{}.png".format(time_)),
                [cv2.IMWRITE_JPEG_QUALITY, 90],
            )
            with open("./output/t2i/grids/{}.txt".format(time_), "w") as infofile:
                infofile.write(get_img_info(imgs_list[0])["Description"])
            return "./output/t2i/grids/{}.jpg".format(time_)

    else:
        return saved_path


def prepare_input(
    fixed_artist,
    fixed_prefix,
    fixed_negative,
    fixed_source,
    fixed_character,
    fixed_action_type,
    fixed_action,
    fixed_emotion,
    fixed_surrounding,
    fixed_stains,
):
    artists_file = read_yaml("./files/favorites/artists.yaml")
    if fixed_artist != "随机":
        artists_file = cancel_probabilities_for_item(artists_file)
        artist_name = fixed_artist
        artist_data = artists_file[fixed_artist]
    else:
        artist_name, artist_data = choose_item(artists_file)
    artist_tag = artist_data["tag"]
    artist_cfg = artist_data["cfg"]
    artist_sm = artist_data["sm"]
    artist_sm_dyn = artist_data["sm_dyn"]
    artist_sampler = artist_data["sampler"]
    artist_noise_schedule = artist_data["noise_schedule"]

    prefixes_file = read_yaml("./files/favorites/prefixes.yaml")
    if fixed_prefix != "随机":
        prefixes_file = cancel_probabilities_for_item(prefixes_file)
        prefix_name = fixed_prefix
        prefix_data = prefixes_file[prefix_name]
    else:
        prefix_name, prefix_data = choose_item(prefixes_file)
    prefix_tag = prefix_data["tag"]

    negative_file = read_yaml("./files/favorites/negative.yaml")
    if fixed_negative != "随机":
        negative_file = cancel_probabilities_for_item(negative_file)
        negative_name = fixed_negative
        negative_data = negative_file[fixed_negative]
    else:
        negative_name, negative_data = choose_item(negative_file)
    negative_tag = negative_data["tag"]

    if fixed_source != "随机":
        characters_file = return_source_or_type_dict(read_yaml("./files/favorites/characters.yaml"))
        print(characters_file)
        source_data = characters_file[fixed_source]
        character_name = random.choice(list(source_data.keys()))
        character_data = source_data[character_name]
        character_source = fixed_source
    else:
        characters_file = read_yaml("./files/favorites/characters.yaml")
        if fixed_character != "随机":
            characters_file = cancel_probabilities_for_item(characters_file)
            character_name = fixed_character
            character_data = characters_file[fixed_character]
        else:
            character_name, character_data = choose_item(characters_file)
        character_source = character_data["source"]
    character_tag = character_data["tag"]

    if fixed_action_type != "随机":
        actions_file = return_source_or_type_dict(read_yaml("./files/favorites/actions.yaml"))
        type_data = actions_file[fixed_action_type]
        action_name = random.choice(list(type_data.keys()))
        action_data = type_data[action_name]
    else:
        actions_file = read_yaml("./files/favorites/actions.yaml")
        if fixed_action != "随机":
            actions_file = cancel_probabilities_for_item(actions_file)
            action_name = fixed_action
            action_data = actions_file[fixed_action]
        else:
            action_name, action_data = choose_item(actions_file)
    action_tag = action_data["tag"]

    emotions_file = read_yaml("./files/favorites/emotions.yaml")
    if fixed_emotion != "随机":
        emotions_file = cancel_probabilities_for_item(emotions_file)
        emotion_name = fixed_emotion
        emotions_data = emotions_file[fixed_emotion]
    else:
        emotion_name, emotions_data = choose_item(emotions_file)
    emotion_tag = emotions_data["tag"]

    surroundings_files = read_yaml("./files/favorites/surroundings.yaml")
    if fixed_surrounding != "随机":
        surroundings_files = cancel_probabilities_for_item(surroundings_files)
        surrounding_name = fixed_surrounding
        surrounding_data = surroundings_files[fixed_surrounding]
    else:
        surrounding_name, surrounding_data = choose_item(surroundings_files)
    surrounding_tag = surrounding_data["tag"]

    stains_file = read_yaml("./files/favorites/stains.yaml")
    if fixed_stains != "随机":
        stains_file = cancel_probabilities_for_item(stains_file)
        stain_name = fixed_stains
        stains_data = stains_file[fixed_stains]
    else:
        stain_name, stains_data = choose_item(stains_file)
    stain_tag = stains_data["tag"]

    if env.censor:
        censored = "{{censored}}, {{{mosaic}}}, {{{{mosaic censored}}}"
    else:
        censored = "uncensored, nsfw, clothed female nude male"

    logger.info(
        f"""
----------
出处: {character_source}
角色: {character_name}: {character_tag}
画风: {artist_name}: {artist_tag}
审查: {"开" if env.censor else "关"}: {censored}
表情: {emotion_name}: {emotion_tag}
动作: {action_name}: {action_tag}
场景: {surrounding_name}: {surrounding_tag}
污渍: {stain_name}: {stain_tag}
正面: {prefix_name}: {prefix_tag}
负面: {negative_name}: {negative_tag}
----------"""
    )

    input_ = format_str(
        f"{character_tag}, {artist_tag}, {censored}, {emotion_tag}, {action_tag}, {surrounding_tag}, {stain_tag}, {prefix_tag}"
    )

    return (
        input_,
        artist_cfg,
        artist_sm,
        artist_sm_dyn,
        artist_sampler,
        artist_noise_schedule,
        character_source,
        character_name,
        negative_tag,
    )


def prepare_json(input_, sm, sm_dyn, scale, sampler, noise_schedule, negative):
    json_for_t2i["input"] = input_
    if isinstance(env.img_size, int):
        resolution_list = [[832, 1216], [1024, 1024], [1216, 832]]
        resolution = random.choice(resolution_list)
    elif isinstance(env.img_size, list):
        resolution = env.img_size
    json_for_t2i["parameters"]["width"] = resolution[0]
    json_for_t2i["parameters"]["height"] = resolution[1]
    json_for_t2i["parameters"]["scale"] = scale
    json_for_t2i["parameters"]["sampler"] = sampler
    json_for_t2i["parameters"]["steps"] = env.steps
    json_for_t2i["parameters"]["sm"] = sm
    json_for_t2i["parameters"]["sm_dyn"] = sm_dyn
    json_for_t2i["parameters"]["noise_schedule"] = noise_schedule
    seed = random.randint(1000000000, 9999999999) if env.seed == -1 else env.seed
    json_for_t2i["parameters"]["seed"] = seed
    json_for_t2i["parameters"]["negative_prompt"] = negative

    return json_for_t2i, seed


def t2i(
    forever: bool,
    fixed_artist,
    fixed_prefix,
    fixed_negative,
    fixed_source,
    fixed_character,
    fixed_action_type,
    fixed_action,
    fixed_emotion,
    fixed_surrounding,
    fixed_stains,
):
    (
        input_,
        artist_cfg,
        artist_sm,
        artist_sm_dyn,
        artist_sampler,
        artist_noise_schedule,
        character_source,
        character_name,
        negative_tag,
    ) = prepare_input(
        fixed_artist,
        fixed_prefix,
        fixed_negative,
        fixed_source,
        fixed_character,
        fixed_action_type,
        fixed_action,
        fixed_emotion,
        fixed_surrounding,
        fixed_stains,
    )
    json_for_t2i, seed = prepare_json(
        input_, artist_sm, artist_sm_dyn, artist_cfg, artist_sampler, artist_noise_schedule, negative_tag
    saved_path = save_image(generate_image(json_for_t2i), "t2i", seed, character_source, character_name)
    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    if forever:
        pass
    else:
        return saved_path
