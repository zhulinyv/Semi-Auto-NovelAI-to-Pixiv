import random

from src.image2image import prepare_json
from utils.env import env
from utils.imgtools import change_the_mask_color, get_img_info, img_to_base64
from utils.prepare import logger
from utils.utils import (
    file_namel2pathl,
    file_path2list,
    file_path2name,
    generate_image,
    position_to_float,
    return_skip_cfg_above_sigma,
    return_x64,
    save_image,
)

if "nai-diffusion-4" in env.model:
    from utils.jsondata import json_for_inpaint_v4 as json_for_inpaint
else:
    from utils.jsondata import json_for_inpaint


def for_webui(
    input_path,
    mask_path,
    inpaint_input_image,
    inpaint_overlay,
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
    inpaint_rescale,
    inpaint_steps,
    inpaint_sm,
    inpaint_sm_dyn,
    inpaint_variety,
    inpaint_decrisp,
    inpaint_seed,
    *args,
):
    if open_button:
        main(input_path, mask_path, inpaint_overlay)
        return None, "处理完成! 图片已保存到 ./output/inpaint..."
    else:
        (inpaint_input_image["background"]).save("./output/temp_inpaint_img.png")
        (inpaint_input_image["layers"][0]).save("./output/temp_inpaint_mask.png")
        change_the_mask_color("./output/temp_inpaint_mask.png")

        json_for_inpaint["input"] = inpaint_positive_input
        json_for_inpaint["parameters"]["add_original_image"] = inpaint_overlay
        json_for_inpaint["parameters"]["negative_prompt"] = inpaint_negative_input
        json_for_inpaint["parameters"]["width"] = return_x64(int(inpaint_width))
        json_for_inpaint["parameters"]["height"] = return_x64(int(inpaint_height))
        json_for_inpaint["parameters"]["sampler"] = inpaint_sampler
        if inpaint_sampler != "ddim_v3":
            json_for_inpaint["parameters"]["noise_schedule"] = inpaint_noise_schedule
        json_for_inpaint["parameters"]["strength"] = inpaint_strength
        json_for_inpaint["parameters"]["noise"] = inpaint_noise
        json_for_inpaint["parameters"]["scale"] = inpaint_scale
        json_for_inpaint["parameters"]["cfg_rescale"] = inpaint_rescale
        json_for_inpaint["parameters"]["steps"] = inpaint_steps
        if "nai-diffusion-4" not in env.model:
            json_for_inpaint["parameters"]["sm"] = False
            json_for_inpaint["parameters"]["sm_dyn"] = False
        json_for_inpaint["parameters"]["skip_cfg_above_sigma"] = return_skip_cfg_above_sigma(inpaint_variety)
        json_for_inpaint["parameters"]["dynamic_thresholding"] = inpaint_decrisp
        seed = random.randint(1000000000, 9999999999) if inpaint_seed == "-1" else int(inpaint_seed)
        json_for_inpaint["parameters"]["seed"] = seed
        json_for_inpaint["parameters"]["extra_noise_seed"] = seed

        json_for_inpaint["parameters"]["image"] = img_to_base64("./output/temp_inpaint_img.png")
        json_for_inpaint["parameters"]["mask"] = img_to_base64("./output/temp_inpaint_mask.png")

        if "nai-diffusion-4" in env.model:
            json_for_inpaint["parameters"]["use_coords"] = not args[0]
            json_for_inpaint["parameters"]["v4_prompt"]["caption"]["base_caption"] = inpaint_positive_input
            json_for_inpaint["parameters"]["v4_prompt"]["use_coords"] = not args[0]
            json_for_inpaint["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = inpaint_negative_input

            args = args[1:]
            components_list = []
            while args:
                components_list.append(args[0:4])
                args = args[4:]

            json_for_inpaint["parameters"]["characterPrompts"] = [
                {
                    "prompt": components[1],
                    "uc": components[2],
                    "center": {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]},
                    "enabled": True,
                }
                for components in components_list
                if components[0]
            ]

            json_for_inpaint["parameters"]["v4_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[1],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]

            json_for_inpaint["parameters"]["v4_negative_prompt"]["caption"]["char_captions"] = [
                {
                    "char_caption": components[2],
                    "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
                }
                for components in components_list
                if components[0]
            ]
        # with open("test.1.json", "w") as file:
        #     json.dump(json_for_inpaint, file)
        saved_path = save_image(generate_image(json_for_inpaint), "inpaint", seed, "None", "None")

    return saved_path, None


def inpaint(img_path, mask_path, inpaint_overlay, *args, **kwargs):
    imginfo = get_img_info(img_path)
    json_for_inpaint = prepare_json(imginfo, img_path)
    json_for_inpaint["parameters"]["mask"] = img_to_base64(mask_path)
    if env.model == "nai-diffusion-4-curated-preview":
        model = "nai-diffusion-4-curated-inpainting"
    elif env.model == "nai-diffusion-4-full":
        model = "nai-diffusion-4-full-inpainting"
    else:
        model = f"{env.model}-inpainting" if env.model != "nai-diffusion-2" else "nai-diffusion-3-inpainting"
    json_for_inpaint["model"] = model
    json_for_inpaint["action"] = "infill"
    json_for_inpaint["add_original_image"] = inpaint_overlay
    json_for_inpaint["strength"] = kwargs["inpaint_strength"]
    json_for_inpaint["noise"] = kwargs["inpaint_noise"]

    if "nai-diffusion-4" in env.model:
        json_for_inpaint["parameters"]["use_coords"] = args[0]
        json_for_inpaint["parameters"]["v4_prompt"]["caption"]["base_caption"] = json_for_inpaint["input"]
        json_for_inpaint["parameters"]["v4_prompt"]["use_coords"] = args[0]
        json_for_inpaint["parameters"]["v4_negative_prompt"]["caption"]["base_caption"] = json_for_inpaint[
            "parameters"
        ]["negative_prompt"]

        args = args[1:]
        components_list = []
        while args:
            components_list.append(args[0:4])
            args = args[4:]

        json_for_inpaint["parameters"]["characterPrompts"] = [
            {
                "prompt": components[1],
                "uc": components[2],
                "center": {"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]},
            }
            for components in components_list
            if components[0]
        ]

        json_for_inpaint["parameters"]["v4_prompt"]["caption"]["char_captions"] = [
            {
                "char_caption": components[1],
                "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
            }
            for components in components_list
            if components[0]
        ]

        json_for_inpaint["parameters"]["v4_negative_prompt"]["caption"]["char_captions"] = [
            {
                "char_caption": components[2],
                "centers": [{"x": position_to_float(components[3])[0], "y": position_to_float(components[3])[1]}],
            }
            for components in components_list
            if components[0]
        ]

    saved_path = save_image(generate_image(json_for_inpaint), "inpaint", (imginfo["Comment"])["seed"], "None", "None")

    return saved_path


def main(img_folder, mask_folder, inpaint_overlay):
    file_list = file_namel2pathl(file_path2list(img_folder), img_folder)

    for file in file_list:
        logger.info(f"正在处理: {file}")
        inpaint(file, f"{mask_folder}/{file_path2name(file)}", inpaint_overlay)
