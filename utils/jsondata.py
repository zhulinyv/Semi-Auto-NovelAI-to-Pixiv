from utils.env import env
from utils.prepare import logger

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
    "Authorization": f'Bearer {env.token if env.token != "xxx" else logger.error("未配置 token!")}',
    "Referer": "https://novelai.net",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    "Sec-Ch-Ua-mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}


json_for_t2i = {
    "input": str,
    "model": env.model,
    "action": "generate",
    "parameters": {
        "params_version": 3,
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "ucPreset": 0,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": bool,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": False,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        # "noise_schedule": str,
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": None,
        "seed": int,
        "negative_prompt": str,
        "reference_image_multiple": [],
        "reference_information_extracted_multiple": [],
        "reference_strength_multiple": [],
    },
}


json_for_i2i = {
    "input": str,
    "model": env.model,
    "action": "img2img",
    "parameters": {
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "strength": float,
        "noise": float,
        "ucPreset": 0,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": bool,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": False,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        # "noise_schedule": str,
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": None,
        "params_version": 3,
        "seed": int,
        "image": str,
        "extra_noise_seed": int,
        "negative_prompt": str,
        "reference_image_multiple": [],
        "reference_information_extracted_multiple": [],
        "reference_strength_multiple": [],
    },
}


json_for_inpaint = {
    "input": str,
    "model": "nai-diffusion-3-inpainting",
    "action": "infill",
    "parameters": {
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "strength": float,
        "noise": float,
        "ucPreset": 0,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": bool,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": bool,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        # "noise_schedule": str,
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": None,
        "params_version": 3,
        "seed": int,
        "image": str,
        "mask": str,
        "extra_noise_seed": int,
        "negative_prompt": str,
        "reference_image_multiple": [],
        "reference_information_extracted_multiple": [],
        "reference_strength_multiple": [],
    },
}


json_for_vibe = {
    "input": str,
    "model": env.model,
    "action": "generate",
    "parameters": {
        "params_version": 3,
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "ucPreset": 0,
        "qualityToggle": True,
        "sm": bool,
        "sm_dyn": bool,
        "dynamic_thresholding": bool,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": False,
        "uncond_scale": 1,
        "cfg_rescale": 0,
        # "noise_schedule": str,
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": None,
        "seed": int,
        "negative_prompt": str,
        "reference_image_multiple": list,
        "reference_information_extracted_multiple": list,
        "reference_strength_multiple": list,
    },
}


json_for_remove_bg = {
    "req_type": "bg-removal",
    "width": int,
    "height": int,
    "image": str,
}


json_for_lineart = {
    "req_type": "lineart",
    "width": int,
    "height": int,
    "image": str,
}

json_for_sketch = {
    "req_type": "sketch",
    "width": int,
    "height": int,
    "image": str,
}

json_for_declutter = {
    "req_type": "declutter",
    "width": int,
    "height": int,
    "image": str,
}

json_for_colorize = {
    "req_type": "colorize",
    "prompt": str,
    "defry": int,
    "width": int,
    "height": int,
    "image": str,
}

json_for_emotion = {
    "req_type": "emotion",
    "prompt": str,
    "defry": int,
    "width": int,
    "height": int,
    "image": str,
}


json_for_t2i_v4 = {
    "input": str,
    "model": "nai-diffusion-4-curated-preview",
    "action": "generate",
    "parameters": {
        "params_version": 3,
        "width": int,
        "height": int,
        "scale": float,
        "sampler": str,
        "steps": int,
        "n_samples": 1,
        "ucPreset": 0,
        "qualityToggle": True,
        "dynamic_thresholding": bool,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": False,
        "cfg_rescale": 0,
        "noise_schedule": str,
        "legacy_v3_extend": False,
        "seed": int,
        "use_coords": bool,
        "characterPrompts": [
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
            # {"prompt": str, "uc": str, "center": {"x": float, "y": float}},
        ],
        "v4_prompt": {
            "caption": {
                "base_caption": str,
                "char_captions": [
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                ],
            },
            "use_coords": bool,
            "use_order": True,
        },
        "v4_negative_prompt": {
            "caption": {
                "base_caption": str,
                "char_captions": [
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                    # {"char_caption": str, "centers": [{"x": float, "y": float}]},
                ],
            }
        },
        "negative_prompt": str,
        "reference_image_multiple": [],
        "reference_information_extracted_multiple": [],
        "reference_strength_multiple": [],
        "deliberate_euler_ancestral_bug": False,
        "prefer_brownian": True,
    },
}
