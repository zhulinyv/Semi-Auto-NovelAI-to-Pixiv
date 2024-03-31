import base64

from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo



def get_img_info(img_path):
    img = Image.open(img_path)
    return img.info

def img_to_base64(img_path):
    if isinstance(img_path, str):
        pass
    else:
        img_path.save("./output/temp.png")
        img_path = "./output/temp.png"
    with open(img_path, 'rb') as file:
        img_base64 = base64.b64encode(file.read()).decode('utf-8')
    return img_base64

def revert_img_info(img_path, output_dir):
    logger.info("正在还原 pnginfo")
    old_img = Image.open(img_path)
    info = old_img.info
    metadata = PngInfo()
    try:
        metadata.add_text("Software", info["Software"])
        metadata.add_text("Comment", info["Comment"])
    except:
        logger.error("还原失败!")
        return
    new_img = Image.open(output_dir)
    new_img.save(output_dir, pnginfo=metadata)
    logger.success("还原成功!")