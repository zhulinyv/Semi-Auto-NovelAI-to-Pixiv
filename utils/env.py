from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 必需
    token: Union[str, None] = None

    # 文生图
    img_size: Union[int, list[int]] = -1
    scale: float = 5
    censor: bool = False
    sampler: str = "k_euler"
    steps: int = 28
    sm: bool = False
    sm_dyn: bool = False
    noise_schedule: str = "native"
    seed: int = -1
    t2i_cool_time: int = 12
    save_path: str = "默认(Default)"

    # 图生图
    magnification: float = 1.5
    hires_strength: float = 0.5
    hires_noise: float = 0

    # 上传 Pixiv
    pixiv_cookie: Union[str, None] = None
    pixiv_token: Union[str, None] = None
    allow_tag_edit: bool = True
    caption_prefix: Union[str, None] = None
    rep_tags: bool = True
    rep_tags_per: float = 0.5
    rep_tags_with_tag: str = "杂鱼~"
    pixiv_cool_time: int = 15

    # 马赛克
    neighbor: float = 0.0085

    # 水印
    alpha: float = 0.65
    water_height: int = 135
    position: list = ["左上", "右上", "左下", "右下"]
    water_num: int = 1
    rotate: int = 45

    # 抹除信息
    meta_data: str = "杂鱼~杂鱼~"
    revert_info: bool = True

    # WebUI
    share: bool = False
    height: int = 650
    port: int = 11451
    g4f_port: int = 19198
    theme: Union[str, None] = None
    webui_lang: str = "zh"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


env = Settings()
