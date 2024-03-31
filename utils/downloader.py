import os
import requests
import zipfile



def download(url):
    rep = requests.get(url, stream=True)
    
    with open("./files/temp.zip", 'wb') as file:
        for chunk in rep.iter_content(chunk_size=512):
            file.write(chunk)


def extract(file_path, otp_path):
    with zipfile.ZipFile(file_path) as zip:
        zip.extractall(otp_path)
    
    os.remove(file_path)



download("https://huggingface.co/datasets/Xytpz/Upscale-Software-Collection/resolve/main/Upscale-Software-Collection.zip?download=true")

extract("./files/temp.zip", "./files/else_upscale_engine")


