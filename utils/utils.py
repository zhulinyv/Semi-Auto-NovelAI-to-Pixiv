import io
import os
import random
import requests
import shutil
import time
import zipfile

from loguru import logger

need_dir_list = ["./output", "./output/t2i", "./output/choose_for_i2i", "./output/i2i/", "./output/pixiv", "./output/choose_for_upscale" ,"./output/upscale", "./output/mosaic"]

if not os.path.exists(".env"):
    shutil.copyfile(".env.example", ".env")
for dir in need_dir_list:
    if not os.path.exists(dir):
        os.mkdir(dir)

from utils.env import env



headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6',
    'Authorization': f'Bearer {env.token if env.token != "xxx" else logger.error("未配置 token!")}',
    'Referer': 'https://novelai.net',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'Sec-Ch-Ua-mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}
json_for_t2i = {
    "input": str,
    "model": "nai-diffusion-3",
    "action": "generate",
    "parameters": {
        "params_version": 1,
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "ucPreset": 3,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": False,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": False,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        "noise_schedule": str,
        "legacy_v3_extend": False,
        "reference_information_extracted": 1,
        "reference_strength": 0.6,
        "seed": int,
        "negative_prompt": str,
    },
}
json_for_i2i = {
    "input": str,
    "model": "nai-diffusion-3",
    "action": "img2img",
    "parameters": {
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "strength": float,
        "noise": 0,
        "ucPreset": 3,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": False,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": True,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        "noise_schedule": str,
        "legacy_v3_extend": False,
        "params_version": 1,
        "reference_information_extracted": 1,
        "reference_strength": 0.6,
        "seed": int,
        "image": str,
        "extra_noise_seed": int,
        "negative_prompt": str
    }
}


def list_to_str(str_list: list):
    empty_str = ""
    for i in str_list:
        empty_str += f"{i},"
    return empty_str

def format_str(str_: str):
    str_ = str_.replace(", ", ',')
    str_ = str_.replace(",", ', ')
    str_ = str_[:-2] if str_[-2:] == ", " else str_
    return str_

def format_path(str_: str):
    if str_[-1] == "/":
        str_ = str_[:-1]
        return str_
    else:
        return str_

def sleep_for_cool(int1, int2):
    sleep_time = round(random.uniform(int1, int2), 3)
    logger.info(f"等待 {sleep_time} 后继续...")
    time.sleep(sleep_time)
    return f"等待 {sleep_time} 后继续..."

def generate_image(json_data):
    try:
        rep = requests.post("https://api.novelai.net/ai/generate-image", json=json_data, headers=headers)
        rep.raise_for_status()
        logger.success("生成成功!")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()

    except Exception as e:
        logger.error(f"出现错误: {e}")
        return None

def save_image(img_data, type_, seed, choose_game, choose_character):
    if img_data != None:
        with open(f"./output/{type_}/{seed}_{choose_game}_{choose_character}.png", "wb") as file:
            file.write(img_data)
    else:
        pass

def inquire_anlas():
    rep = requests.get('https://api.novelai.net/user/subscription', headers=headers)
    if rep.status_code == 200:
        return rep.json()['trainingStepsLeft']['fixedTrainingStepsLeft']
    return 0