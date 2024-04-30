import io
import os
import platform
import random
import time
import zipfile
from pathlib import Path

import requests
import ujson as json
from loguru import logger

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
    if img_data:
        if seed and choose_game and choose_character:
            with open(f"./output/{type_}/{seed}_{choose_game}_{choose_character}.png", "wb") as file:
                file.write(img_data)
        else:
            with open(f"./output/{type_}/{args[0]}", "wb") as file:
                file.write(img_data)


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


def file_name2path(file_list: list, file_path):
    empty_list = []
    for file in file_list:
        empty_list.append(Path(file_path) / file)
    file_list = empty_list[:]
    return file_list


def open_folder(folder):
    os.startfile(folder)
