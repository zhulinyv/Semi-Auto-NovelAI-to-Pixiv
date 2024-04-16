import os
import random
from pathlib import Path

import ujson as json
from loguru import logger

from utils.env import env
from utils.error import UploadError, UploadTooFastError, WrongImgError
from utils.imgtools import get_img_info
from utils.pixivposter import pixiv_upload

# pixivposter 直接抄自[小苹果](https://github.com/LittleApple-fp16)
from utils.utils import sleep_for_cool


def upload(image_list, file):
    image_info = get_img_info(image_list[-1])
    try:
        image_info["Software"] == "NovelAI"
        img_comment = json.loads(image_info["Comment"])
        caption = env.caption_prefix + "\n----------\n" + img_comment["prompt"]
        pass
    except WrongImgError:
        logger.error("不是 NovelAI 生成的图片!")
        caption = env.caption_prefix

    with open("./files/favorite.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    name_list = file.replace(".png", "").split("_")
    name = name_list[2]
    surrounding_title_list = list(data["title"]["surrounding"].keys())
    action_title_list = list(data["title"]["action"].keys())
    for k in surrounding_title_list:
        if k in caption:
            surrounding_title = random.choice(data["title"]["surrounding"][k])
            break
    for v in action_title_list:
        if v in caption:
            action_title = random.choice(data["title"]["action"][v])
            break
    if name == "None":
        title = "无题"
    else:
        try:
            action_title
            title = f"{name}{action_title}~"
        except NameError:
            try:
                surrounding_title
                title = f"和{name}在{surrounding_title}~"
            except NameError:
                title = f"{name}涩涩~"

    labels_list = ["女の子"]
    try:
        character_labels_list = list(data["labels"][name_list[1]].keys())
    except Exception:
        character_labels_list = []
    description_labels_list = list(data["labels"]["description"].keys())
    for i in character_labels_list:
        for j in data["labels"][name_list[1]][i]:
            labels_list.append(j) if i in caption else ...
    for m in description_labels_list:
        for n in data["labels"]["description"][m]:
            labels_list.append(n) if m in caption else ...
    while len(labels_list) > 10:
        del labels_list[-1]

    logger.info(
        f"""
图片: {image_list}
标题: {title}
描述: {caption}
标签: {labels_list}
"""
    )

    status = pixiv_upload(image_list, title, caption, labels_list, env.pixiv_cookie, env.pixiv_token, True, True)
    return status


def main(file_path):
    file_list = os.listdir(file_path)

    for file in file_list:
        times = 0
        while times <= 5:
            try:
                times += 1
                image_list = []
                if file[-4:] == ".png":
                    # image_list.append(f"{file_path}/{file}")
                    image_list.append(Path(file_path) / file)
                    file = file
                else:
                    # folder_path = f"{file_path}/{file}"
                    folder_path = Path(file_path) / file
                    folder_list = os.listdir(folder_path)
                    # for i in folder_list: image_list.append(f"{folder_path}/{i}")
                    for i in folder_list:
                        image_list.append(folder_path / i)
                    file = folder_list[-1]
                status = upload(image_list, file)
                if status == 1:
                    raise UploadError
                elif status == 2:
                    sleep_for_cool(600, 1200)
                    raise UploadTooFastError
                else:
                    break
            except Exception:
                pass
        sleep_for_cool(600, 1200)
    logger.success("上传完成!")

    return "上传完成!"


if __name__ == "__main__":
    main("./output/pixiv")
