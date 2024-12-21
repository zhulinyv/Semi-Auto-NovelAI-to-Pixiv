from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 必需
    token: Union[str, None] = None

    # 文生图
    model: str = "nai-diffusion-3"
    img_size: Union[int, list[int]] = -1
    scale: float = 5.0
    censor: bool = False
    sampler: str = "k_euler"
    steps: int = 28
    sm: bool = False
    sm_dyn: bool = False
    variety: bool = False
    decrisp: bool = False
    noise_schedule: str = "native"
    seed: int = -1
    t2i_cool_time: int = 9
    save_path: str = "默认(Default)"
    proxy: Union[str, None] = "xxx:xxx"

    # 图生图
    magnification: float = 1.5
    hires_strength: float = 0.5
    hires_noise: float = 0
    i2i_cool_time: int = 12

    # 上传 Pixiv
    pixiv_cookie: Union[str, None] = "xxx"
    pixiv_token: Union[str, None] = "xxx"
    allow_tag_edit: bool = True
    caption_prefix: Union[str, None] = "Hi there! 这里是小丫头片子, 芝士我的 QQ 群: 559063963, 欢迎!"
    rep_tags: bool = True
    rep_tags_per: float = 0.5
    rep_tags_with_tag: str = "杂鱼~"
    pixiv_cool_time: int = 15
    remove_info: bool = True
    r18: bool = True
    default_tag: list[str] = ["女の子", "萝莉"]

    # 马赛克
    neighbor: float = 0.0085

    # 水印
    alpha: float = 0.65
    water_height: int = 135
    position: list = ["左上(Upper Left)", "左下(Lower Left)", "右上(Upper Right)", "右下(Upper Right)"]
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
    skip_update_check: bool = False
    skip_start_sound: bool = False
    skip_load_g4f: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="allow", arbitrary_types_allowed=True)


env = Settings()
