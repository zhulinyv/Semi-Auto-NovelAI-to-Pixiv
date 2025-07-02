import os
import random
import time

import cv2
import ujson as json
from PIL import Image
from playsound import playsound

from utils.env import env
from utils.imgtools import get_concat_h, get_concat_v, get_img_info, img_to_base64, revert_img_info

if "nai-diffusion-4" not in env.model:
    from utils.jsondata import json_for_vibe
else:
    from utils.jsondata import json_for_vibe_v4 as json_for_vibe
from utils.prepare import logger
from utils.utils import (
    file_path2name,
    generate_image,
    position_to_float,
    read_json,
    return_skip_cfg_above_sigma,
    return_x64,
    save_image,
    sleep_for_cool,
)


def vibe_by_hand(
    positive: str,
    negative: str,
    vibe_transfer_width: str,
    vibe_transfer_height: str,
    scale: float,
    rescale: float,
    sampler: str,
    noise_schedule: str,
    steps: int,
    sm: bool,
    sm_dyn: bool,
    variety: bool,
    decrisp: bool,
    seed: str,
    times: int,
    normalize_reference_strength_multiple: bool,
    naiv4vibebundle_file: str,
    *_args,
):
    with open("./output/temp.json", "w") as f:
        json.dump({"break": False}, f)

    imgs_list = []

    if env.model == "nai-diffusion-4-5-curated":
        logger.warning("nai-diffusion-4-5-curated 目前不支持 vibe, 本次 vibe 使用 nai-diffusion-4-full")

    for i in range(times):
        data = read_json("./output/temp.json")
        if data["break"]:
            break

        if times != 1:
            logger.info(f"正在生成第 {i+1} 张图片...")
            sleep_for_cool(env.t2i_cool_time - 3, env.t2i_cool_time + 3)

        json_for_vibe["input"] = positive

        json_for_vibe["parameters"]["width"] = return_x64(int(vibe_transfer_width))
        json_for_vibe["parameters"]["height"] = return_x64(int(vibe_transfer_height))
        json_for_vibe["parameters"]["scale"] = scale
        json_for_vibe["parameters"]["cfg_rescale"] = rescale
        json_for_vibe["parameters"]["sampler"] = sampler
        json_for_vibe["parameters"]["steps"] = steps
        if "nai-diffusion-4" not in env.model:
            json_for_vibe["parameters"]["sm"] = sm if sampler != "ddim_v3" else False
            json_for_vibe["parameters"]["sm_dyn"] = sm_dyn if sm and sampler != "ddim_v3" else False
        json_for_vibe["parameters"]["skip_cfg_above_sigma"] = return_skip_cfg_above_sigma(variety)
        if "nai-diffusion-4" not in env.model:
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

        args = _args[:]
        character_args = args[:25]
        vibe_args = args[25:]

        if "nai-diffusion-4" in env.model:
            json_for_vibe["parameters"]["normalize_reference_strength_multiple"] = normalize_reference_strength_multiple
            json_for_vibe["parameters"]["use_coords"] = not character_args[0]
            json_for_vibe["parameters"]["v4_prompt"]["caption"]["base_caption"] = positive
            json_for_vibe["parameters"]["v4_prompt"]["use_coords"] = not character_args[0]
            json_for_vibe["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = negative

            character_args = character_args[1:]
            components_list = []
            while character_args:
                components_list.append(character_args[0:4])
                character_args = character_args[4:]

            json_for_vibe["parameters"]["characterPrompts"] = [
                {
                    "prompt": components[1],
                    "uc": components[2],
                    "center": {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]},
                    "enabled": True,
                }
                for components in components_list
                if components[0]
            ]

            json_for_vibe["parameters"]["v4_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[1],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]

            json_for_vibe["parameters"]["v4_negative_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[2],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]

        if "nai-diffusion-4" in env.model:
            naiv4vibebundle = read_json(naiv4vibebundle_file)
            for naiv4vibe in naiv4vibebundle["vibes"]:
                if "4-5" in env.model:
                    encoding_key = "v4-5full"
                else:
                    encoding_key = "v4full"
                encoding = naiv4vibe["encodings"][encoding_key][list((naiv4vibe["encodings"][encoding_key]).keys())[0]][
                    "encoding"
                ]
                reference_image_multiple.append(encoding)
                information_extracted = naiv4vibe["importInfo"]["information_extracted"]
                reference_information_extracted_multiple.append(information_extracted)
                strength = naiv4vibe["importInfo"]["strength"]
                reference_strength_multiple.append(strength)
                image = naiv4vibe["id"]
                image_list.append(image)
        else:
            components_list = []
            while vibe_args:
                components_list.append(vibe_args[0:3])
                vibe_args = vibe_args[3:]
            for components in components_list:
                # base64 = read_json("test.json")["parameters"]["reference_image_multiple"][0]
                reference_image_multiple.append(img_to_base64(components[0]))
                # reference_image_multiple.append(base64)
                image_list.append(file_path2name(components[0]))
                # reference_list = img.replace(".jpg", "").replace(".png", "").split("_")
                reference_information_extracted_multiple.append(components[1])
                reference_strength_multiple.append(components[2])

        logger.debug(
            f"""
基底图片: {image_list}
信息提取: {reference_information_extracted_multiple if "nai-diffusion-4" not in env.model else []}
参考强度: {reference_strength_multiple}"""
        )

        json_for_vibe["parameters"]["reference_image_multiple"] = reference_image_multiple
        if "nai-diffusion-4" not in env.model:
            json_for_vibe["parameters"][
                "reference_information_extracted_multiple"
            ] = reference_information_extracted_multiple
        json_for_vibe["parameters"]["reference_strength_multiple"] = reference_strength_multiple

        with open("test.json", "w") as file:
            json.dump(json_for_vibe, file)

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
        if not env.skip_save_grid:
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
        else:
            pass

        if not env.skip_finish_sound:
            playsound("./files/webui/download_finish.mp3")

        if env.skip_save_grid:
            return _imgs_list

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
        return [saved_path]
