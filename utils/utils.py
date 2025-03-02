import asyncio
import base64
import hmac
import io
import os
import platform
import random
import re
import subprocess
import sys
import time
import tkinter as tk
import zipfile
from datetime import date
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tkinter.filedialog import askopenfilename

import gradio as gr
import numpy as np
import requests
import ujson as json
import yaml
from PIL import Image

from utils.env import env
from utils.jsondata import headers
from utils.prepare import logger

PATH = os.getcwd()

MODEL = [
    "nai-diffusion-2",
    "nai-diffusion-3",
    "nai-diffusion-furry-3",
    "nai-diffusion-4-curated-preview",
    "nai-diffusion-4-full",
]
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
    "k_dpmpp_2m_sde",
    "ddim_v3",
]
... if "nai-diffusion-4" not in env.model else SAMPLER.remove("ddim_v3")
NOISE_SCHEDULE = ["native", "karras", "exponential", "polyexponential"]
... if "nai-diffusion-4" not in env.model else NOISE_SCHEDULE.remove("native")
CHARACTER_POSITION = [f"{chr(letter)}{number}" for letter in range(ord("A"), ord("F")) for number in range(1, 6)]
FAVORTES_FILE = os.listdir("./files/favorites")
THEME_LIST = [""] + [
    "gradio/base",
    "gradio/glass",
    "gradio/monochrome",
    "gradio/seafoam",
    "gradio/soft",
    "gradio/dracula_test",
    "abidlabs/dracula_test",
    "abidlabs/Lime",
    "abidlabs/pakistan",
    "Ama434/neutral-barlow",
    "dawood/microsoft_windows",
    "finlaymacklon/smooth_slate",
    "Franklisi/darkmode",
    "freddyaboulton/dracula_revamped",
    "freddyaboulton/test-blue",
    "gstaff/xkcd",
    "Insuz/Mocha",
    "Insuz/SimpleIndigo",
    "JohnSmith9982/small_and_pretty",
    "nota-ai/theme",
    "nuttea/Softblue",
    "ParityError/Anime",
    "reilnuud/polite",
    "remilia/Ghostly",
    "rottenlittlecreature/Moon_Goblin",
    "step-3-profit/Midnight-Deep",
    "Taithrah/Minimal",
    "ysharma/huggingface",
    "ysharma/steampunk",
    "NoCrypt/miku",
]

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
    if env.skip_format_str:
        return str_
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


def position_to_float(position: str):
    offset = 0.1
    letter_dict = {chr(65 + i): i * 0.2 + offset for i in range(5)}
    number_dict = {str(i + 1): i * 0.2 + offset for i in range(5)}
    letter, number = position
    return round(letter_dict[letter], 1), round(number_dict[number], 1)


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


def choose_item(data):
    """按照概率随机选择条目

    Args:
        data (dict): 读取的 favorites 中的 yaml 文件

    Returns:
        tuple[str, dict]: 名称, 条目
    """
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


def find_wild_card_and_replace_tag(text):
    """查找并替换 wildcard

    Args:
        text (str): 要执行该操作的字符串

    Returns:
        str: 替换后的字符串
    """
    pattern = r"<([^:]+):([^>]+)>"
    matchers = re.findall(pattern, text)
    for wild_card in matchers:
        if wild_card[1] != "随机":
            yaml_data = cancel_probabilities_for_item(read_yaml("./files/favorites/{}.yaml".format(wild_card[0])))
            text = text.replace("<{}:{}>".format(wild_card[0], wild_card[1]), yaml_data[wild_card[1]]["tag"])
        else:
            _, yaml_data = choose_item(read_yaml("./files/favorites/{}.yaml".format(wild_card[0])))
            text = text.replace("<{}:{}>".format(wild_card[0], wild_card[1]), yaml_data["tag"])
    logger.info(f"发现 {len(matchers)} 个 wildcard, 已完成替换!") if len(matchers) != 0 else ...
    return format_str(text)


