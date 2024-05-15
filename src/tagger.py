from pathlib import Path

from gradio_client import Client, file
from loguru import logger

from utils.utils import file_namel2pathl, file_path2list, file_path2name

try:
    client = Client("SmilingWolf/wd-tagger", verbose=False)
except Exception:
    pass


# Dataset v3 series of models:
SWINV2_MODEL_DSV3_REPO = "SmilingWolf/wd-swinv2-tagger-v3"
CONV_MODEL_DSV3_REPO = "SmilingWolf/wd-convnext-tagger-v3"
VIT_MODEL_DSV3_REPO = "SmilingWolf/wd-vit-tagger-v3"

# Dataset v2 series of models:
MOAT_MODEL_DSV2_REPO = "SmilingWolf/wd-v1-4-moat-tagger-v2"
SWIN_MODEL_DSV2_REPO = "SmilingWolf/wd-v1-4-swinv2-tagger-v2"
CONV_MODEL_DSV2_REPO = "SmilingWolf/wd-v1-4-convnext-tagger-v2"
CONV2_MODEL_DSV2_REPO = "SmilingWolf/wd-v1-4-convnextv2-tagger-v2"
VIT_MODEL_DSV2_REPO = "SmilingWolf/wd-v1-4-vit-tagger-v2"


dropdown_list = [
    SWINV2_MODEL_DSV3_REPO,
    CONV_MODEL_DSV3_REPO,
    VIT_MODEL_DSV3_REPO,
    MOAT_MODEL_DSV2_REPO,
    SWIN_MODEL_DSV2_REPO,
    CONV_MODEL_DSV2_REPO,
    CONV2_MODEL_DSV2_REPO,
    VIT_MODEL_DSV2_REPO,
]


def format_dict(dict_):
    try:
        list_ = dict_["confidences"]
        dict_ = {}
        for i in list_:
            dict_.update({i["label"]: i["confidence"]})
        return dict_
    except KeyError:
        return None


def tagger(
    image,
    path,
    batch,
    model_repo,
    general_thresh,
    general_mcut_enabled,
    character_thresh,
    character_mcut_enabled,
):
    if batch:
        # imgs_list = [Path(path) / i for i in file_path2list(path)]
        imgs_list = file_namel2pathl(file_path2list(path), Path(path))
    else:
        image.save("./output/temp.png")
        imgs_list = ["./output/temp.png"]
    for img in imgs_list:
        if str(img).endswith(".txt"):
            pass
        else:
            while 1:
                try:
                    logger.info(f"正在反推: {img}...")
                    result = client.predict(
                        file(img),  # filepath  in 'Input' Image component
                        model_repo,  # Literal['SmilingWolf/wd-swinv2-tagger-v3', 'SmilingWolf/wd-convnext-tagger-v3', 'SmilingWolf/wd-vit-tagger-v3', 'SmilingWolf/wd-v1-4-moat-tagger-v2', 'SmilingWolf/wd-v1-4-swinv2-tagger-v2', 'SmilingWolf/wd-v1-4-convnext-tagger-v2', 'SmilingWolf/wd-v1-4-convnextv2-tagger-v2', 'SmilingWolf/wd-v1-4-vit-tagger-v2']  in 'Model' Dropdown component
                        general_thresh,  # float (numeric value between 0 and 1) in 'General Tags Threshold' Slider component
                        general_mcut_enabled,  # bool  in 'Use MCut threshold' Checkbox component
                        character_thresh,  # float (numeric value between 0 and 1) in 'Character Tags Threshold' Slider component
                        character_mcut_enabled,  # bool  in 'Use MCut threshold' Checkbox component
                        api_name="/predict",
                    )
                    if batch:
                        with open(Path(path) / file_path2name(img).replace(".png", ".txt"), "w", encoding="utf-8") as f:
                            f.write(result[0])
                    break
                except Exception as e:
                    logger.error(f"出现错误: {e}")
                    logger.info("正在重试...")
    return result[0], format_dict(result[1]), format_dict(result[2]), format_dict(result[3])
