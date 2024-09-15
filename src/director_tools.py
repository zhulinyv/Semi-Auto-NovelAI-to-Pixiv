from PIL import Image

from utils.imgtools import img_to_base64
from utils.jsondata import (
    json_for_colorize,
    json_for_declutter,
    json_for_emotion,
    json_for_lineart,
    json_for_remove_bg,
    json_for_sketch,
)
from utils.prepare import logger
from utils.utils import (
    file_namel2pathl,
    file_path2list,
    generate_image_for_director_tools,
    save_image_for_director_tools,
)


def director_tools_remove_bg(
    director_tools_remove_bg_image_path,
    director_tools_remove_bg_batch_switch,
    director_tools_remove_bg_image: Image.Image,
):
    if director_tools_remove_bg_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_remove_bg_image_path), director_tools_remove_bg_image_path
        )
    else:
        director_tools_remove_bg_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info(f"正在处理 {image}...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_remove_bg["width"] = w
        json_for_remove_bg["height"] = h
        json_for_remove_bg["image"] = img_to_base64(image)
        masked, generated, blend = generate_image_for_director_tools(json_for_remove_bg)
        saved_paths = save_image_for_director_tools("bg-removal", [masked, generated, blend])
    return saved_paths[0], saved_paths[1], saved_paths[2], "处理完成! 图片已保存到 ./output/bg-removal"


def director_tools_line_art(
    director_tools_lineart_image_path,
    director_tools_lineart_batch_switch,
    director_tools_lineart_image: Image.Image,
):
    if director_tools_lineart_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_lineart_image_path), director_tools_lineart_image_path
        )
    else:
        director_tools_lineart_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info(f"正在处理 {image}...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_lineart["width"] = w
        json_for_lineart["height"] = h
        json_for_lineart["image"] = img_to_base64(image)
        saved_path = save_image_for_director_tools("lineart", generate_image_for_director_tools(json_for_lineart))
    return saved_path, "处理完成! 图片已保存到 ./output/lineart"


def director_tools_sketch(
    director_tools_sketch_image_path,
    director_tools_sketch_batch_switch,
    director_tools_sketch_image: Image.Image,
):
    if director_tools_sketch_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_sketch_image_path), director_tools_sketch_image_path
        )
    else:
        director_tools_sketch_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info(f"正在处理 {image}...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_sketch["width"] = w
        json_for_sketch["height"] = h
        json_for_sketch["image"] = img_to_base64(image)
        saved_path = save_image_for_director_tools("sketch", generate_image_for_director_tools(json_for_sketch))
    return saved_path, "处理完成! 图片已保存到 ./output/sketch"


def director_tools_declutter(
    director_tools_declutter_image_path,
    director_tools_declutter_batch_switch,
    director_tools_declutter_image: Image.Image,
):
    if director_tools_declutter_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_declutter_image_path), director_tools_declutter_image_path
        )
    else:
        director_tools_declutter_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info(f"正在处理 {image}...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_declutter["width"] = w
        json_for_declutter["height"] = h
        json_for_declutter["image"] = img_to_base64(image)
        saved_path = save_image_for_director_tools("declutter", generate_image_for_director_tools(json_for_declutter))
    return saved_path, "处理完成! 图片已保存到 ./output/declutter"


def director_tools_colorize(
    director_tools_colorize_defry,
    director_tools_colorize_prompt,
    director_tools_colorize_image: Image.Image,
    director_tools_colorize_image_path,
    director_tools_colorize_batch_switch,
):
    if director_tools_colorize_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_colorize_image_path), director_tools_colorize_image_path
        )
    else:
        director_tools_colorize_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info("正在处理...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_colorize["width"] = w
        json_for_colorize["height"] = h
        json_for_colorize["defry"] = director_tools_colorize_defry
        json_for_colorize["prompt"] = director_tools_colorize_prompt
        json_for_colorize["image"] = img_to_base64(image)
        saved_path = save_image_for_director_tools("colorize", generate_image_for_director_tools(json_for_colorize))
        return saved_path


def director_tools_emotion(
    director_tools_emotion_emotion: str,
    director_tools_emotion_defry,
    director_tools_emotion_prompt,
    director_tools_emotion_image: Image.Image,
    director_tools_emotion_image_path,
    director_tools_emotion_batch_switch,
):
    if director_tools_emotion_batch_switch:
        image_list = file_namel2pathl(
            file_path2list(director_tools_emotion_image_path), director_tools_emotion_image_path
        )
    else:
        director_tools_emotion_image.save("./output/temp.png")
        image_list = ["./output/temp.png"]

    for image in image_list:
        logger.info("正在处理...")
        with Image.open(image) as img:
            w, h = img.size
        json_for_emotion["width"] = w
        json_for_emotion["height"] = h
        if director_tools_emotion_defry == "Normal":
            defry = 0
        elif director_tools_emotion_defry == "Slightly Weak":
            defry = 1
        elif director_tools_emotion_defry == "Weak":
            defry = 2
        elif director_tools_emotion_defry == "Even Weaker":
            defry = 3
        elif director_tools_emotion_defry == "Very Weak":
            defry = 4
        elif director_tools_emotion_defry == "Weakest":
            defry = 5
        json_for_emotion["defry"] = defry
        prompt = f"{director_tools_emotion_emotion.lower()};;{director_tools_emotion_prompt}"
        logger.debug(f"Prompt: {prompt}")
        json_for_emotion["prompt"] = prompt
        json_for_emotion["image"] = img_to_base64(image)
        saved_path = save_image_for_director_tools("emotion", generate_image_for_director_tools(json_for_emotion))
        return saved_path
