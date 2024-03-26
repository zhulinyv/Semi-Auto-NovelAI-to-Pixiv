import random

import ujson as json

from loguru import logger

from utils.utils import *


def generate_by_band(positive: str, negative: str, resolution: str, scale: float, sampler: str, noise_schedule: str, steps: int, sm: bool, seed: str):
    json_for_t2i["input"] = positive
    
    json_for_t2i["parameters"]["width"] = int(resolution.split("x")[0])
    json_for_t2i["parameters"]["height"] = int(resolution.split("x")[1])
    json_for_t2i["parameters"]["scale"] = scale
    json_for_t2i["parameters"]["sampler"] = sampler
    json_for_t2i["parameters"]["steps"] = steps
    json_for_t2i["parameters"]["sm"] = sm
    json_for_t2i["parameters"]["sm_dyn"] = False
    json_for_t2i["parameters"]["noise_schedule"] = noise_schedule
    json_for_t2i["parameters"]["seed"] = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
    json_for_t2i["parameters"]["negative_prompt"] = negative
    
    logger.debug(json_for_t2i)
    
    save_image(generate_image(json_for_t2i), "t2i", seed, "None", "None")
    sleep_for_cool(12, 24)
    
    return f"./output/t2i/{seed}_None_None.png"


def prepare_input():
    with open("./files/favorite.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    artist = random.choice(data["artists"]["belief"])
    pref = random.choice(data["quality_pref"]["belief"])
    negetive = format_str(random.choice(data["negative_prompt"]["belief"]))
    choose_game = random.choice(list(data["character"].keys()))
    choose_character = random.choice(list(data["character"][choose_game].keys()))
    character = list_to_str(data["character"][choose_game][choose_character])
    censored = data["R18"]["去码"] if not env.censor else data["R18"]["打码"]
    action_type = "巨乳" if any(char in character for char in ['huge breasts', 'large breasts', 'medium breasts']) else "普通"
    choose_action: list = random.choice(list(data["R18"]["动作"][f"{action_type}动作"].keys()))
    action = list_to_str(data["R18"]["动作"][f"{action_type}动作"][choose_action])
    emotion_type = "口交" if "oral" in action else "普通"
    choose_emotion = random.choice(list(data["R18"]["表情"][f"{emotion_type}表情"].keys()))
    emotion = list_to_str(data["R18"]["表情"][f"{emotion_type}表情"][choose_emotion])
    choose_surrounding = random.choice(list(data["R18"]["场景"]["仅场景"].keys()))
    surrounding = list_to_str(data["R18"]["场景"]["仅场景"][choose_surrounding])
    cum = random.choice(data["R18"]["射精"])

    logger.info(f"""
>>>>>>>>>>
游戏: {choose_game}: {choose_character}
角色: {character}
画风: {artist}
审查: {censored}
表情: {emotion}
动作: {action}
场景: {surrounding}
射精: {cum}
正面: {pref}
负面: {negetive}
<<<<<<<<<<""")

    input_ = format_str(pref + character + artist + censored + emotion + action + surrounding + cum)

    return input_, negetive, choose_game, choose_character


def prepare_json(input_, negetive):
    json_for_t2i["input"] = input_
    if isinstance(env.img_size, int):
        resolution_list = [[832, 1216],[1024, 1024], [1216, 832]]
        resolution = random.choice(resolution_list)
    elif isinstance(env.img_size, list):
        resolution = env.img_size
    json_for_t2i["parameters"]["width"] = resolution[0]
    json_for_t2i["parameters"]["height"] = resolution[1]
    json_for_t2i["parameters"]["scale"] = env.scale
    json_for_t2i["parameters"]["sampler"] = env.sampler
    json_for_t2i["parameters"]["steps"] = env.steps
    json_for_t2i["parameters"]["sm"] = env.sm
    json_for_t2i["parameters"]["sm_dyn"] = env.sm_dyn if env.sm and env.sm_dyn else False
    json_for_t2i["parameters"]["noise_schedule"] = env.noise_schedule
    seed = random.randint(1000000000, 9999999999) if env.seed == -1 else env.seed
    json_for_t2i["parameters"]["seed"] = seed
    json_for_t2i["parameters"]["negative_prompt"] = negetive

    return json_for_t2i, seed


times = 0

def t2i(forever: bool):
    try:
        global times
        times += 1
        logger.info(f"正在生成第{times}张图片...")
        input_, negative, choose_game, choose_character = prepare_input()
        json_for_t2i, seed = prepare_json(input_, negative)
        img_data = generate_image(json_for_t2i)
        save_image(img_data, "t2i", seed, choose_game, choose_character)
        sleep_for_cool(12, 24)
    except GeneratorExit:
        logger.error("生成失败")

    if forever:
        return t2i(True)
    else:
        return f"./output/t2i/{seed}_{choose_game}_{choose_character}.png"



if __name__ == "__main__":
    try:
        t2i(True)
    except KeyboardInterrupt:
        logger.warning("程序退出...")
