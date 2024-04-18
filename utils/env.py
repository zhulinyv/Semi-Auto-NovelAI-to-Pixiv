from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str = None
    img_size: Union[int, list[int]] = -1
    scale: float = 5
    censor: bool = False
    sampler: str = "k_euler"
    steps: int = 28
    sm: bool = False
    sm_dyn: bool = False
    noise_schedule: str = "native"
    seed: int = -1
    magnification: float = 1.5
    hires_strength: float = 0.5
    pixiv_cookie: str = None
    pixiv_token: str = None
    allow_tag_edit: bool = True
    waifu2x_scale: int = 2
    waifu2x_noise: int = 3
    share: bool = False
    height: int = 650
    port: int = 11451
    theme: Union[str, None] = "NoCrypt/miku"
    caption_prefix: str = None
    neighbor: float = 0.0085
    alpha: float = 0.65
    water_height: int = 135
    position: list = ["左上", "右上", "左下", "右下"]
    water_num: int = 1
    t2i_cool_time: int = 12
    webui_lang: str = "zh"
    pixiv_cool_time: int = 15
    meta_data: str = "杂鱼~杂鱼~"
    g4f_port: int = 19198

    class Config:
        env_file = ".env"


env = Settings()
