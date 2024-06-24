import random
import shutil

from loguru import logger

from src.text2image_nsfw import prepare_json
from utils.env import env
from utils.utils import file_path2list, format_str, generate_image, read_json, read_txt, save_image, sleep_for_cool


def prepare_input(pref, position):
    file_list = file_path2list("./files/prompt")
    file_list.remove("done")
    if file_list == []:
        logger.warning("./files/prompt 目录下 *.txt 文件已全部生成过一次!")
        return None
    file: str = random.choice(file_list)

    prompt = read_txt(f"./files/prompt/{file}")

    if pref != "":
        if position == "最前面(Top)":
            prompt = f"{format_str(pref)}, {prompt}"
        else:
            prompt = f"{format_str(prompt)}, {pref}"
    logger.debug("prompt: " + prompt)

    file_list.remove(file)
    shutil.move(f"./files/prompt/{file}", f"./files/prompt/done/{file}")

    return file, prompt


def main(forever: bool, pref, position):
    file, prompt = prepare_input(pref, position)

    data = read_json("./files/favorite.json")

    json_for_t2i, seed = prepare_json(prompt, env.sm, env.scale, random.choice(data["negative_prompt"]["belief"]))
    saved_path = save_image(
        generate_image(json_for_t2i), "t2i", str(seed) + file.replace(".txt", "").replace("_", "-"), "None", "None"
    )

    sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

    if forever:
        return main(True)
    else:
        return saved_path
