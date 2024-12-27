import os
import random
import shutil
import traceback
import uuid
from pathlib import Path

import requests
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.env import env
from utils.error import UploadError, UploadTooFastError
from utils.imgtools import get_img_info

# inject_data 修改自 https://github.com/NovelAI/novelai-image-metadata
from utils.naimeta import inject_data
from utils.pixivposter import headers, pixiv_upload
from utils.prepare import logger

# pixivposter 直接抄自[小苹果](https://github.com/LittleApple-fp16)
from utils.utils import (
    cancel_probabilities_for_item,
    file_path2list,
    file_path2name,
    format_str,
    list_to_str,
    read_yaml,
    sleep_for_cool,
)


def upload(image_list, file):
    image_info = get_img_info(image_list[-1])

    try:
        image_info["Software"] == "NovelAI"
        img_comment = image_info["Comment"]
        prompt: str = img_comment["prompt"]
        if env.rep_tags_per == 1:
            caption = env.caption_prefix
        else:
            if env.rep_tags:
                prompt = "".join(i for i in prompt if i not in ["[", "]", "{", "}"])
                prompt = format_str(prompt)
                prompt = prompt.split(", ")
                prompt = random.sample(prompt, int((num := len(prompt)) * env.rep_tags_per))
                prompt = list_to_str(prompt)
                prompt = format_str(prompt)
                prompt += f", {env.rep_tags_with_tag}" * int(num * (1 - env.rep_tags_per))
            caption = env.caption_prefix + "\n----------\n" + prompt

        if env.remove_info:
            for image in image_list:
                metadata = PngInfo()
                metadata.add_text("None", env.meta_data)
                logger.warning(f"正在清除 {image} 的元数据...")
                with Image.open(image) as img:
                    img = inject_data(
                        img,
                        metadata,
                        ["Title", "Description ", "Software", "Source", "Generation time", "Comment", "parameters"],
                    )
                    img.save(image)
                logger.success("清除成功!")

    except KeyError:
        logger.error("不是 NovelAI 生成的图片!")
        caption = env.caption_prefix
        img_comment = {"prompt": ""}
    except TypeError:
        logger.error("未包含 NovelAI 生成信息!")
        caption = env.caption_prefix
        img_comment = {"prompt": ""}

    # 标题
    characters_data = cancel_probabilities_for_item(read_yaml("./files/favorites/characters.yaml"))
    surroundings_data = cancel_probabilities_for_item(read_yaml("./files/favorites/surroundings.yaml"))

    if env.use_file_name_as_title:
        name = file_path2name(image).split(".")[0]
    elif env.use_old_title_rule:
        name = (file_path2name(image).split("_")[2]).split(".")[0]
    else:
        for k, v in characters_data.items():
            if (format_str(v["tag"]) in img_comment["prompt"]) or (v["tag"] in img_comment["prompt"]):
                name = k
                break
            else:
                name = "None"

    if name == "None":
        name == "无题"
        new_name = name
    else:
        if env.r18:
            for k, v in surroundings_data.items():
                if (format_str(v["tag"]) in img_comment["prompt"]) or (v["tag"] in img_comment["prompt"]):
                    new_name = random.choice([f"{name}~", f"和{name}涩涩~", f"和{name}在{k}~"])
                    break
            try:
                new_name
            except Exception:
                new_name = random.choice([f"{name}~", f"和{name}涩涩~"])
        else:
            new_name = f"{name}~"

    file = image_list[-1]

    # 标签
    if env.suggest_tag:
        if str(file)[-4:] == ".png":
            format_ = "image/png"
        else:
            format_ = "image/jpeg"

        with open(file, "rb") as image:
            image_data = image.read()

        files = {"image": (file_path2name(file), image_data, format_)}

        headers["sentry-trace"] = f'{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-"0"'
        response = requests.post("https://www.pixiv.net/rpc/suggest_tags_by_image.php", files=files, headers=headers)

        if response.status_code == 200:
            suggest_tags = response.json()["body"]["tags"]
        else:
            suggest_tags = []
    else:
        suggest_tags = []

    labels = env.default_tag + suggest_tags

    while length := len(labels) > 10:
        labels.pop(random.randint(0, length - 1))

    # 预览
    logger.info(
        f"""
图片: {image_list}
标题: {new_name}
标签: {labels}
描述: {caption}"""
    )

    # 状态
    times = 0
    while times <= 5:
        try:
            times += 1
            status = pixiv_upload(
                image_paths=image_list,
                title=new_name,
                caption=caption,
                labels=labels,
                allow_tag_edit=env.allow_tag_edit,
                is_r18=env.r18,
            )
            if status == 1:
                raise UploadError
            elif status == 2:
                raise UploadTooFastError
            else:
                pass
            break
        except Exception:
            logger.error("出现错误: >>>>>")
            traceback.print_exc()
            logger.error("<<<<<")
            sleep_for_cool(300, 600)
    return status


def main(file_path):
    file_list = file_path2list(file_path)
    for file in file_list:
        image_list = []
        if file[-4:] == ".png":
            image_list.append(Path(file_path) / file)
            file = file
        else:
            folder_path = Path(file_path) / file
            folder_list = file_path2list(folder_path)
            for i in folder_list:
                image_list.append(folder_path / i)
            file = folder_list[-1]
        status = upload(image_list, file)
        if status not in [1, 2]:
            logger.warning(f"删除 {Path(file_path) / file}...")
        try:
            shutil.rmtree(Path(file_path) / file)
        except NotADirectoryError:
            os.remove(Path(file_path) / file)
        sleep_for_cool((env.pixiv_cool_time - 5) * 60, (env.pixiv_cool_time + 5) * 60)
    logger.success("上传完成!")

    return "上传完成!"
