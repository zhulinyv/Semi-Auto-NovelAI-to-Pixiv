from pydantic import BaseSettings
from typing import Union



class Settings(BaseSettings):
    token: str
    img_size: Union[int, list]
    scale: float
    censor: bool
    sampler: str
    steps: int
    sm: bool
    sm_dyn: bool
    noise_schedule: str
    seed: int

    class Config:
        env_file = '.env'

env = Settings()