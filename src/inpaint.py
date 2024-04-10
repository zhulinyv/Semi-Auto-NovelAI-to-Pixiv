import os
import random
import string

from loguru import logger
from PIL.PngImagePlugin import PngInfo

from src.i2i import prepare_json
from utils.error import DataIsNoneError
from utils.imgtools import get_img_info, img_to_base64
from utils.utils import format_path, generate_image, inquire_anlas


def for_webui(input_path, mask_path, input_img, input_mask, open_button):
    if open_button:
        main(input_path, mask_path, "./output/inpaint")
        return None, "处理完成, 图片已保存到 ./output/inpaint..."
    else:
        logger.warning(f"剩余水晶: {inquire_anlas()}")
        info = input_img.info
        metadata = PngInfo()
        metadata.add_text("Software", info["Software"])
        metadata.add_text("Comment", info["Comment"])
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        input_img.save(f"./output/inpaint_img_{random_string}.png", pnginfo=metadata)
        input_mask.save("./output/temp_inpaint_mask.png")
        inpaint(f"./output/inpaint_img_{random_string}.png", "./output/temp_inpaint_mask.png", "./output/inpaint")
    return f"./output/inpaint/inpaint_img_{random_string}.png", None


def inpaint(img_path, mask_path, output_path):
    imginfo = get_img_info(img_path)
    json_for_inpaint = prepare_json(imginfo, img_path)
    json_for_inpaint["parameters"]["mask"] = img_to_base64(mask_path)
    img_data = generate_image(json_for_inpaint)
    if not img_data:
        raise DataIsNoneError
    img_name = os.path.basename(img_path)
    with open(f"{format_path(output_path)}/{img_name}", "wb") as file:
        file.write(img_data)
    return f"{format_path(output_path)}/{img_name}"


def main(img_folder, mask_folder, otp_folder):
    file_list = os.listdir(img_folder)
    empty_list = []
    for file in file_list:
        empty_list.append(f"{img_folder}/{file}")
    file_list = empty_list

    for i in range(len(file_list)):
        logger.warning(f"剩余水晶: {inquire_anlas()}")
        inpaint(file_list[i], f"{mask_folder}/{os.path.basename(file_list[i])}", otp_folder)


if __name__ == "__main__":
    main("./output/inpaint/img", "./output/inpaint/mask", "./output/inpaint")
