import os
import random
import string
import subprocess

from loguru import logger

from utils.downloader import download, extract
from utils.env import env
from utils.error import VideoCardError, Waifu2xError
from utils.imgtools import revert_img_info
from utils.utils import check_platform


def run_cmd(file, output_dir, code):
    logger.info(f"正在放大 {file}...")
    check_platform()
    logger.debug(code)

    try:
        p = subprocess.Popen(code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        result = (stdout or stderr).decode("gb18030", errors="ignore").strip()
    except Waifu2xError:
        logger.error("放大失败!")
        return "寄"

    logger.info("\n" + result)
    logger.success("放大成功!")
    logger.info(f"图片已保存到 {output_dir}")

    revert_img_info(file, output_dir)


def main(engine, file, file_path, open_button, *options):
    if open_button:
        file_path = file_path
        file_list = os.listdir(file_path)
        empty_list = []
        for i in file_list:
            empty_list.append(f"{file_path}/{i}")
        file_list = empty_list
    else:
        file_path = "./output"
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file.save(f"./output/upscale_temp_{random_string}.png")
        file = f"./output/upscale_temp_{random_string}.png"
        file_list = [file]

    for j in file_list:
        otp = "./output/upscale/" + j.replace(file_path, "").replace("/", "")

        if engine == "waifu2x-ncnn-vulkan":
            code = r".\files\waifu2x-ncnn-vulkan\waifu2x-ncnn-vulkan.exe -i {} -o {} -n {} -s {}".format(j, otp, options[0], options[1])
            if options[2]:
                code += " -x"
            run_cmd(j, otp, code)
        else:
            if os.path.exists(f"./files/else_upscale_engine/{engine}"):
                pass
            else:
                download(f"https://huggingface.co/datasets/Xytpz/Upscale-Software-Collection/resolve/main/{engine}.zip?download=true")
                extract("./files/temp.zip", "./files/else_upscale_engine")

            if engine == "Anime4K":
                code = r".\files\else_upscale_engine\Anime4K\Anime4KCPP_CLI.exe -i {} -o {} -z {}".format(j, otp, options[0])
                if options[1]:
                    code += " -q"
                if options[2]:
                    code += " -w"
                    if options[3]:
                        code += " -H -L {}".format(options[4])

            elif engine == "realcugan-ncnn-vulkan":
                code = r".\files\else_upscale_engine\realcugan-ncnn-vulkan\realcugan-ncnn-vulkan.exe -i {} -o {} -n {} -s {}".format(j, otp, options[0], options[1])
                if options[2] != "models-se":
                    code += " -m {}".format(options[2])

            elif engine == "realesrgan-ncnn-vulkan":
                code = r".\files\else_upscale_engine\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe -i {} -o {} -s {} -n {}".format(j, otp, options[0], options[1])
                if options[2]:
                    code += " -x"

            elif engine == "realsr-ncnn-vulkan":
                code = rf".\files\else_upscale_engine\realsr-ncnn-vulkan\realsr-ncnn-vulkan.exe -i {j} -o {otp}"
                if options[0] != "models-DF2K_JPEG":
                    code += " -m {}".format(options[0])
                if options[1]:
                    code += " -x"

            elif engine == "srmd-cuda":
                try:
                    from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, nvmlInit

                    nvmlInit()
                    vcard = nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(0))
                    logger.info(f"检测到显卡: {vcard}")
                    if "GTX" in vcard:
                        software = "srmd-cuda-GTX-W2xEX.exe"
                    elif "RTX" in vcard:
                        software = "srmd-cuda-RTX-W2xEX.exe"
                    else:
                        logger.error("仅支持 RTX 和 GTX 系列显卡")
                except VideoCardError:
                    logger.error("仅支持 RTX 和 GTX 系列显卡")
                code = r".\files\else_upscale_engine\srmd-cuda\{} -i {} -o {} -n {} -s {}".format(software, j, otp, options[0], options[1])

            elif engine == "srmd-ncnn-vulkan":
                code = r".\files\else_upscale_engine\srmd-ncnn-vulkan\srmd-ncnn-vulkan.exe -i {} -o {} -n {} -s {}".format(j, otp, options[0], options[1])
                if options[2]:
                    code += " -x"

            else:
                if engine == "waifu2x-caffe":
                    code = os.path.abspath("./files/else_upscale_engine/waifu2x-caffe/waifu2x-caffe-cui.exe")
                    code += " -i {} -o {} -m {} -s {} -n {}".format(os.path.abspath(j), os.path.abspath(otp), options[0], options[1], options[2])
                    if options[3] != "gpu":
                        code += " -p {}".format(options[3])
                    if options[4]:
                        code += " -t 1"
                    if options[5] != "models/cunet":
                        code += " --model_dir {}".format(options[5])

                elif engine == "waifu2x-converter":
                    code = "cd ./files/else_upscale_engine/waifu2x-converter\n"
                    code += os.path.abspath("./files/else_upscale_engine/waifu2x-converter/waifu2x-converter-cpp.exe")
                    code += " -i {} -o {} --scale-ratio {} --noise-level {} -m {} -j {}".format(os.path.abspath(j), os.path.abspath(otp), options[0], options[1], options[2], options[3])

                with open("./output/temp_waifu2x.bat", "w") as temp:
                    temp.write(code)
                os.system(os.path.abspath("./output/temp_waifu2x.bat"))
                revert_img_info(j, otp)

            if engine in ["waifu2x-caffe", "waifu2x-converter"]:
                pass
            else:
                run_cmd(j, otp, code)

    if open_button:
        return "图片已保存到 ./output/upscale...", None
    else:
        return None, otp


if __name__ == "__main__":
    main(None, "./output/choose_for_upscale", True, env.waifu2x_noise, env.waifu2x_scale)