def generate_image(json_data):
    """发送 post 请求

    Args:
        json_data (dict): json 数据

    Returns:
        (bytes): 二进制图片
    """
    with open("start.json", "w") as f:
        json.dump({"positive": json_data["input"], "negative": json_data["parameters"]["negative_prompt"]}, f)

    json_data["input"] = find_wild_card_and_replace_tag(json_data["input"])
    json_data["parameters"]["negative_prompt"] = find_wild_card_and_replace_tag(
        json_data["parameters"]["negative_prompt"]
    )
    if "nai-diffusion-4" in env.model:
        json_data["parameters"]["v4_prompt"]["caption"]["base_caption"] = find_wild_card_and_replace_tag(
            json_data["parameters"]["v4_prompt"]["caption"]["base_caption"]
        )
        json_data["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = find_wild_card_and_replace_tag(
            json_data["parameters"]["v4_negative_prompt"]["caption"]["base_caption"]
        )

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
        json_data["prompt"] = find_wild_card_and_replace_tag(json_data["prompt"])
    except KeyError:
        pass

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
        os.mkdir(f"./output/{type_}{path}")

    if img_data:
        if seed and choose_game and choose_character:
            saved_path = f"./output/{type_}{path}/{seed}{generate_random_str(6)}_{choose_game}_{choose_character}.png"
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
    return platform.system()


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


def cancel_probabilities_for_item(d: dict):
    """删除读取的 favorites 中的 yaml 文件中的概率键

    Args:
        d (dict): 读取的 favorites 中的 yaml 文件

    Returns:
        dict: 新的字典数据
    """
    n = {}
    for k, v in d.items():
        try:
            n.update(v)
        except TypeError:
            pass
    return n


def return_keys_list(d: dict):
    """返回字典的键

    Args:
        d (dict): 字典

    Returns:
        list[str]: 键名列表
    """
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
    names_list = ["随机"] + names_list
    return names_list


def update_t2i_nsf_dropdown_list():
    characters_file = read_yaml("./files/favorites/characters.yaml")
    actions_file = read_yaml("./files/favorites/actions.yaml")
    return (
        gr.update(choices=return_names_list(read_yaml("./files/favorites/artists.yaml")), visible=True),
        gr.update(choices=return_names_list(read_yaml("./files/favorites/prefixes.yaml")), visible=True),
        gr.update(choices=return_names_list(read_yaml("./files/favorites/negative.yaml")), visible=True),
        gr.update(
            choices=["随机"] + return_source_or_type_list(cancel_probabilities_for_item(characters_file)),
            visible=True,
        ),
        gr.update(choices=return_names_list(characters_file), visible=True),
        gr.update(
            choices=["随机"] + return_source_or_type_list(cancel_probabilities_for_item(actions_file)),
            visible=True,
        ),
        gr.update(choices=return_names_list(actions_file), visible=True),
        gr.update(choices=return_names_list(read_yaml("./files/favorites/emotions.yaml")), visible=True),
        gr.update(choices=return_names_list(read_yaml("./files/favorites/surroundings.yaml")), visible=True),
        gr.update(choices=return_names_list(read_yaml("./files/favorites/stains.yaml")), visible=True),
    )


def update_name_to_dropdown_list(item_to_del):
    return gr.update(choices=return_names_list(read_yaml(f"./files/favorites/{item_to_del}")), visible=True)


def update_image_size(d):
    w, h = (d["layers"][0]).size
    return gr.update(height=h, width=w)


def add_item_for_yaml(
    item_to_add,
    tag_to_add,
    name_to_add,
    probability_to_add,
    source_to_add,
    type_to_add,
    sampler_to_add,
    noise_schedule_to_add,
    cfg_to_add,
    sm_to_add,
    sm_dyn_to_add,
    variety_to_add,
    decrisp_to_add,
):
    yaml_file = read_yaml(yaml_path := f"./files/favorites/{item_to_add}")
    if item_to_add == "actions.yaml":
        yaml_file[probability_to_add][name_to_add] = {"tag": tag_to_add, "type": type_to_add}
    elif item_to_add == "artists.yaml":
        yaml_file[probability_to_add][name_to_add] = {
            "tag": tag_to_add,
            "cfg": cfg_to_add,
            "sm": sm_to_add,
            "sm_dyn": sm_dyn_to_add,
            "variety": variety_to_add,
            "decrisp": decrisp_to_add,
            "sampler": sampler_to_add,
            "noise_schedule": noise_schedule_to_add,
        }
    elif item_to_add == "characters.yaml":
        yaml_file[probability_to_add][name_to_add] = {"tag": tag_to_add, "source": source_to_add}
    else:
        yaml_file[probability_to_add][name_to_add] = {"tag": tag_to_add}
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_file, f, allow_unicode=True)
    return (
        None,
        "已添加",
        None,
        probability_to_add,
        None,
        None,
        sampler_to_add,
        noise_schedule_to_add,
        cfg_to_add,
        sm_to_add,
        sm_dyn_to_add,
    )


