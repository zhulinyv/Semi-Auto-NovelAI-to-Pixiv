import random
import shutil

from src.text2image_nsfw import prepare_json
from utils.env import env
from utils.prepare import logger
from utils.utils import (
    choose_item,
    file_path2list,
    format_str,
    generate_image,
    read_txt,
    read_yaml,
    save_image,
    sleep_for_cool,
)


def prepare_input(
    pref,
    position,
    text2image_sfw_random_artists_top_switch,
    text2image_sfw_random_artists_last_switch,
    text2image_sfw_prevent_to_move_switch,
):
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
        artists_file = read_yaml("./files/favorites/artists.yaml")
        artist_name, artist_data = choose_item(artists_file)
        artist_tag = artist_data["tag"]
        return artist_tag

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

    negative_data = read_yaml("./files/favorites/negative.yaml")

    json_for_t2i, seed = prepare_json(prompt, env.sm, env.scale, choose_item(negative_data)["tag"])
    saved_path = save_image(
        generate_image(json_for_t2i), "t2i", str(seed) + file.replace(".txt", "").replace("_", "-"), "None", "None"
    )

    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    if forever:
        pass
    else:
        return saved_path
