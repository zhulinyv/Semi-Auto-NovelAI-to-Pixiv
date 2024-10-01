import base64
import hmac
import io
import os
import platform
import random
import time
import zipfile
from datetime import date
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import requests
import ujson as json
import yaml
from PIL import Image

from utils.env import env
from utils.jsondata import headers
from utils.prepare import logger

PATH = os.getcwd()

RESOLUTION = [
    "832x1216",
    "1216x832",
    "1024x1024",
    "512x768",
    "768x768",
    "640x640",
    "1024x1536",
    "1536x1024",
    "1472x1472",
    "1088x1920",
    "1920x1088",
]
SAMPLER = [
    "k_euler",
    "k_euler_ancestral",
    "k_dpmpp_2s_ancestral",
    "k_dpmpp_2m",
    "k_dpmpp_sde",
    "ddim_v3",
]
NOISE_SCHEDULE = ["native", "karras", "exponential", "polyexponential"]


if env.proxy != "xxx:xxx":
    proxies = {
        "http": "http://" + env.proxy,
        "https": "http://" + env.proxy,
    }
else:
    proxies = None

if env.proxy != "xxx:xxx":
    os.environ["http_proxy"] = env.proxy
    os.environ["https_proxy"] = env.proxy


def format_str(str_: str):
    """格式化字符串

    Args:
        str_ (str): 字符串

    Returns:
        str_: 格式化后的字符串
    """
    str_ = str_.replace(", ", ",")
    str_ = str_.replace(",,", ",")
    str_ = str_.replace(",,,", ",")
    str_ = str_.replace(",", ", ")
    str_ = str_[:-2] if str_[-2:] == ", " else str_
    return str_


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
    return format_str(empty_str)


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


def generate_random_str(randomlength):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ""
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def inquire_anlas():
    """计算剩余点数

    Returns:
        (int): 剩余点数数量
    """
    try:
        rep = requests.get("https://api.novelai.net/user/subscription", headers=headers, proxies=proxies)
        if rep.status_code == 200:
            return rep.json()["trainingStepsLeft"]["fixedTrainingStepsLeft"]
        return 0
    except Exception as e:
        return str(e)


def generate_image(json_data):
    """发送 post 请求

    Args:
        json_data (dict): json 数据

    Returns:
        (bytes): 二进制图片
    """
    try:
        rep = requests.post(
            "https://image.novelai.net/ai/generate-image", json=json_data, headers=headers, proxies=proxies
        )
        while rep.status_code == 429:
            sleep_for_cool(3, 9)
            rep = requests.post(
                "https://image.novelai.net/ai/generate-image", json=json_data, headers=headers, proxies=proxies
            )
            logger.debug(f">>>>> {rep.status_code}")
        rep.raise_for_status()
        logger.success("生成成功!")
        logger.warning(f"剩余点数: {inquire_anlas()}")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()
    except Exception as e:
        logger.error(f"出现错误: {e}")


def generate_image_for_director_tools(json_data):
    """发送 post 请求(For director tools)

    Args:
        json_data (dict): json 数据

    Returns:
        (bytes): 二进制图片
    """
    try:
        rep = requests.post(
            "https://image.novelai.net/ai/augment-image", json=json_data, headers=headers, proxies=proxies
        )
        while rep.status_code == 429:
            sleep_for_cool(3, 9)
            rep = requests.post(
                "https://image.novelai.net/ai/augment-image", json=json_data, headers=headers, proxies=proxies
            )
            logger.debug(f">>>>> {rep.status_code}")
        rep.raise_for_status()
        logger.success("生成成功!")
        logger.warning(f"剩余点数: {inquire_anlas()}")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            if json_data["req_type"] == "bg-removal":
                with zip.open("image_0.png") as masked, zip.open("image_1.png") as generated, zip.open(
                    "image_2.png"
                ) as blend:
                    return masked.read(), generated.read(), blend.read()
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
        if choose_character:
            path = f"/{choose_character}"
        else:
            path = ""
    elif env.save_path == "出处(Origin)":
        if choose_character:
            path = f"/{choose_game}"
        else:
            path = ""
    elif env.save_path == "画风(Artists)":
        with Image.open(BytesIO(img_data)) as image:
            info = image.info
            prompt = json.loads(info["Comment"])["prompt"]
        artists_data = read_yaml("./files/favorites/artists.yaml")
        artists_data = cancel_probabilities_for_item(artists_data)
        for artist in list(artists_data.keys()):
            artists = artists_data[artist]["tag"]
            if format_str(artists) in prompt:
                path = f"/{artist}"
            else:
                path = ""
    else:
        path = ""
    if not os.path.exists(f"./output/{type_}{path}"):
        os.chdir(PATH)
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


