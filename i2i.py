import os
import ujson as json

from loguru import logger

from utils.error import DataIsNoneError
from utils.imgtools import get_img_info, img_to_base64
from utils.utils import *



def i2i_by_band(input_img, input_path, open_button, positive: str, negative: str, resolution: str, scale: float, sampler: str, noise_schedule: str, steps: int, strength: float, sm: bool, sm_dyn: bool):
    if open_button:
        main(input_path)
        return None, "处理完成"
    else:
        json_for_i2i["input"] = positive
        json_for_i2i["parameters"]["width"] = int(resolution.split("x")[0])
        json_for_i2i["parameters"]["height"] = int(resolution.split("x")[1])
        json_for_i2i["parameters"]["scale"] = scale
        json_for_i2i["parameters"]["sampler"] = sampler
        json_for_i2i["parameters"]["steps"] = steps
        json_for_i2i["parameters"]["strength"] = strength
        json_for_i2i["parameters"]["sm"] = sm
        json_for_i2i["parameters"]["sm_dyn"] =  sm_dyn if sm else False
        json_for_i2i["parameters"]["noise_schedule"] = noise_schedule
        seed = random.randint(1000000000, 9999999999)
        json_for_i2i["parameters"]["seed"] = seed
        json_for_i2i["parameters"]["image"] = img_to_base64(input_img)
        json_for_i2i["parameters"]["extra_noise_seed"] = seed
        json_for_i2i["parameters"]["negative_prompt"] = negative
        
        # logger.debug(json_for_i2i)
        
        save_image(generate_image(json_for_i2i), "i2i", seed, "None", "None")
        sleep_for_cool(12, 24)
        
        return f"./output/i2i/{seed}_None_None.png", None


def prepare_json(imginfo: dict, imgpath):
    if imginfo["Software"] != "NovelAI":
        logger.error("不是 NovelAI 生成的图片!")
        return "寄"
    img_comment = json.loads(imginfo["Comment"])
    json_for_i2i["input"] = img_comment["prompt"]
    width = img_comment["width"]
    height = img_comment["height"]
    # 柠檬熟了
    if width == height == 1024:
        json_for_i2i["parameters"]["width"] = int(width * env.magnification)
        json_for_i2i["parameters"]["height"] = int(height * env.magnification)
    else:
        json_for_i2i["parameters"]["width"] = int(width * env.magnification + 32)
        json_for_i2i["parameters"]["height"] = int(height * env.magnification + 32)
    json_for_i2i["parameters"]["scale"] = img_comment["scale"]
    json_for_i2i["parameters"]["sampler"] = img_comment["sampler"]
    json_for_i2i["parameters"]["steps"] = img_comment["steps"]
    json_for_i2i["parameters"]["strength"] = env.hires_strength
    json_for_i2i["parameters"]["sm"] = img_comment["sm"]
    json_for_i2i["parameters"]["sm_dyn"] = img_comment["sm_dyn"]
    json_for_i2i["parameters"]["noise_schedule"] = img_comment["noise_schedule"]
    json_for_i2i["parameters"]["seed"] = img_comment["seed"]
    json_for_i2i["parameters"]["image"] = img_to_base64(imgpath)
    json_for_i2i["parameters"]["extra_noise_seed"] = img_comment["seed"]
    json_for_i2i["parameters"]["negative_prompt"] = img_comment["uc"]

    return json_for_i2i


def main(input_path):
    type_ = "i2i"
    i2i_path = format_path(input_path)
    img_list = os.listdir(i2i_path)

    for img in img_list:
        times = 1
        while times <= 5:
            try:
                logger.warning(f"剩余水晶: {inquire_anlas()}")
                logger.info(f"正在放大{img}...")
                info_list = img.replace(".png", '').split("_")
                img_path = f"{i2i_path}/{img}"
                imginfo = get_img_info(img_path)
                json_for_i2i = prepare_json(imginfo, img_path)
                img_data = generate_image(json_for_i2i)
                if img_data == None:
                    raise DataIsNoneError
                save_image(img_data, type_, info_list[0], info_list[1], info_list[2])
                logger.warning("删除小图...")
                os.remove(img_path)
                sleep_for_cool(16, 48)
                break
            except Exception:
                sleep_for_cool(8, 24)
                times += 1
                logger.warning(f"重试 {times}/5...")
            except KeyboardInterrupt:
                logger.warning("程序退出...")
                quit()


if __name__ == "__main__":
    main("./output/choose_for_i2i")