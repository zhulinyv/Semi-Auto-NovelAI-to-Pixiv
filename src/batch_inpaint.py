import random

import ujson as json

from src.image2image import prepare_json
from utils.imgtools import change_the_mask_color_to_white, get_img_info, img_to_base64, revert_img_info
from utils.prepare import logger
from utils.utils import file_namel2pathl, file_path2list, file_path2name, generate_image, return_x64, save_image


def for_webui(
    input_path,
    mask_path,
    inpaint_input_image,
    open_button,
    inpaint_positive_input,
    inpaint_negative_input,
    inpaint_width,
    inpaint_height,
    inpaint_sampler,
    inpaint_noise_schedule,
    inpaint_strength,
    inpaint_noise,
    inpaint_scale,
    inpaint_steps,
    inpaint_sm,
    inpaint_sm_dyn,
    inpaint_seed,
):
    if open_button:
        main(input_path, mask_path)
        return None, "处理完成, 图片已保存到 ./output/inpaint..."
    else:
        (inpaint_input_image["background"]).save("./output/temp_inpaint_img.png")
        (inpaint_input_image["layers"][0]).save("./output/temp_inpaint_mask.png")
        change_the_mask_color_to_white("./output/temp_inpaint_mask.png")

        info = {
            "Software": "NovelAI",
            "Comment": json.dumps(
                {
                    "prompt": inpaint_positive_input,
                    "steps": inpaint_steps,
                    "height": return_x64(int(inpaint_height)),
                    "width": return_x64(int(inpaint_width)),
                    "scale": inpaint_scale,
                    "seed": random.randint(1000000000, 9999999999) if inpaint_seed == "-1" else int(inpaint_seed),
                    "noise_schedule": inpaint_noise_schedule,
                    "sampler": inpaint_sampler,
                    "sm": inpaint_sm,
                    "sm_dyn": inpaint_sm_dyn,
                    "uc": inpaint_negative_input,
                }
            ),
        }

        revert_img_info(None, "./output/temp_inpaint_img.png", info)

        logger.info("开始重绘...")
        path = inpaint(
            "./output/temp_inpaint_img.png", "./output/temp_inpaint_mask.png", inpaint_strength, inpaint_noise
        )
    return path, None


def inpaint(img_path, mask_path, *args):
    imginfo = get_img_info(img_path)
    json_for_inpaint = prepare_json(imginfo, img_path)
    json_for_inpaint["parameters"]["mask"] = img_to_base64(mask_path)
    json_for_inpaint["model"] = "nai-diffusion-3-inpainting"
    json_for_inpaint["action"] = "infill"
    if args:
        json_for_inpaint["strength"] = args[0]
        json_for_inpaint["noise"] = args[1]

    saved_path = save_image(generate_image(json_for_inpaint), "inpaint", (imginfo["Comment"])["seed"], "None", "None")

    return saved_path


def main(img_folder, mask_folder):
    file_list = file_namel2pathl(file_path2list(img_folder), img_folder)

    for file in file_list:
        logger.info(f"正在处理: {file}")
        inpaint(file, f"{mask_folder}/{file_path2name(file)}")
