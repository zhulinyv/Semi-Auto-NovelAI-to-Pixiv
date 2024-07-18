import os
import random
from pathlib import Path

import ujson as json
from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils.imgtools import get_img_info, revert_img_info

# inject_data 修改自 https://github.com/NovelAI/novelai-image-metadata
from utils.naimeta import inject_data
from utils.utils import NOISE_SCHEDULE, RESOLUTION, file_path2list, get_sign


def remove_info(input_path, output_path, choose_to_rm, remove_pnginfo_metadate, data_cloaking_switch):
    metadata = PngInfo()
    if data_cloaking_switch:
        choose_to_rm = []
        metadata.add_text("Title", "AI generated image")
        metadata.add_text("Description", "1girl, loli, cute, artist:ding_zhen")
        metadata.add_text("Software", "NovelAI")
        metadata.add_text("Source", "Stable Diffusion XL C1E1DE52")
        metadata.add_text("Generation time", f"11.4514{random.randint(1000000000, 9999999999)}")
        resolution = (random.choice(RESOLUTION)).split("x")
        sm = random.choice([True, False])
        metadata.add_text(
            "Comment",
            json.dumps(
                {
                    "prompt": "1girl, {loli}, cute, artist:ding_zhen",
                    "steps": random.randint(28, 50),
                    "height": resolution[1],
                    "width": resolution[0],
                    "scale": round(random.uniform(0.1, 9.9), 1),
                    "uncond_scale": 0.0,
                    "cfg_rescale": 0.0,
                    "seed": random.randint(1000000000, 9999999999),
                    "n_samples": 1,
                    "hide_debug_overlay": False,
                    "noise_schedule": random.choice(NOISE_SCHEDULE),
                    "legacy_v3_extend": False,
                    "reference_information_extracted_multiple": [],
                    "reference_strength_multiple": [],
                    "sampler": "k_euler",
                    "controlnet_strength": 1.0,
                    "controlnet_model": None,
                    "dynamic_thresholding": False,
                    "dynamic_thresholding_percentile": 0.999,
                    "dynamic_thresholding_mimic_scale": 10.0,
                    "sm": sm,
                    "sm_dyn": random.choice([True, False]) if sm else False,
                    "skip_cfg_below_sigma": 0.0,
                    "lora_unet_weights": None,
                    "lora_clip_weights": None,
                    "uc": "nsfw, lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]",
                    "request_type": "PromptGenerateRequest",
                    "signed_hash": get_sign(
                        "1girl,{},cute,[artist:ding_zhen],{}".format("{loli}", remove_pnginfo_metadate),
                        "abcdefghijklmnopqrstuvwxyz1234567890",
                    ),
                }
            ),
        )
    else:
        metadata.add_text("None", remove_pnginfo_metadate)

    file_list = file_path2list(input_path)
    for file in file_list:
        logger.warning(f"正在清除 {file} 的元数据...")
        with Image.open(Path(input_path) / file) as img:
            img = inject_data(img, metadata, choose_to_rm)
            img.save(Path(output_path) / file)
        logger.success("清除成功!")
    return f"清除成功! 图片已保存到 {output_path}"


def revert_info(info_file_path, input_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        if os.path.exists(Path(info_file_path) / f"{file[:-4]}.txt"):
            revert_img_info(str(Path(info_file_path) / f"{file[:-4]}.txt"), Path(input_path) / file)
        elif os.path.exists(Path(info_file_path) / f"{file[:-4]}.png"):
            revert_img_info(str(Path(info_file_path) / f"{file[:-4]}.png"), Path(input_path) / file)
        else:
            logger.error("仅支持从 *.png 和 *.txt 文件中读取元数据!")
    return f"还原成功! 图片已保存到 {input_path}"


def export_info(input_path, output_path):
    file_list = file_path2list(input_path)
    for file in file_list:
        logger.info(f"正在导出: {file}...")
        info = get_img_info(f"{input_path}/{file}")
        prompt = json.loads(info["Comment"])["prompt"]
        file = file.replace(".png", ".txt")
        with open(f"{output_path}/{file}", "w", encoding="utf-8") as f:
            f.write(prompt)
        logger.success("导出成功!")
    return f"导出成功! 文件已保存到 {output_path}"
