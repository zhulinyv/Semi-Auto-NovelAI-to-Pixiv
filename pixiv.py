import os

import ujson as json

from loguru import logger

from utils.env import env
from utils.error import UploadError, UploadTooFastError
from utils.imgtools import get_img_info
from utils.pixivposter import *
# pixivposter 直接抄自[小苹果](https://github.com/LittleApple-fp16)
from utils.utils import sleep_for_cool


file_path = "./output/pixiv/"
file_list = os.listdir(file_path)



def upload(image_list, file):
    image_info = get_img_info(image_list[-1])
    if image_info["Software"] != "NovelAI":
        logger.error("不是 NovelAI 生成的图片!")
        return
    img_comment = json.loads(image_info["Comment"])
    caption = img_comment["prompt"]
    
    name_list = file.replace(".png", '').split("_")
    title = name_list[2]
    
    with open("./files/favorite.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    labels_list = ['女の子']
    character_labels_list = list(data["labels"][name_list[1]].keys())
    description_labels_list = list(data["labels"]["description"].keys())
    for i in character_labels_list:
        for j in data["labels"][name_list[1]][i]: labels_list.append(j) if i in caption else ...
    for m in description_labels_list:
        for n in data["labels"]["description"][m]: labels_list.append(n) if m in caption else ...
    while len(labels_list) > 10:
        del labels_list[-1]
    
    logger.info(f"""
图片: {image_list}
标题: {title}
描述: {caption}
标签: {labels_list}
""")
    
    status = pixiv_upload(image_list, title, caption, labels_list, env.pixiv_cookie, env.pixiv_token, True, True)
    return status



for file in file_list:
    times = 1
    while times <= 5:
        try:
            image_list = []
            if file[-4:] == '.png':
                image_list.append(file_path + file)
                file = file
            else:
                folder_path = file_path + file
                folder_list = os.listdir(folder_path)
                for i in folder_list: image_list.append(f"{folder_path}/{i}")
                file = folder_list[-1]
            status = upload(image_list, file)
            if status == 1:
                times += 1
                raise UploadError
            elif status == 2:
                sleep_for_cool(600, 1200)
                raise UploadTooFastError
            else:
                break
        except:
            pass
    sleep_for_cool(600, 1200)