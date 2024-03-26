import base64

from PIL import Image



def get_img_info(img_path):
    img = Image.open(img_path)
    return img.info

def img_to_base64(img_path):
    if isinstance(img_path, str):
        pass
    else:
        img_path.save("./output/temp.png")
        img_path = "./output/temp.png"
    with open(img_path, 'rb') as file:
        img_base64 = base64.b64encode(file.read()).decode('utf-8')
    return img_base64