def del_item_for_yaml(item_to_del, name_to_del):
    yaml_file = read_yaml(yaml_path := f"./files/favorites/{item_to_del}")
    for probability in ["较大概率选中", "中等概率选中", "较小概率选中"]:
        try:
            del yaml_file[probability][name_to_del]
        except KeyError:
            pass
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_file, f, allow_unicode=True)
    return item_to_del, update_name_to_dropdown_list(item_to_del)


def add_wildcard_to_textbox(positive_input, negative_input, wildcard_file, wildcard_name):
    if wildcard_file != "negative.yaml":
        return (
            format_str(positive_input) + ", <{}:{}>,".format(wildcard_file.replace(".yaml", ""), wildcard_name),
            negative_input,
        )
    else:
        return positive_input, format_str(negative_input) + f", <negative:{wildcard_name}>,"


def return_wildcard_tag(wildcard_file, wildcard_name):
    if wildcard_name == "随机":
        return None
    else:
        return cancel_probabilities_for_item(read_yaml(f"./files/favorites/{wildcard_file}"))[wildcard_name]["tag"]


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


def stop_generate():
    logger.warning("正在停止生成...")
    with open("./output/temp.json", "w") as f:
        json.dump({"break": True}, f)
    return


def silent_wrapper(func):
    def wrapped():
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        func()

    return wrapped


def install_requirements(path):
    logger.debug(f"开始安装所需依赖 {path} ...")
    command = f"{sys.executable} -s -m pip install -r {path}"
    if env.skip_else_log:
        devnull = subprocess.DEVNULL
    else:
        devnull = None
    subprocess.call(command, stdout=devnull, stderr=devnull)
    logger.success("安装完成!")
    return


def tk_window_asksavefile(init_dir=os.getcwd(), suffix="") -> str:
    window = tk.Tk()
    window.wm_attributes("-topmost", 1)
    window.withdraw()
    filename = askopenfilename(initialdir=init_dir, filetypes=[("", suffix)])
    return filename


async def tk_asksavefile_asy(init_dir=os.getcwd(), suffix="") -> str:
    fname = await asyncio.to_thread(tk_window_asksavefile, init_dir, suffix)
    return fname


def return_array_iamge(path):
    if path:
        with Image.open(path) as image:
            return np.array(image)


def gen_script(script_type, *args):
    with open("stand_alone_scripts.py", "w", encoding="utf-8") as script:
        if script_type == "随机蓝图":
            script.write(
                """from playsound import playsound

from src.text2image_nsfw import t2i
from utils.env import env
from utils.prepare import logger

times = 0
_times = 0
while times + 1 <= env.times_for_scripts:
    if env.times_for_scripts == 0:
        _times += 1
    else:
        times += 1
    info = "正在生成第 " + str(_times if env.times_for_scripts == 0 else times) + " 张图片..."
    logger.info(info)
    t2i(True, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")

if not env.skip_finish_sound:
    playsound("./files/webui/download_finish.mp3")
""".format(
                    args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9]
                )
            )
        elif script_type == "随机图片":
            script.write(
                """from playsound import playsound

from src.text2image_sfw import main
from utils.env import env
from utils.prepare import logger

times = 0
_times = 0
while times + 1 <= env.times_for_scripts:
    if env.times_for_scripts == 0:
        _times += 1
    else:
        times += 1
    info = "正在生成第 " + str(_times if env.times_for_scripts == 0 else times) + " 张图片..."
    logger.info(info)
    main(True, \"\"\"{}\"\"\", "{}", "{}", "{}", "{}")

if not env.skip_finish_sound:
    playsound("./files/webui/download_finish.mp3")
""".format(
                    args[0], args[1], args[2], args[3], args[4]
                )
            )
        else:
            ...
    logger.success("生成成功, 运行 run_stand_alone_scripts.bat 即可独立执行该操作")
