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
    skip_format_str: bool = False
    noise_schedule: str = "karras"
    seed: int = -1
    t2i_cool_time: int = 9
    save_path: str = "默认(Default)"
    proxy: Union[str, None] = "xxx:xxx"
    times_for_scripts: int = 0
    rescale: float = 0
    skip_save_grid: bool = False
    quality_toggle: bool = True
    uc_preset: int = 4
    legacy_uc: bool = False

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
    suggest_tag: bool = True
    use_file_name_as_title: bool = False
    use_old_title_rule: bool = False

    # 马赛克
    neighbor: float = 0.0085

    # 水印
    water_num: int = 1

    # 抹除信息
    meta_data: str = "杂鱼~杂鱼~"
    revert_info: bool = True

    # WebUI
    share: bool = False
    height: int = 850
    port: int = 11451
    g4f_port: int = 19198
    doc_port: int = 13579
    theme: Union[str, None] = None
    webui_lang: str = "zh"
    skip_update_check: bool = False
    skip_start_sound: bool = False
    skip_load_g4f: bool = False
    skip_finish_sound: bool = False
    skip_else_log: bool = True
    num_of_suggest_tag: int = 25
    new_interface: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="allow", arbitrary_types_allowed=True)


env = Settings()
