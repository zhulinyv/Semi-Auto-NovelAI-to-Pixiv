import random

from src.t2i import t2i_by_hand
from utils.env import env
from utils.utils import format_str, read_json, sleep_for_cool


def prompt():
    prompt = ""
    data = read_json("./files/favorite.json")
    clothes = list(data["服装"].keys())
    for clothe in clothes:
        styles = list(data["服装"][clothe].keys())
        style = random.choice(styles)
        prompt += data["服装"][clothe][style] + ", "
    return format_str(prompt)


def t2i():
    positive = prompt()
    data = read_json("./files/favorite.json")
    negative = format_str(random.choice(data["negative_prompt"]["belief"]))
    resolution = (
        random.choice(["832x1216", "1024x1024", "1216x832"])
        if env.img_size == -1
        else "{}x{}".format(env.img_size[0], env.img_size[1])
    )
    scale = env.scale
    sampler = env.sampler
    noise_schedule = env.noise_schedule
    steps = env.steps
    sm = env.sm
    sm_dyn = env.sm_dyn
    seed = random.randint(1000000000, 9999999999) if env.seed == -1 else env.seed
    img = t2i_by_hand(positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, sm_dyn, seed, 1)
    sleep_for_cool(env.t2i_cool_time - 6, env.t2i_cool_time + 6)
    return img
