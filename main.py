import multiprocessing as mp
from pathlib import Path

import gradio as gr
from loguru import logger

from src.batchtxt import main as batchtxt
from src.i2i import i2i_by_hand
from src.inpaint import for_webui as inpaint
from src.m2m import m2m, merge_av, video2frame
from src.mosaic import main as mosaic
from src.mosold import main as mosold
from src.pixiv import main as pixiv
from src.rminfo import export_info, remove_info, revert_info
from src.selector import del_current_img, move_current_img, show_first_img, show_next_img
from src.setting import webui as setting
from src.t2i import t2i, t2i_by_hand
from src.tagger import SWINV2_MODEL_DSV3_REPO, dropdown_list, tagger
from src.tileups import tile_upscale
from src.vibe import vibe, vibe_by_hand
from src.waifu2x import main as upscale
from src.water import main as water
from utils.env import env
from utils.g4f import main as g4f
from utils.plugin import load_plugins
from utils.restart import restart
from utils.update import check_update
from utils.utils import gen_script, open_folder, read_json, read_txt, return_random

webui_lang = read_json(f"./files/language/{env.webui_lang}/webui.json")
webui_help = read_txt(f"./files/language/{env.webui_lang}/help.md")
other_setting = read_txt(f"./files/language/{env.webui_lang}/setting.md")