def save_image_for_director_tools(type_, image_data):
    """保存图片

    Args:
        type_ (str): 分类
        image_data (bytes): 二进制图片

    Returns:
        saved_path (str): 保存路径
    """
    if env.save_path == "默认(Default)":
        path = ""
    elif env.save_path == "日期(Date)":
        path = f"/{date.today()}"
    else:
        path = ""
    saved_path = f"./output/{type_}{path}/{generate_random_str(10)}.png"
    if not os.path.exists(f"./output/{type_}{path}"):
        os.mkdir(f"./output/{type_}{path}")
    if type_ == "bg-removal":
        saved_paths = []
        for image in image_data:
            saved_path = f"./output/{type_}{path}/{generate_random_str(10)}.png"
            saved_paths.append(saved_path)
            with open(saved_path, "wb") as file:
                file.write(image)
        return saved_paths
    else:
        with open(saved_path, "wb") as file:
            file.write(image_data)
        return saved_path


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


def read_yaml(path):
    """读取 *.yaml 文件

    Args:
        path (str|WindowsPath): 文件路径

    Returns:
        (dict): 数据
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def choose_item(data):
    item = None
    while item is None:
        possibility = random.random()
        if possibility >= 0.5:
            choice = "较大概率选中"
        elif possibility >= 0.15:
            choice = "中等概率选中"
        elif possibility >= 0.0:
            choice = "较小概率选中"
        if data[choice] is None:
            item = None
        else:
            name = random.choice(list(data[choice].keys()))
            item = data[choice][name]
    return name, item


def cancel_probabilities_for_item(d: dict):
    n = {}
    for k, v in d.items():
        try:
            n.update(v)
        except TypeError:
            pass
    return n


def return_keys_list(d: dict):
    keys_list = list(d.keys())
    return keys_list


def return_source_or_type_list(d: dict):
    sources = []
    for name in return_keys_list(d):
        try:
            source = d[name]["source"]
        except KeyError:
            source = d[name]["type"]
        if source not in sources:
            sources.append(source)
    return sources


def return_source_or_type_dict(d: dict):
    n = {}
    d = cancel_probabilities_for_item(d)
    for source in return_source_or_type_list(d):
        n.update({source: {}})

    for name in return_keys_list(d):
        try:
            n[(d[name]["source"])][name] = {"tag": d[name]["tag"]}

        except KeyError:
            n[(d[name]["type"])][name] = {"tag": d[name]["tag"]}

    return n


def return_names_list(d: dict):
    names_list = return_keys_list(cancel_probabilities_for_item(d))
    names_list.append("随机")
    return names_list


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


def return_random():
    return "-1"


def return_x64(int_: int):
    """返回最接近 64 倍数的整数

    Args:
        int_ (int): 整数

    Returns:
        (int): 调整后的整数
    """
    if int_ <= 64:
        int_ = 64
    elif int_ % 64 == 0:
        pass
    elif int_ / 64 % 1 >= 0.5:
        int_ = (int_ // 64 + 1) * 64
    else:
        int_ = (int_ // 64) * 64
    return int_


def get_sign(data: str, key: str):
    key = key.encode("utf-8")
    message = data.encode("utf-8")
    sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
    sign = str(sign, "utf-8")
    return sign


def gen_script(script_type, *args):
    with open("stand_alone_scripts.py", "w", encoding="utf-8") as script:
        if script_type == "随机蓝图":
            script.write(
                """from utils.prepare import logger

from src.text2image_nsfw import t2i

times = 0
while 1:
    times += 1
    info = "正在生成第 " + str(times) + " 张图片..."
    logger.info(info)
    t2i(True, "{}", "{}", "{}", "{}", \"\"\"{}\"\"\", {})
""".format(
                    args[0], args[1], args[2], args[3], args[4], args[5]
                )
            )
        elif script_type == "随机图片":
            script.write(
                """
                from utils.prepare import logger
from src.text2image_sfw import main

times = 0
while 1:
    times += 1
    info = "正在生成第 " + str(times) + " 张图片..."
    logger.info(info)
    main(True, \"\"\"{}\"\"\", "{}", "{}", "{}", "{}")
""".format(
                    args[0], args[1], args[2], args[3], args[4]
                )
            )
        else:
            ...
    logger.success("生成成功, 运行 run_stand_alone_scripts.bat 即可独立执行该操作")
