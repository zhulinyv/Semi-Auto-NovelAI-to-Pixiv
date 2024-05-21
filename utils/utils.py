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


def list_to_str(str_list: list[str]):
    """列表加和字符串

    Args:
        str_list (list[str]): 字符串列表

    Returns:
        empty_str: 字符串
    """
    empty_str = ""
    for i in str_list:
        empty_str += f"{i},"
    return empty_str


def format_str(str_: str):
    """格式化字符串

    Args:
        str_ (str): 字符串

    Returns:
        str_: 格式化后的字符串
    """
    str_ = str_.replace(", ", ",")
    str_ = str_.replace(",", ", ")
    str_ = str_[:-2] if str_[-2:] == ", " else str_
    return str_


def sleep_for_cool(int1, int2):
    """等待指定时间

    Args:
        int1 (int): 下限
        int2 (int): 上限
    """
    sleep_time = round(random.uniform(int1, int2), 3)
    logger.info(f"等待 {sleep_time} 秒后继续...")
    time.sleep(sleep_time)
    return f"等待 {sleep_time} 秒后继续..."


def generate_image(json_data):
    """发送 post 请求

    Args:
        json_data (dict): json 数据

    Returns:
        (bytes): 二进制图片
    """
    if env.proxy != "xxx:xxx":
        proxies = {
            "http": "http://" + env.proxy,
            "https": "http://" + env.proxy,
        }
    else:
        proxies = None
    try:
        rep = requests.post(
            "https://image.novelai.net/ai/generate-image", json=json_data, headers=headers, proxies=proxies
        )
        while rep.status_code in [429, 500]:
            sleep_for_cool(3, 9)
            rep = requests.post(
                "https://image.novelai.net/ai/generate-image", json=json_data, headers=headers, proxies=proxies
            )
            logger.debug(f">>>>> {rep.status_code}")
        rep.raise_for_status()
        logger.success("生成成功!")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()
    except Exception as e:
        logger.error(f"出现错误: {e}")


def save_image(img_data, type_, seed, choose_game, choose_character, *args):
    """保存图片

    Args:
        img_data (bytes): 二进制图片
        type_ (str): 分类
        seed (int): 种子
        choose_game (str): 游戏
        choose_character (str): 角色

    Returns:
        saved_path (str): 保存路径
    """
    try:
        file_name: str = args[0]
        file_name = file_name.replace(".png", "")
        name_list = file_name.split("_")
        choose_character = name_list[2]
    except Exception:
        pass
    if env.save_path == "默认(Default)":
        path = ""
    elif env.save_path == "日期(Date)":
        path = f"/{date.today()}"
    elif env.save_path == "角色(Character)":
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
    """计算剩余水晶

    Returns:
        (int): 剩余水晶数量
    """
    rep = requests.get("https://api.novelai.net/user/subscription", headers=headers)
    if rep.status_code == 200:
        return rep.json()["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    return 0


def check_platform():
    """检测运行平台"""
    if platform.system() == "Windows":
        pass
    else:
        logger.error("仅支持 Window 运行!")
        return


def read_json(path):
    """读取 *.json 文件

    Args:
        path (str|WindowsPath): 文件路径

    Returns:
        (dict): 数据
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_txt(path):
    """读取文本文件

    Args:
        path (str|WindowsPath): 文件路径

    Returns:
        (str): 数据
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def file_path2name(path) -> str:
    """文件路径返还文件名

    Args:
        path (str|WindowsPath): 路径

    Returns:
        (str): 文件名
    """
    return os.path.basename(path)


def file_path2list(path) -> list[str]:
    """文件目录返还文件名列表

    Args:
        path (str|WindowsPath): 目录

    Returns:
        (list[str]): 文件名列表
    """
    return os.listdir(path)


def file_namel2pathl(file_list: list, file_path):
    """文件名列表返还文件路径列表

    Args:
        file_list (list): 文件名列表
        file_path (_type_): 文件路径列表

    Returns:
        (list[str]): 文件路径列表
    """
    empty_list = []
    for file in file_list:
        empty_list.append(Path(file_path) / file)
    file_list = empty_list[:]
    return file_list


def file_path2abs(path):
    """文件相对路径返还绝对路径

    Args:
        path (str|WindowsPath): 相对路径

    Returns:
        (str): 绝对路径
    """
    return os.path.abspath(path)


def file_path2dir(path) -> str:
    """文件路径返还所在目录

    Args:
        path (str|WindowsPath): 路径

    Returns:
        (str): 所在目录
    """
    return os.path.dirname(file_path2abs(path))


def open_folder(folder):
    """打开文件/目录

    Args:
        folder (str|WindowsPath): 文件或目录
    """
    os.startfile(folder)


def gen_script(script_type, *args):
    with open("stand_alone_scripts.py", "w", encoding="utf-8") as script:
        if script_type == "随机涩图":
            script.write(
                """import sys

sys.setrecursionlimit(999999999)

from src.t2i import t2i  # noqa: E402

t2i(True, "{}")
""".format(
                    args[0]
                )
            )
        elif script_type == "随机图片":
            script.write(
                """import sys

sys.setrecursionlimit(999999999)

from src.batchtxt import main  # noqa: E402

main(True, \"\"\"{}\"\"\", "{}")
""".format(
                    args[0], args[1]
                )
            )
        elif script_type == "vibe":
            script.write(
                """from src.vibe import vibe

while 1:
    vibe({}, "{}")
""".format(
                    args[0], args[1]
                )
            )
        else:
            ...


def return_random():
    return "-1"
