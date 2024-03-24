import io
import random
import requests
import time
import zipfile

import ujson as json

from loguru import logger

from utils.utils import *
from utils.imgtools import get_img_info, img_to_base64



def prepare_json(imginfo: dict, imgpath):
    if imginfo["Software"] != "NovelAI":
        logger.error("不是 NovelAI 生成的图片!")
        return "寄"
    img_comment = json.loads(imginfo["Comment"])
    json_for_i2i["input"] = img_comment["prompt"]
    width = img_comment["width"]
    height = img_comment["height"]
    # 柠檬熟了
    if width == height == 1024:
        json_for_i2i["parameters"]["width"] = int(width * env.magnification)
        json_for_i2i["parameters"]["height"] = int(height * env.magnification)
    else:
        json_for_i2i["parameters"]["width"] = int(width * env.magnification + 32)
        json_for_i2i["parameters"]["height"] = int(height * env.magnification + 32)
    json_for_i2i["parameters"]["scale"] = img_comment["scale"]
    json_for_i2i["parameters"]["sampler"] = img_comment["sampler"]
    json_for_i2i["parameters"]["steps"] = img_comment["steps"]
    json_for_i2i["parameters"]["strength"] = env.hires_strength
    json_for_i2i["parameters"]["sm"] = img_comment["sm"]
    json_for_i2i["parameters"]["sm_dyn"] = img_comment["sm_dyn"]
    json_for_i2i["parameters"]["noise_schedule"] = img_comment["noise_schedule"]
    json_for_i2i["parameters"]["seed"] = img_comment["seed"]
    json_for_i2i["parameters"]["image"] = img_to_base64(imgpath)
    json_for_i2i["parameters"]["extra_noise_seed"] = img_comment["seed"]
    json_for_i2i["parameters"]["negative_prompt"] = img_comment["uc"]

    return json_for_i2i


def upscale_img(json_for_i2i):
    try:
        rep = requests.post('https://image.novelai.net/ai/generate-image', headers=headers, json=json_for_i2i)
        rep.raise_for_status()
        # logger.success("放大成功!")
        with zipfile.ZipFile(io.BytesIO(rep.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()
    except Exception as e:
        logger.error(f"出现错误: {e}")
        return None


imgpath = r"D:\GitClone\Semi-Auto-NovelAI-to-Pixiv\output\140845219_GenshinImpact_纳西妲.png"


info = get_img_info(imgpath)

json_ = prepare_json(info, imgpath)



"""with open("./test.txt", 'w', encoding='utf-8') as file:
    file.write(json.dumps(json_))

with open("./test.txt", 'r', encoding='utf-8') as file:
    data = file.read()"""

imgdata = upscale_img(json_)

save_image(imgdata, "t", "t", "t")