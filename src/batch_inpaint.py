from loguru import logger

from src.image2image import prepare_json
from utils.imgtools import get_img_info, img_to_base64, revert_img_info
from utils.utils import file_namel2pathl, file_path2list, file_path2name, generate_image, inquire_anlas, save_image


def for_webui(input_path, mask_path, input_img, input_mask, open_button):
    if open_button:
        main(input_path, mask_path)
        return None, "处理完成, 图片已保存到 ./output/inpaint..."
    else:
        input_img.save("./output/temp_inpaint_img.png")
        input_mask.save("./output/temp_inpaint_mask.png")
        revert_img_info(None, "./output/temp_inpaint_img.png", input_img.info)
        path = inpaint("./output/temp_inpaint_img.png", "./output/temp_inpaint_mask.png")
    return path, f"剩余水晶: {inquire_anlas()}"


def inpaint(img_path, mask_path):
    imginfo = get_img_info(img_path)
    json_for_inpaint = prepare_json(imginfo, img_path)
    json_for_inpaint["parameters"]["mask"] = img_to_base64(mask_path)
    json_for_inpaint["model"] = "nai-diffusion-3-inpainting"
    json_for_inpaint["action"] = "infill"

    img_name = file_path2name(img_path)

    saved_path = save_image(generate_image(json_for_inpaint), "inpaint", None, None, None, img_name)

    return saved_path


def main(img_folder, mask_folder):
    file_list = file_namel2pathl(file_path2list(img_folder), img_folder)

    for file in file_list:
        logger.info(f"正在处理: {file}")
        inpaint(file, f"{mask_folder}/{file_path2name(file)}")