with gr.Blocks(theme=env.theme, title="Semi-Auto-NovelAI-to-Pixiv") as demo:
    gr.Markdown(webui_lang["title"] + "    " + check_update())
    with gr.Tab(webui_lang["info"]["tab"]):
        gr.Markdown(webui_help)
    with gr.Tab(webui_lang["t2i"]["tab"]):
        with gr.Tab(webui_lang["t2i"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_lang["t2i"]["description"])
                folder = gr.Textbox(Path("./output/t2i"), visible=False)
                open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
                open_folder_.click(open_folder, inputs=folder)
            with gr.Column():
                with gr.Column(scale=3):
                    positive = gr.Textbox(
                        value=webui_lang["example"]["positive"], lines=2, label=webui_lang["t2i"]["positive"]
                    )
                    with gr.Row():
                        negative = gr.Textbox(
                            value=webui_lang["example"]["negative"],
                            lines=2,
                            label=webui_lang["t2i"]["negative"],
                            scale=3,
                        )
                        with gr.Column(scale=1):
                            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
                            times = gr.Slider(minimum=1, maximum=999, value=1, step=1, label=webui_lang["t2i"]["times"])
                with gr.Row():
                    with gr.Column(scale=1):
                        resolution = gr.Radio(
                            [
                                "832x1216",
                                "1216x832",
                                "1024x1024",
                                "512x768",
                                "768x768",
                                "640x640",
                                "1024x1536",
                                "1536x1024",
                                "1472x1472",
                                "1088x1920",
                                "1920x1088",
                            ],
                            value="832x1216",
                            label=webui_lang["t2i"]["resolution"],
                        )
                        scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label=webui_lang["t2i"]["scale"])
                        sampler = gr.Radio(
                            [
                                "k_euler",
                                "k_euler_ancestral",
                                "k_dpmpp_2s_ancestral",
                                "k_dpmpp_2m",
                                "k_dpmpp_sde",
                                "ddim_v3",
                            ],
                            value="k_euler",
                            label=webui_lang["t2i"]["sampler"],
                        )
                        noise_schedule = gr.Radio(
                            ["native", "karras", "exponential", "polyexponential"],
                            value="native",
                            label=webui_lang["t2i"]["noise_schedule"],
                        )
                        steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label=webui_lang["t2i"]["steps"])
                        sm = gr.Radio([True, False], value=False, label="sm")
                        sm_dyn = gr.Radio([True, False], value=False, label=webui_lang["t2i"]["smdyn"])
                        with gr.Row():
                            seed = gr.Textbox(value="-1", label=webui_lang["t2i"]["seed"], scale=7)
                            random_button = gr.Button(value="♻️", size="sm", scale=1)
                            random_button.click(return_random, inputs=None, outputs=seed)
                    output_img = gr.Image(scale=2)
            generate.click(
                fn=t2i_by_hand,
                inputs=[positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, sm_dyn, seed, times],
                outputs=output_img,
            )
        with gr.Tab(webui_lang["random blue picture"]["tab"]):
            with gr.Row():
                with gr.Column(scale=6):
                    gr.Markdown(webui_lang["random blue picture"]["description"])
                with gr.Row():
                    folder = gr.Textbox(Path("./output/t2i"), visible=False)
                    open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"])
                    open_folder_.click(open_folder, inputs=folder)
                    script_type = gr.Textbox("随机涩图", visible=False)
                    script_gen = gr.Button(webui_lang["t2i"]["script_gen"])
                    script_gen.click(gen_script, inputs=script_type, outputs=None)
            with gr.Row():
                forever = gr.Radio(value=False, visible=False)
                generate_button = gr.Button(webui_lang["t2i"]["generate_button"], scale=2)
                generate_forever = gr.Button(webui_lang["random blue picture"]["generate_forever"], scale=1)
                stop_button = gr.Button(webui_lang["random blue picture"]["stop_button"], scale=1)
            with gr.Row():
                show_img = gr.Image()
                show_img_ = gr.Image()
            cancel_event = show_img_.change(fn=t2i, inputs=forever, outputs=show_img_, show_progress="hidden")
            generate_button.click(fn=t2i, inputs=forever, outputs=show_img)
            generate_forever.click(fn=t2i, inputs=forever, outputs=show_img_)
            stop_button.click(None, None, None, cancels=[cancel_event])
        with gr.Tab(webui_lang["random picture"]["tab"]):
            with gr.Row():
                with gr.Column(scale=6):
                    gr.Markdown(webui_lang["random picture"]["description"])
                with gr.Row():
                    folder = gr.Textbox(Path("./output/t2i"), visible=False)
                    open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"])
                    open_folder_.click(open_folder, inputs=folder)
                    script_type = gr.Textbox("随机图片", visible=False)
                    script_gen = gr.Button(webui_lang["t2i"]["script_gen"])
            with gr.Row():
                pref = gr.Textbox("", label=webui_lang["random picture"]["pref"], lines=2, scale=5)
                position = gr.Radio(
                    value="最前面(Top)",
                    choices=["最前面(Top)", "最后面(Last)"],
                    label=webui_lang["random picture"]["position"],
                    scale=1,
                )
            with gr.Row():
                forever = gr.Radio(value=False, visible=False)
                generate_button = gr.Button(webui_lang["random blue picture"]["generate_forever"])
                stop = gr.Button(webui_lang["random blue picture"]["stop_button"])
            batchtxt_img = gr.Image()
            cancel_event = batchtxt_img.change(
                fn=batchtxt, inputs=[forever, pref, position], outputs=batchtxt_img, show_progress="hidden"
            )
            generate_button.click(fn=batchtxt, inputs=[forever, pref, position], outputs=batchtxt_img)
            stop.click(None, None, None, cancels=[cancel_event])
            script_gen.click(gen_script, inputs=[script_type, pref, position])
        plugins = load_plugins(Path("./plugins/t2i"))
        for plugin_name, plugin_module in plugins.items():
            if hasattr(plugin_module, "plugin"):
                plugin_module.plugin()
            else:
                logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
    with gr.Tab(webui_lang["i2i"]["tab"]):
        with gr.Tab(webui_lang["i2i"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_lang["t2i"]["description"])
                folder = gr.Textbox(Path("./output/i2i"), visible=False)
                open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
                open_folder_.click(open_folder, inputs=folder)
            with gr.Column():
                with gr.Column():
                    positive = gr.Textbox(
                        value=webui_lang["example"]["positive"],
                        lines=2,
                        label=webui_lang["t2i"]["positive"],
                    )
                    with gr.Row():
                        negative = gr.Textbox(
                            value=webui_lang["example"]["negative"],
                            lines=3,
                            label=webui_lang["t2i"]["negative"],
                            scale=3,
                        )
                        generate = gr.Button(value=webui_lang["t2i"]["generate_button"], scale=1)
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil")
                    with gr.Column():
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image()
                with gr.Column():
                    with gr.Row():
                        resolution = gr.Radio(
                            [
                                "832x1216",
                                "1216x832",
                                "1024x1024",
                                "512x768",
                                "768x768",
                                "640x640",
                                "1024x1536",
                                "1536x1024",
                                "1472x1472",
                                "1088x1920",
                                "1920x1088",
                            ],
                            value="832x1216",
                            label=webui_lang["t2i"]["resolution"],
                        )
                        scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label=webui_lang["t2i"]["scale"])
                        steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label=webui_lang["t2i"]["steps"])
                        with gr.Column():
                            strength = gr.Slider(
                                minimum=0, maximum=1, value=0.5, step=0.1, label=webui_lang["i2i"]["strength"]
                            )
                            noise = gr.Slider(minimum=0, maximum=1, value=0, step=0.1, label=webui_lang["i2i"]["noise"])
                            with gr.Row():
                                seed = gr.Textbox(value="-1", label=webui_lang["t2i"]["seed"], scale=7)
                                random_button = gr.Button(value="♻️", size="sm", scale=1)
                                random_button.click(return_random, inputs=None, outputs=seed)
                    with gr.Row():
                        sampler = gr.Radio(
                            [
                                "k_euler",
                                "k_euler_ancestral",
                                "k_dpmpp_2s_ancestral",
                                "k_dpmpp_2m",
                                "k_dpmpp_sde",
                                "ddim_v3",
                            ],
                            value="k_euler",
                            label=webui_lang["t2i"]["sampler"],
                        )
                        noise_schedule = gr.Radio(
                            ["native", "karras", "exponential", "polyexponential"],
                            value="native",
                            label=webui_lang["t2i"]["noise_schedule"],
                        )
                        sm = gr.Radio([True, False], value=False, label="sm")
                        sm_dyn = gr.Radio([True, False], value=False, label=webui_lang["t2i"]["smdyn"])
                generate.click(
                    fn=i2i_by_hand,
                    inputs=[
                        input_img,
                        input_path,
                        open_button,
                        positive,
                        negative,
                        resolution,
                        scale,
                        sampler,
                        noise_schedule,
                        steps,
                        strength,
                        noise,
                        sm,
                        sm_dyn,
                        seed,
                    ],
                    outputs=[output_img, output_info],
                )
        with gr.Tab("视频转绘"):
            with gr.Tab("0.教程说明"):
                gr.Markdown("1.实验性功能, 请留意每一步的选项")
                gr.Markdown("2.无法使用 ControlNet, 效果可能不太理想")
                gr.Markdown("3.还没来得及写部分页面的翻译")
            with gr.Tab("1.视频拆帧"):
                output_info = gr.Textbox(label="输出信息")
                generate_button = gr.Button("开始拆分")
                video_path = gr.Textbox(label="视频路径(*.mp4)")
                frames_save_path = gr.Textbox(label="帧保存目录(空目录)")
                with gr.Row():
                    time_interval = gr.Slider(1, 30, 3, step=1, label="间隔取帧", scale=5)
                    save_audio = gr.Checkbox(True, label="是否提取音频", scale=1)
                audio_path = gr.Textbox(label="音频保存目录")
                name = gr.Textbox("video_.mp4", visible=False)
                frames = gr.Slider(visible=False)
                fps_ = gr.Slider(visible=False)
                generate_button.click(
                    video2frame,
                    inputs=[video_path, frames_save_path, time_interval, save_audio, audio_path],
                    outputs=[name, frames, fps_, output_info],
                )
            with gr.Tab("2.反推提示词"):
                gr.Markdown("请前往 法术解析-Tagger 页面批量反推提示词")
            with gr.Tab("3.测试图生图"):
                gr.Markdown("请前往 图生图-图生图 页面进行单张测试")
            with gr.Tab("4.逐帧转绘"):
                output_info = gr.Textbox(label="输出信息")
                generate_button = gr.Button("开始转绘")
                frames_save_path = gr.Textbox(label="重绘帧目录")
                frames_m2m_path = gr.Textbox(label="重绘帧保存目录")
                with gr.Row():
                    pref = gr.Textbox("", label="追加的提示词", lines=2, scale=5)
                    position = gr.Radio(
                        value="最前面(Top)",
                        choices=["最前面(Top)", "最后面(Last)"],
                        label="追加位置",
                        scale=1,
                    )
                negative = gr.Textbox(
                    "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract],",
                    label="负面提示词",
                    lines=2,
                )
                resolution = gr.Radio(
                    [
                        "832x1216",
                        "1216x832",
                        "1024x1024",
                        "512x768",
                        "768x768",
                        "640x640",
                        "1024x1536",
                        "1536x1024",
                        "1472x1472",
                        "1088x1920",
                        "1920x1088",
                    ],
                    value="832x1216",
                    label="分辨率(宽x高)(大分辨率请注意水晶消耗)",
                )
                scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label="提示词相关性")
                steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label="采样步数")
                strength = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, label="重绘幅度")
                noise = gr.Slider(minimum=0, maximum=1, value=0, step=0.1, label="添加噪声")
                sampler = gr.Radio(
                    [
                        "k_euler",
                        "k_euler_ancestral",
                        "k_dpmpp_2s_ancestral",
                        "k_dpmpp_2m",
                        "k_dpmpp_sde",
                        "ddim_v3",
                    ],
                    value="k_euler",
                    label="采样器",
                )
                noise_schedule = gr.Radio(
                    ["native", "karras", "exponential", "polyexponential"],
                    value="native",
                    label="噪声计划表",
                )
                with gr.Row():
                    sm = gr.Radio([True, False], value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label="smdyn")
                    with gr.Row():
                        seed = gr.Textbox(value="-1", label="固定种子", scale=7)
                        random_button = gr.Button(value="♻️", size="sm", scale=1)
                        random_button.click(return_random, inputs=None, outputs=seed)
                generate_button.click(
                    fn=m2m,
                    inputs=[
                        frames_save_path,
                        frames_m2m_path,
                        pref,
                        negative,
                        position,
                        resolution,
                        scale,
                        steps,
                        sampler,
                        noise_schedule,
                        strength,
                        noise,
                        sm,
                        sm_dyn,
                        seed,
                    ],
                    outputs=output_info,
                )
            with gr.Tab("5.合并视频"):
                output_info = gr.Textbox(label="输出信息")
                generate_button = gr.Button("开始合并")
                frames_save_path = gr.Textbox(label="重绘帧目录")
                video_save_path = gr.Textbox(label="视频保存目录(不要和原视频在同一目录)")
                fps = gr.Slider(0, 60, 8, step=1, label="视频帧率")
                with gr.Row():
                    audio_path = gr.Textbox(label="音频路径(*.mp3)")
                    merge_audio = gr.Checkbox(True, label="是否并入音频")
                generate_button.click(
                    merge_av,
                    inputs=[
                        name,
                        fps,
                        time_interval,
                        frames_save_path,
                        video_save_path,
                        merge_audio,
                        audio_path,
                    ],
                    outputs=output_info,
                )
        with gr.Tab("分块重绘(正在施工)"):
            gr.Markdown("> 可以将一张大分辨率图片使用 nai3 不消耗点数放大")
            with gr.Row():
                with gr.Column():
                    generate_button = gr.Button("开始生成")
                    image = gr.Image(label="输入图片(路径为空时使用图片)", type="pil")
                    img_path = gr.Textbox(value=None, label="图片路径(单张)")
                    positive = gr.Textbox("", lines=2, label="质量词画风串(不建议添加角色描述)")
                    negative = gr.Textbox(
                        "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract],",
                        label="负面提示词",
                    )
                    strength = gr.Slider(0, 0.5, 0.15, step=0.01, label="重绘幅度(建议不要大于 0.3)")
                    engine = gr.Radio(
                        ["cain-ncnn-vulkan", "dain-ncnn-vulkan", "ifrnet-ncnn-vulkan", "rife-ncnn-vulkan"],
                        label="接缝合并引擎",
                    )
                show_image = gr.Image()
                generate_button.click(
                    tile_upscale, inputs=[image, img_path, positive, negative, strength, engine], outputs=show_image
                )
    with gr.Tab(webui_lang["inpaint"]["tab"]):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["inpaint"]["description"])
            folder = gr.Textbox(Path("./output/inpaint"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(value="", label=webui_lang["inpaint"]["input_path"], scale=5)
                mask_path = gr.Textbox(value="", label=webui_lang["inpaint"]["mask_path"], scale=5)
                open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
            with gr.Row():
                input_img = gr.Image(label=webui_lang["inpaint"]["inpaint_img"], type="pil", scale=1)
                input_mask = gr.Image(
                    image_mode="RGBA", label=webui_lang["inpaint"]["inpaint_mask"], type="pil", scale=1
                )
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                    output_img = gr.Image(scale=2)
        generate.click(
            fn=inpaint,
            inputs=[input_path, mask_path, input_img, input_mask, open_button],
            outputs=[output_img, output_info],
        )
    with gr.Tab("Vibe"):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["t2i"]["description"])
            folder = gr.Textbox(Path("./output/vibe"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=3):
                    positive = gr.Textbox(
                        value=webui_lang["example"]["positive"], lines=2, label=webui_lang["t2i"]["positive"]
                    )
                    negative = gr.Textbox(
                        value=webui_lang["example"]["negative"], lines=2, label=webui_lang["t2i"]["negative"]
                    )
                with gr.Column(scale=1):
                    generate = gr.Button(value=webui_lang["t2i"]["generate_button"], scale=1)
                    stop_button = gr.Button(webui_lang["random blue picture"]["stop_button"], scale=1)
                    generate_forever = gr.Button(webui_lang["random blue picture"]["generate_forever"], scale=1)
                    blue_imgs = gr.Checkbox(True, label=webui_lang["vibe"]["blue_imgs"])
            input_imgs = gr.Textbox("", label=webui_lang["vibe"]["input_imgs"])
            with gr.Row():
                with gr.Column(scale=1):
                    resolution = gr.Radio(
                        [
                            "832x1216",
                            "1216x832",
                            "1024x1024",
                            "512x768",
                            "768x768",
                            "640x640",
                            "1024x1536",
                            "1536x1024",
                            "1472x1472",
                            "1088x1920",
                            "1920x1088",
                        ],
                        value="832x1216",
                        label=webui_lang["t2i"]["resolution"],
                    )
                    scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label=webui_lang["t2i"]["scale"])
                    sampler = gr.Radio(
                        [
                            "k_euler",
                            "k_euler_ancestral",
                            "k_dpmpp_2s_ancestral",
                            "k_dpmpp_2m",
                            "k_dpmpp_sde",
                            "ddim_v3",
                        ],
                        value="k_euler",
                        label=webui_lang["t2i"]["sampler"],
                    )
                    noise_schedule = gr.Radio(
                        ["native", "karras", "exponential", "polyexponential"],
                        value="native",
                        label=webui_lang["t2i"]["noise_schedule"],
                    )
                    steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label=webui_lang["t2i"]["steps"])
                    sm = gr.Radio([True, False], value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label=webui_lang["t2i"]["smdyn"])
                    seed = gr.Textbox(value="-1", label=webui_lang["t2i"]["seed"])
                output_img = gr.Image(scale=2)
                output_img_ = gr.Image(visible=False)
        cancel_event = output_img_.change(
            fn=vibe, inputs=[blue_imgs, input_imgs], outputs=[output_img, output_img_], show_progress="hidden"
        )
        generate.click(
            fn=vibe_by_hand,
            inputs=[
                positive,
                negative,
                resolution,
                scale,
                sampler,
                noise_schedule,
                steps,
                sm,
                sm_dyn,
                seed,
                input_imgs,
            ],
            outputs=output_img,
        )
        generate_forever.click(fn=vibe, inputs=[blue_imgs, input_imgs], outputs=[output_img, output_img_])
        stop_button.click(None, None, None, cancels=[cancel_event])
    with gr.Tab(webui_lang["super resolution"]["tab"]):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["super resolution"]["description"])
            folder = gr.Textbox(Path("./output/upscale"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        with gr.Tab("waifu2x-nv"):
            engine = gr.Textbox("waifu2x-ncnn-vulkan", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    waifu2x_noise = gr.Slider(
                        minimum=-1,
                        maximum=3,
                        value=3,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_noise"],
                        scale=2,
                    )
                    waifu2x_scale = gr.Radio(
                        [1, 2, 4, 8, 16, 32], value=2, label=webui_lang["super resolution"]["waifu2x_scale"], scale=2
                    )
                    tta = gr.Radio([True, False], value=False, label=webui_lang["super resolution"]["tta"])
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, waifu2x_noise, waifu2x_scale, tta],
                outputs=[output_info, output_img],
            )
        with gr.Tab("Anime4K"):
            engine = gr.Textbox("Anime4K", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                zoomFactor = gr.Slider(
                    1, maximum=32, value=2, step=1, label=webui_lang["super resolution"]["waifu2x_scale"]
                )
                with gr.Row():
                    GPUMode = gr.Radio([True, False], label=webui_lang["super resolution"]["gpumode"], value=True)
                    CNNMode = gr.Radio([True, False], label=webui_lang["super resolution"]["cnnmode"], value=True)
                    HDN = gr.Radio([True, False], label=webui_lang["super resolution"]["hdn"], value=True)
                    HDNLevel = gr.Slider(
                        minimum=1, maximum=3, step=1, value=3, label=webui_lang["super resolution"]["hdn_level"]
                    )
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, zoomFactor, GPUMode, CNNMode, HDN, HDNLevel],
                outputs=[output_info, output_img],
            )
        with gr.Tab("realcugan-nv"):
            engine = gr.Textbox("realcugan-ncnn-vulkan", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    realcugan_noise = gr.Slider(
                        minimum=-1,
                        maximum=3,
                        value=3,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_noise"],
                        scale=2,
                    )
                    realcugan_scale = gr.Slider(
                        minimum=1,
                        maximum=4,
                        value=2,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_scale"],
                        scale=2,
                    )
                    realcugan_model = gr.Radio(
                        ["models-se", "models-pro", "models-nose"],
                        value="models-se",
                        label=webui_lang["super resolution"]["realcugan_model"],
                        scale=3,
                    )
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, realcugan_noise, realcugan_scale, realcugan_model],
                outputs=[output_info, output_img],
            )
        with gr.Tab("realesrgan-nv"):
            engine = gr.Textbox("realesrgan-ncnn-vulkan", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    with gr.Row():
                        realesrgan_scale = gr.Slider(
                            minimum=2,
                            maximum=4,
                            value=4,
                            step=1,
                            label=webui_lang["super resolution"]["waifu2x_scale"],
                            scale=1,
                        )
                        tta = gr.Radio([True, False], value=True, label=webui_lang["super resolution"]["tta"])
                    realesrgan_model = gr.Radio(
                        [
                            "esrgan-x4",
                            "Photo-Conservative-x4",
                            "realesr-animevideov3-x2",
                            "realesr-animevideov3-x3",
                            "realesr-animevideov3-x4",
                            "RealESRGANv2-animevideo-xsx2",
                            "RealESRGANv2-animevideo-xsx4",
                            "realesrgan-x4plus",
                            "realesrgan-x4plus-anime",
                            "realesr-general-wdn-x4v3",
                            "realesr-general-x4v3",
                            "realesrnet-x4plus",
                            "Universal-Fast-W2xEX",
                        ],
                        value="realesr-animevideov3-x4",
                        label=webui_lang["super resolution"]["realcugan_model"],
                        scale=3,
                    )
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, realesrgan_scale, realesrgan_model, tta],
                outputs=[output_info, output_img],
            )
        with gr.Tab("realsr-nv"):
            engine = gr.Textbox("realsr-ncnn-vulkan", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    realsr_model = gr.Radio(
                        ["models-DF2K_JPEG", "models-DF2K"],
                        value="models-DF2K_JPEG",
                        label=webui_lang["super resolution"]["realcugan_model"],
                    )
                    tta = gr.Radio([True, False], value=True, label=webui_lang["super resolution"]["tta"])
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, realsr_model, tta],
                outputs=[output_info, output_img],
            )
        with gr.Tab("srmd-cuda"):
            engine = gr.Textbox("srmd-cuda", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    srmd_noise = gr.Slider(
                        minimum=-1,
                        maximum=10,
                        value=3,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_noise"],
                        scale=3,
                    )
                    srmd_scale = gr.Radio(
                        [2, 3, 4], value=2, label=webui_lang["super resolution"]["waifu2x_scale"], scale=1
                    )
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, srmd_noise, srmd_scale],
                outputs=[output_info, output_img],
            )
        with gr.Tab("srmd-nv"):
            engine = gr.Textbox("srmd-ncnn-vulkan", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Column():
                with gr.Row():
                    srmd_ncnn_noise = gr.Slider(
                        minimum=-1,
                        maximum=10,
                        value=3,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_noise"],
                        scale=2,
                    )
                    srmd_ncnn_scale = gr.Slider(
                        minimum=2,
                        maximum=4,
                        value=2,
                        step=1,
                        label=webui_lang["super resolution"]["waifu2x_scale"],
                        scale=2,
                    )
                    tta = gr.Radio([True, False], value=True, label=webui_lang["super resolution"]["tta"], scale=1)
                with gr.Row():
                    input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                    open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                        output_img = gr.Image(scale=2)
            generate.click(
                fn=upscale,
                inputs=[engine, input_img, input_path, open_button, srmd_ncnn_noise, srmd_ncnn_scale, tta],
                outputs=[output_info, output_img],
            )
        with gr.Tab("waifu2x-caffe"):
            engine = gr.Textbox("waifu2x-caffe", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Row():
                mode = gr.Radio(
                    ["noise", "scale", "noise_scale"],
                    value="noise_scale",
                    label=webui_lang["super resolution"]["mode"],
                    scale=4,
                )
                scale = gr.Slider(
                    minimum=1, maximum=32, value=2, label=webui_lang["super resolution"]["waifu2x_scale"], scale=1
                )
                noise = gr.Slider(
                    minimum=0,
                    maximum=3,
                    step=1,
                    value=3,
                    label=webui_lang["super resolution"]["waifu2x_noise"],
                    scale=1,
                )
                process = gr.Radio(
                    ["cpu", "gpu", "cudnn"], value="gpu", label=webui_lang["super resolution"]["process"], scale=3
                )
                tta = gr.Radio([True, False], value=False, label=webui_lang["super resolution"]["tta"], scale=2)
            model = gr.Radio(
                [
                    "models/anime_style_art_rgb",
                    "models/anime_style_art",
                    "models/photo",
                    "models/upconv_7_anime_style_art_rgb",
                    "models/upconv_7_photo",
                    "models/upresnet10",
                    "models/cunet",
                    "models/ukbench",
                ],
                value="models/cunet",
                label=webui_lang["super resolution"]["realcugan_model"],
            )
            with gr.Row():
                input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                    output_img = gr.Image(scale=2)
        generate.click(
            fn=upscale,
            inputs=[engine, input_img, input_path, open_button, mode, scale, noise, process, tta, model],
            outputs=[output_info, output_img],
        )
        with gr.Tab("waifu2x-converter"):
            engine = gr.Textbox("waifu2x-converter", visible=False)
            generate = gr.Button(value=webui_lang["t2i"]["generate_button"])
            with gr.Row():
                mode = gr.Radio(
                    ["noise", "scale", "noise-scale"],
                    value="noise-scale",
                    label=webui_lang["super resolution"]["mode"],
                    scale=3,
                )
                scale = gr.Slider(
                    minimum=1,
                    maximum=32,
                    step=1,
                    value=2,
                    label=webui_lang["super resolution"]["waifu2x_scale"],
                    scale=2,
                )
                noise = gr.Slider(
                    minimum=0,
                    maximum=3,
                    step=1,
                    value=3,
                    label=webui_lang["super resolution"]["waifu2x_noise"],
                    scale=2,
                )
                jobs = gr.Slider(1, maximum=10, value=5, step=1, label=webui_lang["super resolution"]["jobs"], scale=2)
            with gr.Row():
                input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                    output_img = gr.Image(scale=2)
        generate.click(
            fn=upscale,
            inputs=[engine, input_img, input_path, open_button, scale, noise, mode, jobs],
            outputs=[output_info, output_img],
        )
    with gr.Tab(webui_lang["mosaic"]["tab"]):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["mosaic"]["description"])
            folder = gr.Textbox(Path("./output/mosaic"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        with gr.Row():
            generate = gr.Button(value=webui_lang["mosaic"]["generate_button"], scale=2)
            generate_old = gr.Button(value=webui_lang["mosaic"]["generate_button_old"], scale=1)
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(value="", label=webui_lang["i2i"]["input_path"], scale=5)
                open_button = gr.Radio([True, False], value=False, label=webui_lang["i2i"]["open_button"], scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
                    output_img = gr.Image(scale=2)
        generate.click(fn=mosaic, inputs=[input_path, input_img, open_button], outputs=[output_img, output_info])
        generate_old.click(fn=mosold, inputs=[input_path, input_img, open_button], outputs=[output_img, output_info])
    with gr.Tab(webui_lang["water mark"]["tab"]):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["water mark"]["description"])
            folder = gr.Textbox(Path("./output/water"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        output_path = gr.Textbox("./output/water", visible=False)
        with gr.Row():
            input_path = gr.Textbox(label=webui_lang["i2i"]["input_path"], scale=4)
            start_button = gr.Button(webui_lang["water mark"]["generate_button"], scale=1)
        output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
        start_button.click(fn=water, inputs=[input_path, output_path], outputs=output_info)
    with gr.Tab(webui_lang["pixiv"]["tab"]):
        gr.Markdown(webui_lang["pixiv"]["description"])
        with gr.Column():
            input_path = gr.Textbox(label=webui_lang["i2i"]["input_path"])
            with gr.Row():
                output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"], scale=4)
                generate = gr.Button(webui_lang["water mark"]["generate_button"], scale=1)
        generate.click(fn=pixiv, inputs=input_path, outputs=output_info)
    with gr.Tab(webui_lang["selector"]["tab"]):
        gr.Markdown(webui_lang["selector"]["description"])
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(label=webui_lang["selector"]["input_path"], scale=4)
                select_button = gr.Button(webui_lang["selector"]["select_button"], scale=1)
            with gr.Row():
                output_path = gr.Textbox(label=webui_lang["selector"]["output_path"])
                output_path_ = gr.Textbox(label=webui_lang["selector"]["output_path_"])
        with gr.Row():
            show_img = gr.Image(scale=7)
            with gr.Column(scale=1):
                next_button = gr.Button(webui_lang["selector"]["next_button"], size="lg")
                move_button = gr.Button(webui_lang["selector"]["move_button"], size="lg")
                move_button_ = gr.Button(webui_lang["selector"]["move_button_"], size="lg")
                del_button = gr.Button(webui_lang["selector"]["del_button"], size="lg")
        current_img = gr.Textbox(visible=False)
        select_button.click(fn=show_first_img, inputs=[input_path], outputs=[show_img, current_img])
        next_button.click(fn=show_next_img, outputs=[show_img, current_img])
        move_button.click(fn=move_current_img, inputs=[current_img, output_path], outputs=[show_img, current_img])
        move_button_.click(fn=move_current_img, inputs=[current_img, output_path_], outputs=[show_img, current_img])
        del_button.click(fn=del_current_img, inputs=[current_img], outputs=[show_img, current_img])
    with gr.Tab(webui_lang["rm png info"]["tab"]):
        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(webui_lang["rm png info"]["description"])
            folder = gr.Textbox(Path("./output"), visible=False)
            open_folder_ = gr.Button(webui_lang["t2i"]["open_folder"], scale=1)
            open_folder_.click(open_folder, inputs=folder)
        with gr.Tab(webui_lang["rm png info"]["tab_rm"]):
            start_button = gr.Button(webui_lang["water mark"]["generate_button"])
            input_path = gr.Textbox(label=webui_lang["i2i"]["input_path"])
            output_path = gr.Textbox("./output/info_removed", visible=False)
            output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
            start_button.click(fn=remove_info, inputs=[input_path, output_path], outputs=[output_info])
        with gr.Tab(webui_lang["rm png info"]["tab_re"]):
            start_button = gr.Button(webui_lang["water mark"]["generate_button"])
            info_file_path = gr.Textbox(label=webui_lang["rm png info"]["info_file_path"])
            input_path = gr.Textbox(label=webui_lang["rm png info"]["input_path"])
            output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
            start_button.click(fn=revert_info, inputs=[info_file_path, input_path], outputs=[output_info])
        with gr.Tab(webui_lang["rm png info"]["tab_ex"]):
            start_button = gr.Button(webui_lang["water mark"]["generate_button"])
            input_path = gr.Textbox(label=webui_lang["i2i"]["input_path"])
            output_path = gr.Textbox("./output/info_file", visible=False)
            output_info = gr.Textbox(label=webui_lang["i2i"]["output_info"])
            start_button.click(fn=export_info, inputs=[input_path, output_path], outputs=output_info)
    with gr.Tab(webui_lang["maigic analysis"]["tab"]):
        with gr.Tab(webui_lang["maigic analysis"]["tab"]):
            gr.HTML(
                """
<iframe id="myiframe" src="https://spell.novelai.dev/"></iframe>
<style>
    #myiframe {
        width: 100%;
        height: 600px;
    }
</style>
    """.replace(
                    "600", str(env.height)
                )
            )
        with gr.Tab("Tagger"):
            with gr.Row():
                with gr.Column(variant="panel"):
                    image = gr.Image(type="pil", image_mode="RGBA", label="Input")
                    with gr.Row():
                        path = gr.Textbox(label="Input Path", scale=3)
                        batch = gr.Checkbox(False, label="Batch", scale=1)
                    model_repo = gr.Dropdown(
                        dropdown_list,
                        value=SWINV2_MODEL_DSV3_REPO,
                        label="Model",
                    )
                    with gr.Row():
                        general_thresh = gr.Slider(
                            0,
                            1,
                            step=0.01,
                            value=0.35,
                            label="General Tags Threshold",
                            scale=3,
                        )
                        general_mcut_enabled = gr.Checkbox(
                            value=False,
                            label="Use MCut threshold",
                            scale=1,
                        )
                    with gr.Row():
                        character_thresh = gr.Slider(
                            0,
                            1,
                            step=0.01,
                            value=0.85,
                            label="Character Tags Threshold",
                            scale=3,
                        )
                        character_mcut_enabled = gr.Checkbox(
                            value=False,
                            label="Use MCut threshold",
                            scale=1,
                        )
                    with gr.Row():
                        clear = gr.ClearButton(
                            components=[
                                image,
                                model_repo,
                                general_thresh,
                                general_mcut_enabled,
                                character_thresh,
                                character_mcut_enabled,
                            ],
                            variant="secondary",
                            size="lg",
                        )
                        submit = gr.Button(value="Submit", variant="primary", size="lg")
                with gr.Column(variant="panel"):
                    sorted_general_strings = gr.Textbox(label="Output (string)")
                    rating = gr.Label(label="Rating")
                    character_res = gr.Label(label="Output (characters)")
                    general_res = gr.Label(label="Output (tags)")
                    clear.add(
                        [
                            sorted_general_strings,
                            rating,
                            character_res,
                            general_res,
                        ]
                    )
            submit.click(
                tagger,
                [
                    image,
                    path,
                    batch,
                    model_repo,
                    general_thresh,
                    general_mcut_enabled,
                    character_thresh,
                    character_mcut_enabled,
                ],
                outputs=[sorted_general_strings, rating, character_res, general_res],
            )
    with gr.Tab("GPT Free"):
        gr.HTML(
            """
<iframe id="myiframe" src="http://127.0.0.1:19198"></iframe>
<style>
    #myiframe {
        width: 100%;
        height: 650px;
    }
</style>
""".replace(
                "650", str(env.height)
            ).replace(
                "19198", str(env.g4f_port)
            )
        )
    plugins = load_plugins(Path("./plugins/webui"))
    for plugin_name, plugin_module in plugins.items():
        if hasattr(plugin_module, "plugin"):
            plugin_module.plugin()
        else:
            logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
    with gr.Tab(webui_lang["setting"]["tab"]):
        with gr.Row():
            modify_button = gr.Button("保存(Save)")
            restar_button = gr.Button("重启(Restart)")
        output_info = gr.Textbox(
            value="检测到已开启分享链接, 隐藏部分隐私配置!" if env.share else None,
            label=webui_lang["i2i"]["output_info"],
        )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["necessary"]):
            token = gr.Textbox(
                value=env.token,
                label=webui_lang["setting"]["description"]["token"],
                lines=2,
                visible=True if not env.share else False,
            )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["t2i"]):
            with gr.Column():
                img_size = gr.Radio(
                    [-1, "832x1216", "1216x832"],
                    value=env.img_size,
                    label=webui_lang["setting"]["description"]["img_size"],
                )
                scale = gr.Slider(0, 10, env.scale, step=0.1, label=webui_lang["setting"]["description"]["scale"])
                censor = gr.Checkbox(value=env.censor, label=webui_lang["setting"]["description"]["censor"])
                sampler = gr.Radio(
                    [
                        "k_euler",
                        "k_euler_ancestral",
                        "k_dpmpp_2s_ancestral",
                        "k_dpmpp_2m",
                        "k_dpmpp_sde",
                        "ddim_v3",
                    ],
                    value=env.sampler,
                    label=webui_lang["setting"]["description"]["sampler"],
                )
                steps = gr.Slider(1, 28, env.steps, step=1, label=webui_lang["setting"]["description"]["steps"])
                with gr.Row():
                    sm = gr.Checkbox(env.sm, label=webui_lang["setting"]["description"]["sm"])
                    sm_dyn = gr.Checkbox(env.sm_dyn, label=webui_lang["setting"]["description"]["sm"])
                noise_schedule = gr.Radio(
                    ["native", "karras", "exponential", "polyexponential"],
                    value=env.noise_schedule,
                    label=webui_lang["setting"]["description"]["noise_schedule"],
                )
                seed = gr.Textbox(env.seed, label=webui_lang["setting"]["description"]["seed"])
                t2i_cool_time = gr.Slider(
                    6, 120, env.t2i_cool_time, step=1, label=webui_lang["setting"]["description"]["t2i_cool_time"]
                )
                save_path = gr.Radio(
                    ["默认(Default)", "日期(Date)", "角色(Character)"],
                    value=env.save_path,
                    label=webui_lang["setting"]["description"]["save_path"],
                )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["i2i"]):
            with gr.Column():
                magnification = gr.Slider(
                    1,
                    1.5,
                    env.magnification,
                    step=0.1,
                    label=webui_lang["setting"]["description"]["magnification"],
                )
                hires_strength = gr.Slider(
                    0,
                    1,
                    env.hires_strength,
                    step=0.1,
                    label=webui_lang["setting"]["description"]["hires_strength"],
                )
                hires_noise = gr.Slider(
                    0,
                    1,
                    env.hires_noise,
                    step=0.1,
                    label=webui_lang["setting"]["description"]["hires_noise"],
                )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["pixiv"]):
            pixiv_cookie = gr.Textbox(
                value=env.pixiv_cookie,
                label=webui_lang["setting"]["description"]["pixiv_cookie"],
                lines=7,
                visible=True if not env.share else False,
            )
            pixiv_token = gr.Textbox(
                value=env.pixiv_token,
                label=webui_lang["setting"]["description"]["pixiv_token"],
                visible=True if not env.share else False,
            )
            allow_tag_edit = gr.Checkbox(
                env.allow_tag_edit, label=webui_lang["setting"]["description"]["allow_tag_edit"]
            )
            caption_prefix = gr.Textbox(
                value=env.caption_prefix, label=webui_lang["setting"]["description"]["caption_prefix"]
            )
            rep_tags = gr.Checkbox(env.rep_tags, label=webui_lang["setting"]["description"]["rep_tags"])
            rep_tags_per = gr.Slider(
                0, 1, env.rep_tags_per, step=0.1, label=webui_lang["setting"]["description"]["rep_tags_per"]
            )
            rep_tags_with_tag = gr.Textbox(
                value=env.rep_tags_with_tag, label=webui_lang["setting"]["description"]["rep_tags_with_tag"]
            )
            pixiv_cool_time = gr.Slider(
                10,
                360,
                env.pixiv_cool_time,
                step=1,
                label=webui_lang["setting"]["description"]["pixiv_cool_time"],
            )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["mosaic"]):
            neighbor = gr.Slider(
                0, 0.25, env.neighbor, step=0.0001, label=webui_lang["setting"]["description"]["neighbor"]
            )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["eraser"]):
            meta_data = gr.Textbox(value=env.meta_data, label=webui_lang["setting"]["description"]["meta_data"])
            revert_info_ = gr.Radio(
                choices=[True, False], value=env.revert_info, label=webui_lang["setting"]["description"]["revert_info_"]
            )
        with gr.Tab(webui_lang["setting"]["sub_tab"]["water"]):
            alpha = gr.Slider(0, 1, env.alpha, label=webui_lang["setting"]["description"]["alpha"])
            water_height = gr.Slider(
                10, 300, env.water_height, label=webui_lang["setting"]["description"]["water_height"]
            )
            gr.Markdown(webui_lang["setting"]["description"]["position"])
            with gr.Row():
                ul = gr.Checkbox(True if "左上" in env.position else False, label="左上(Upper Left)")
                ll = gr.Checkbox(True if "左下" in env.position else False, label="左下(Lower Left)")
                ur = gr.Checkbox(True if "右上" in env.position else False, label="右上(Upper Right)")
                lr = gr.Checkbox(True if "右下" in env.position else False, label="右下(Upper Right)")
            water_num = gr.Slider(1, 10, env.water_num, step=1, label=webui_lang["setting"]["description"]["water_num"])
            rotate = gr.Slider(0, 360, 45, step=1, label=webui_lang["setting"]["description"]["rotate"])
        with gr.Tab("WebUI"):
            share = gr.Checkbox(env.share, label=webui_lang["setting"]["description"]["share"])
            height = gr.Slider(300, 1200, env.height, step=10, label=webui_lang["setting"]["description"]["height"])
            port = gr.Textbox(value=env.port, label=webui_lang["setting"]["description"]["port"])
            g4f_port = gr.Textbox(env.g4f_port, label=webui_lang["setting"]["description"]["g4f_port"])
            theme = gr.Textbox(env.theme, label=webui_lang["setting"]["description"]["theme"])
            webui_lang_ = gr.Textbox(value=env.webui_lang, label=webui_lang["setting"]["description"]["webui_lang"])
        with gr.Tab(webui_lang["setting"]["sub_tab"]["other"]):
            gr.Markdown(other_setting)
        modify_button.click(
            setting,
            inputs=[
                token,
                img_size,
                scale,
                censor,
                sampler,
                steps,
                sm,
                sm_dyn,
                noise_schedule,
                seed,
                t2i_cool_time,
                save_path,
                magnification,
                hires_strength,
                hires_noise,
                pixiv_cookie,
                pixiv_token,
                allow_tag_edit,
                caption_prefix,
                rep_tags,
                rep_tags_per,
                rep_tags_with_tag,
                pixiv_cool_time,
                neighbor,
                alpha,
                water_height,
                ul,
                ll,
                ur,
                lr,
                water_num,
                rotate,
                meta_data,
                revert_info_,
                share,
                height,
                port,
                g4f_port,
                theme,
                webui_lang_,
            ],
            outputs=output_info,
        )
        restar_button.click(restart)


def main():
    demo.queue().launch(inbrowser=True, share=env.share, server_port=env.port, favicon_path="./files/logo.png")


if __name__ == "__main__":
    p1 = mp.Process(target=g4f)
    p2 = mp.Process(target=main)

    p1.start()
    p2.start()

    logger.opt(colors=True).success(
        """<c>
██╗  ██╗██╗   ██╗████████╗██████╗ ███████╗
╚██╗██╔╝╚██╗ ██╔╝╚══██╔══╝██╔══██╗╚══███╔╝
 ╚███╔╝  ╚████╔╝    ██║   ██████╔╝  ███╔╝
 ██╔██╗   ╚██╔╝     ██║   ██╔═══╝  ███╔╝
██╔╝ ██╗   ██║      ██║   ██║     ███████╗
╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚══════╝</c>"""
    )

    p1.join()
    p2.join()
