import os
import zipfile

import requests
from loguru import logger

from utils.utils import proxies


def download(url):
    logger.info("正在下载超分引擎...")
    rep = requests.get(url, proxies=proxies, stream=True)
    with open("./files/temp.zip", "wb") as file:
        for chunk in rep.iter_content(chunk_size=256):
            file.write(chunk)
    logger.success("下载完成!")


def extract(file_path, otp_path):
    logger.info("正在解压超分引擎...")
    with zipfile.ZipFile(file_path) as zip:
        zip.extractall(otp_path)
    os.remove(file_path)
    logger.success("解压完成!")
