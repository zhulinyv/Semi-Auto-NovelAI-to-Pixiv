import os
import random
import shutil

from loguru import logger

from t2i import prepare_json

from utils.predir import *
from utils.env import env
from utils.utils import generate_image, save_image, sleep_for_cool



def main(forever: bool):
    file_list = os.listdir("./files/prompt")
    file_list.remove("done")
    if file_list == []:
        logger.warning("./files/prompt 目录下 *.txt 文件已全部生成过一次!")
        return None
    file = random.choice(file_list)

    with open(f"./files/prompt/{file}") as f:
        prompt = f.read()
    logger.debug("prompt: " + prompt)

    json_for_t2i, seed = prepare_json(prompt, env.sm, env.scale, env.negetive)
    img_data = generate_image(json_for_t2i)
    if img_data != None:
        save_image(img_data, "t2i", str(seed) + file.replace(".txt", ''), "None", "None")
        file_list.remove(file)
        shutil.move(f"./files/prompt/{file}", f"./files/prompt/done/{file}")
    else:
        pass

    sleep_for_cool(12, 24)

    if forever:
        return main(True)
    else:
        return "./output/t2i/{}_None_None.png".format(str(seed) + file.replace(".txt", ''))


if __name__ == "__main__":
    try:
        main(True)
    except KeyboardInterrupt:
        logger.warning("程序退出...")