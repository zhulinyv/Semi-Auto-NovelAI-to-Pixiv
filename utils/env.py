from pydantic_settings import BaseSettings
from typing import Union



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

    class Config:
        env_file = '.env'

env = Settings()