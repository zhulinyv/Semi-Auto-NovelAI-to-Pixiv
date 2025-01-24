import os
import random
import time

import cv2
from PIL import Image
from playsound import playsound

from utils.env import env
from utils.imgtools import get_concat_h, get_concat_v, get_img_info, img_to_base64, revert_img_info
from utils.jsondata import json_for_vibe
from utils.prepare import logger
from utils.utils import file_path2name, generate_image, return_x64, save_image, sleep_for_cool


def vibe_by_hand(
    positive: str,
    negative: str,
    vibe_transfer_width: str,
    vibe_transfer_height: str,
    scale: float,
    sampler: str,
    noise_schedule: str,
    steps: int,
    sm: bool,
    sm_dyn: bool,
    variety: bool,
    decrisp: bool,
    seed: str,
    times: int,
    *args,
):
    imgs_list = []
    for i in range(times):
        if times != 1:
            logger.info(f"正在生成第 {i+1} 张图片...")
            sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

        json_for_vibe["input"] = positive

        json_for_vibe["parameters"]["width"] = return_x64(int(vibe_transfer_width))
        json_for_vibe["parameters"]["height"] = return_x64(int(vibe_transfer_height))
        json_for_vibe["parameters"]["scale"] = scale
        json_for_vibe["parameters"]["sampler"] = sampler
        json_for_vibe["parameters"]["steps"] = steps
        json_for_vibe["parameters"]["sm"] = sm if sampler != "ddim_v3" else False
        json_for_vibe["parameters"]["sm_dyn"] = sm_dyn if sm and sampler != "ddim_v3" else False
        json_for_vibe["parameters"]["skip_cfg_above_sigma"] = 19 if variety else None
        json_for_vibe["parameters"]["dynamic_thresholding"] = decrisp
        if sampler != "ddim_v3":
            json_for_vibe["parameters"]["noise_schedule"] = noise_schedule
        if isinstance(seed, int):
            seed = random.randint(1000000000, 9999999999)
        else:
            seed = random.randint(1000000000, 9999999999) if seed == "-1" else int(seed)
        json_for_vibe["parameters"]["seed"] = seed
        json_for_vibe["parameters"]["negative_prompt"] = negative

        json_for_vibe["parameters"]["add_original_image"] = True

        reference_image_multiple = []
        reference_information_extracted_multiple = []
        reference_strength_multiple = []
        image_list = []

        components_list = []
        while args:
            components_list.append(args[0:3])
            args = args[3:]

        for components in components_list:
            reference_image_multiple.append(img_to_base64(components[0]))
            image_list.append(file_path2name(components[0]))
            # reference_list = img.replace(".jpg", "").replace(".png", "").split("_")
            reference_information_extracted_multiple.append(components[1])
            reference_strength_multiple.append(components[2])

        logger.debug(
            f"""
基底图片: {image_list}
信息提取: {reference_information_extracted_multiple}
参考强度: {reference_strength_multiple}"""
        )

        json_for_vibe["parameters"]["reference_image_multiple"] = reference_image_multiple
        json_for_vibe["parameters"][
            "reference_information_extracted_multiple"
        ] = reference_information_extracted_multiple
        json_for_vibe["parameters"]["reference_strength_multiple"] = reference_strength_multiple

        saved_path = save_image(generate_image(json_for_vibe), "vibe", seed, "None", "None")

        if saved_path != "寄":
            imgs_list.append(saved_path)
        else:
            pass
        _imgs_list = imgs_list[:]

    for img in imgs_list:
        if not os.path.exists(img):
            imgs_list.remove(img)

    if times != 1:
        num_list = []
        for row in range(3 if len(imgs_list) == 2 else len(imgs_list)):
            for column in range(3 if len(imgs_list) == 2 else len(imgs_list)):
                if row * column >= len(imgs_list):
                    num_list.append([row, column])
        row, column = num_list[0]
        for num in num_list[1:]:
            if abs(num[0] - num[1]) < abs(row - column):
                row, column = num

        imgs_list_list = [imgs_list[i : i + column] for i in range(0, len(imgs_list), column)]

        merged_imgs = []
        for imgs_list in imgs_list_list:
            for img in imgs_list:
                if img == imgs_list[0]:
                    merged_img = Image.open(img)
                else:
                    merged_img = get_concat_h(merged_img, Image.open(img))
            merged_imgs.append(merged_img)
        for img in merged_imgs:
            if img == merged_imgs[0]:
                merged_img = img
            else:
                merged_img = get_concat_v(merged_img, img)

        time_ = int(time.time())
        merged_img.save("./output/vibe/grids/{}.png".format(time_))
        merged_img.close()

        if not env.skip_finish_sound:
            playsound("./files/webui/download_finish.mp3")

        if times <= 10:
            revert_img_info(imgs_list[0], "./output/vibe/grids/{}.png".format(time_))
            return ["./output/vibe/grids/{}.png".format(time_)] + _imgs_list
        # except Image.DecompressionBombError:
        else:
            logger.warning("图片过大, 进行压缩...")
            cv2.imwrite(
                "./output/vibe/grids/{}.jpg".format(time_),
                cv2.imread("./output/vibe/grids/{}.png".format(time_)),
                [cv2.IMWRITE_JPEG_QUALITY, 90],
            )
            with open("./output/vibe/grids/{}.txt".format(time_), "w") as infofile:
                infofile.write(get_img_info(imgs_list[0])["Description"])
            logger.success("压缩完成!")
            return ["./output/vibe/grids/{}.jpg".format(time_)] + _imgs_list
    else:
        return saved_path
