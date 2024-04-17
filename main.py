import gradio as gr

from src.batchtxt import main as batchtxt
from src.i2i import i2i_by_band
from src.inpaint import for_webui as inpaint
from src.mosaic import main as mosaic
from src.mosold import main as mosold
from src.pixiv import main as pixiv
from src.rminfo import remove_info, revert_info
from src.selector import del_current_img, move_current_img, show_first_img, show_next_img
from src.t2i import t2i, t2i_by_band
from src.waifu2x import main as upscale
from src.water import main as water
from utils.env import env
from utils.utils import read_json

webui_lang = read_json(f"./files/webui_{env.webui_lang}.json")


with gr.Blocks(theme=env.theme, title="Semi-Auto-NovelAI-to-Pixiv") as demo:
    gr.Markdown(webui_lang["title"])
    with gr.Tab(webui_lang["t2i"]["tab"]):
        gr.Markdown(webui_lang["t2i"]["description"])
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
                    generate = gr.Button(value=webui_lang["t2i"]["generate_button"], scale=1)
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
        generate.click(
            fn=t2i_by_band,
            inputs=[positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, sm_dyn, seed],
            outputs=output_img,
        )
    with gr.Tab(webui_lang["i2i"]["tab"]):
        gr.Markdown(webui_lang["t2i"]["description"])
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
                    strength = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, label=webui_lang["i2i"]["strength"])
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
                fn=i2i_by_band,
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
                    sm,
                    sm_dyn,
                ],
                outputs=[output_img, output_info],
            )
    with gr.Tab(webui_lang["random blue picture"]["tab"]):
        gr.Markdown(webui_lang["random blue picture"]["description"])
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
        gr.Markdown(webui_lang["random picture"]["description"])
        with gr.Row():
            pref = gr.Textbox("", label=webui_lang["random picture"]["pref"], lines=2, scale=5)
            position = gr.Radio(
                value="最前面(Top)"["最前面(Top)", "最后面(Last)"],
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
    with gr.Tab(webui_lang["inpaint"]["tab"]):
        gr.Markdown(webui_lang["inpaint"]["description"])
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
    with gr.Tab(webui_lang["super resolution"]["tab"]):
        gr.Markdown(webui_lang["super resolution"]["description"])
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
        gr.Markdown(webui_lang["mosaic"]["description"])
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
        gr.Markdown(webui_lang["water mark"]["description"])
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
        gr.Markdown(webui_lang["rm png info"]["description"])
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
    with gr.Tab(webui_lang["maigic analysis"]["tab"]):
        gr.HTML(
            """
<iframe id="myiframe" src="https://spell.novelai.dev/"></iframe>
<style>
    #myiframe {
        width: 100%;
        height: 650px;
    }
</style>
""".replace(
                "650", str(env.height)
            )
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
            )
        )


demo.queue().launch(inbrowser=True, share=env.share, server_port=env.port, favicon_path="./files/logo.png")
