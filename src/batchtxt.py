import random
import shutil

from loguru import logger

from src.t2i import prepare_json
from utils.env import env
from utils.utils import file_path2list, format_str, generate_image, read_json, save_image, sleep_for_cool


def main(forever: bool, pref, position):
    file_list = file_path2list("./files/prompt")
    file_list.remove("done")
    if file_list == []:
        logger.warning("./files/prompt 目录下 *.txt 文件已全部生成过一次!")
        return None
    file: str = random.choice(file_list)

    with open(f"./files/prompt/{file}") as f:
        prompt = f.read()
    if pref != "":
        if position == "最前面(Top)":
            prompt = f"{format_str(pref)}, {prompt}"
        else:
            prompt = f"{format_str(prompt)}, {pref}"
    logger.debug("prompt: " + prompt)

    data = read_json("./files/favorite.json")

    json_for_t2i, seed = prepare_json(prompt, env.sm, env.scale, random.choice(data["negative_prompt"]["belief"]))
    save_image(
        generate_image(json_for_t2i), "t2i", str(seed) + file.replace(".txt", "").replace("_", "-"), "None", "None"
    )

    file_list.remove(file)
    shutil.move(f"./files/prompt/{file}", f"./files/prompt/done/{file}")

    sleep_for_cool(env.t2i_cool_time - 6, env.t2i_cool_time + 6)

    if forever:
        return main(True)
    else:
        return "./output/t2i/{}_None_None.png".format(str(seed) + file.replace(".txt", "").replace("_", "-"))


if __name__ == "__main__":
    try:
        main(True)
    except KeyboardInterrupt:
        logger.warning("程序退出...")
