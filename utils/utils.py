import io
import os
import platform
import random
import time
import zipfile
from datetime import date
from pathlib import Path

import requests
import ujson as json
from loguru import logger

from utils.env import env
from utils.jsondata import headers


def list_to_str(str_list: list):
    empty_str = ""
    for i in str_list:
        empty_str += f"{i},"
    return empty_str


def format_str(str_: str):
    str_ = str_.replace(", ", ",")
    str_ = str_.replace(",", ", ")
    str_ = str_[:-2] if str_[-2:] == ", " else str_
    return str_


def sleep_for_cool(int1, int2):
    sleep_time = round(random.uniform(int1, int2), 3)
    logger.info(f"等待 {sleep_time} 秒后继续...")
    time.sleep(sleep_time)
    return f"等待 {sleep_time} 秒后继续..."


def generate_image(json_data):
    try:
        rep = requests.post("https://image.novelai.net/ai/generate-image", json=json_data, headers=headers)
        while rep.status_code in [429, 500]:
            sleep_for_cool(3, 9)
            rep = requests.post("https://image.novelai.net/ai/generate-image", json=json_data, headers=headers)
            logger.debug(f">>>>> {rep.status_code}")
        rep.raise_for_status()
        logger.success("生成成功!")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()
    except Exception as e:
        logger.error(f"出现错误: {e}")


def save_image(img_data, type_, seed, choose_game, choose_character, *args):
    try:
        file_name: str = args[0]
        file_name = file_name.replace(".png", "")
        name_list = file_name.split("_")
        choose_character = name_list[2]
    except Exception:
        pass
    if env.save_path == "默认":
        path = ""
    elif env.save_path == "日期":
        path = f"/{date.today()}"
    elif env.save_path == "角色":
        path = f"/{choose_character}"
    else:
        path = ""
    if not os.path.exists(f"./output/{type_}{path}"):
        os.mkdir(f"./output/{type_}{path}")

    if img_data:
        if seed and choose_game and choose_character:
            saved_path = f"./output/{type_}{path}/{seed}_{choose_game}_{choose_character}.png"
            with open(saved_path, "wb") as file:
                file.write(img_data)
        else:
            saved_path = f"./output/{type_}{path}/{args[0]}"
            with open(saved_path, "wb") as file:
                file.write(img_data)
        return saved_path
    else:
        return "寄"


def inquire_anlas():
    rep = requests.get("https://api.novelai.net/user/subscription", headers=headers)
    if rep.status_code == 200:
        return rep.json()["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    return 0


def check_platform():
    if platform.system() == "Windows":
        pass
    else:
        logger.error("仅支持 Window 运行!")
        return


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def file_path2name(path) -> str:
    return os.path.basename(path)


def file_path2list(path) -> list:
    return os.listdir(path)


def file_namel2pathl(file_list: list, file_path):
    empty_list = []
    for file in file_list:
        empty_list.append(Path(file_path) / file)
    file_list = empty_list[:]
    return file_list


def file_path2abs(path):
    return os.path.abspath(path)


def file_path2dir(path) -> str:
    return os.path.dirname(file_path2abs(path))


def open_folder(folder):
    os.startfile(folder)


def gen_script(script_type, *args):
    with open("stand_alone_scripts.py", "w", encoding="utf-8") as script:
        if script_type == "随机涩图":
            script.write(
                """import sys

sys.setrecursionlimit(999999999)

from src.t2i import t2i  # noqa: E402

t2i(True)
"""
            )
        elif script_type == "随机图片":
            script.write(
                """import sys

sys.setrecursionlimit(999999999)

from src.batchtxt import main  # noqa: E402

main(True, "{}", "{}")
""".format(
                    args[0], args[1]
                )
            )
        else:
            ...


def return_random():
    return "-1"
