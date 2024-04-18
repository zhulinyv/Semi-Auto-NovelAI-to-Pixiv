import base64
from pathlib import WindowsPath

import ujson as json
from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo


def get_img_info(img_path):
    with Image.open(img_path) as img:
        return img.info


def img_to_base64(img_path):
    if isinstance(img_path, str):
        pass
    elif isinstance(img_path, WindowsPath):
        pass
    else:
        img_path.save("./output/temp.png")
        img_path = "./output/temp.png"
    with open(img_path, "rb") as file:
        img_base64 = base64.b64encode(file.read()).decode("utf-8")
    return img_base64


def revert_img_info(img_path, output_dir, *args):
    logger.info("正在还原 pnginfo")
    try:
        if img_path:
            if img_path[-4:] == ".png":
                with Image.open(img_path) as old_img:
                    info = old_img.info
                software = info["Software"]
                comment = info["Comment"]
            elif img_path[-4:] == ".txt":
                with open(img_path) as f:
                    prompt = f.read()
                software = "NovelAI"
                comment = json.dumps({"prompt": prompt})
            else:
                logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
                return
        else:
            software = args[0]["Software"]
            comment = args[0]["Comment"]
        metadata = PngInfo()
        metadata.add_text("Software", software)
        metadata.add_text("Comment", comment)
        with Image.open(output_dir) as new_img:
            new_img.save(output_dir, pnginfo=metadata)
        logger.success("还原成功!")
    except Exception:
        logger.error("还原失败!")
