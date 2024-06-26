import random
import shutil
import time

from loguru import logger

from src.text2image_nsfw import prepare_json
from utils.env import env
from utils.utils import file_path2list, format_str, generate_image, read_json, read_txt, save_image, sleep_for_cool


def prepare_input(
    pref,
    position,
    text2image_sfw_random_artists_top_switch,
    text2image_sfw_random_artists_last_switch,
    text2image_sfw_prevent_to_move_switch,
):
    data = read_json("./files/favorite.json")
    file_list = file_path2list("./files/prompt")
    file_list.remove("done")
    if file_list == []:
        logger.warning("./files/prompt 目录下 *.txt 文件已全部生成过一次!")
        return None
    file: str = random.choice(file_list)

    prompt = read_txt(f"./files/prompt/{file}")

    if pref:
        if position == "最前面(Top)":
            prompt = f"{format_str(pref)}, {format_str(prompt)}"
        else:
            prompt = f"{format_str(prompt)}, {format_str(pref)}"

    def random_artists():
        weight_list = list(data["artists"]["belief"].keys())
        artist = ""
        while artist == "":
            possibility = random.random()
            time.sleep(1)
            for weight in weight_list:
                if possibility >= float(weight):
                    artist_list = list(data["artists"]["belief"][weight].keys())
                    if artist_list != []:
                        style_name = random.choice(artist_list)
                        style = data["artists"]["belief"][weight][style_name]
                        artist = style[0]
                        break
        return artist

    if text2image_sfw_random_artists_top_switch:
        prompt = f"{format_str(random_artists())}, {format_str(prompt)}"
    elif text2image_sfw_random_artists_last_switch:
        prompt = f"{format_str(prompt)}, {format_str(random_artists())}"

    logger.debug("prompt: " + prompt)

    if text2image_sfw_prevent_to_move_switch:
        pass
    else:
        file_list.remove(file)
        shutil.move(f"./files/prompt/{file}", f"./files/prompt/done/{file}")

    return file, prompt


def main(
    forever: bool,
    pref,
    position,
    text2image_sfw_random_artists_top_switch,
    text2image_sfw_random_artists_last_switch,
    text2image_sfw_prevent_to_move_switch,
):
    file, prompt = prepare_input(
        pref,
        position,
        text2image_sfw_random_artists_top_switch,
        text2image_sfw_random_artists_last_switch,
        text2image_sfw_prevent_to_move_switch,
    )

    data = read_json("./files/favorite.json")

    json_for_t2i, seed = prepare_json(prompt, env.sm, env.scale, random.choice(data["negative_prompt"]["belief"]))
    saved_path = save_image(
        generate_image(json_for_t2i), "t2i", str(seed) + file.replace(".txt", "").replace("_", "-"), "None", "None"
    )

    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    if forever:
        return main(True, pref, position)
    else:
        return saved_path
