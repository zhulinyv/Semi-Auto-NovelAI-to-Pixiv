import gradio as gr

from batchtxt import main as batchtxt
from i2i import i2i_by_band
from inpaint import for_webui as inpaint
from mosaic import main as mosaic
from pixiv import main as pixiv
from selector import del_current_img, move_current_img, show_first_img, show_next_img
from t2i import t2i, t2i_by_band
from utils.env import env
from waifu2x import main as upscale
from water import main as water

with gr.Blocks(theme=env.theme, title="Semi-Auto-NovelAI-to-Pixiv") as demo:
    gr.Markdown("# [Semi-Auto-NovelAI-to-Pixiv](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv) | 半自动 NovelAI 上传 Pixiv")
    with gr.Tab("文生图"):
        gr.Markdown("> 等同于使用 NovelAI 官网, 支持你喜欢的画风串. 如果未返回图片, 多半是 500(服务器负载过高), 429(请求过快), 443(节点不稳定), 反正不是我的问题 ヾ(≧▽≦*)o")
        with gr.Column():
            with gr.Column(scale=3):
                positive = gr.Textbox(value="[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,", lines=2, label="正面提示词")
                with gr.Row():
                    negative = gr.Textbox(value="lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], mosaic censoring, bar censor, censored, {{{{{chibi,doll}}}}}, silhouette,", lines=2, label="负面提示词", scale=3)
                    generate = gr.Button(value="开始生成", scale=1)
            with gr.Row():
                with gr.Column(scale=1):
                    resolution = gr.Radio(["832x1216", "1216x832", "1024x1024", "512x768", "768x768", "640x640", "1024x1536", "1536x1024", "1472x1472", "1088x1920", "1920x1088"], value="832x1216", label="分辨率(宽x高)(大分辨率请注意水晶消耗)")
                    scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label="提示词相关性")
                    sampler = gr.Radio(["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral", "k_dpmpp_2m", "k_dpmpp_sde", "ddim_v3"], value="k_euler", label="采样器")
                    noise_schedule = gr.Radio(["native", "karras", "exponential", "polyexponential"], value="native", label="噪声计划表")
                    steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label="采样步数")
                    sm = gr.Radio([True, False], value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label="sm_dyn(开启需同时开启 sm)")
                    seed = gr.Textbox(value="-1", label="随机种子")
                output_img = gr.Image(scale=2)
        generate.click(fn=t2i_by_band, inputs=[positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, sm_dyn, seed], outputs=output_img)
    with gr.Tab("图生图"):
        gr.Markdown("> 等同于使用 NovelAI 官网, 支持你喜欢的画风串. 如果未返回图片, 多半是 500(服务器负载过高), 429(请求过快), 443(节点不稳定), 反正不是我的问题 ヾ(≧▽≦*)o")
        with gr.Column():
            with gr.Column():
                positive = gr.Textbox(value="[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,", lines=2, label="正面提示词")
                with gr.Row():
                    negative = gr.Textbox(value="lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], mosaic censoring, bar censor, censored, {{{{{chibi,doll}}}}}, silhouette,", lines=3, label="负面提示词", scale=3)
                    generate = gr.Button(value="开始生成", scale=1)
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil")
                with gr.Column():
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image()
            with gr.Column():
                with gr.Row():
                    resolution = gr.Radio(["832x1216", "1216x832", "1024x1024", "512x768", "768x768", "640x640", "1024x1536", "1536x1024", "1472x1472", "1088x1920", "1920x1088"], value="832x1216", label="分辨率(宽x高)(大分辨率请注意水晶消耗)")
                    scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label="提示词相关性")
                    steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label="采样步数")
                    strength = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, label="重绘幅度")
                with gr.Row():
                    sampler = gr.Radio(["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral", "k_dpmpp_2m", "k_dpmpp_sde", "ddim_v3"], value="k_euler", label="采样器")
                    noise_schedule = gr.Radio(["native", "karras", "exponential", "polyexponential"], value="native", label="噪声计划表")
                    sm = gr.Radio([True, False], value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label="sm_dyn(开启需同时开启 sm)")
            generate.click(fn=i2i_by_band, inputs=[input_img, input_path, open_button, positive, negative, resolution, scale, sampler, noise_schedule, steps, strength, sm, sm_dyn], outputs=[output_img, output_info])
    with gr.Tab("随机涩图"):
        gr.Markdown("> 通过随机组合 ./files/favorite.json 中的 tag 生成一张涩图")
        with gr.Row():
            forever = gr.Radio(value=False, visible=False)
            generate_button = gr.Button("开始生成", scale=2)
            generate_forever = gr.Button("无限生成", scale=1)
            stop_button = gr.Button("停止生成", scale=1)
        with gr.Row():
            show_img = gr.Image()
            show_img_ = gr.Image()
        cancel_event = show_img_.change(fn=t2i, inputs=forever, outputs=show_img_, show_progress="hidden")
        generate_button.click(fn=t2i, inputs=forever, outputs=show_img)
        generate_forever.click(fn=t2i, inputs=forever, outputs=show_img_)
        stop_button.click(None, None, None, cancels=[cancel_event])
    with gr.Tab("随机图片"):
        gr.Markdown("> 通过读取 ./file/prompt 中的 *.txt 作为提示词生成一张图片")
        with gr.Row():
            forever = gr.Radio(value=False, visible=False)
            generate_button = gr.Button("无限生成")
            stop = gr.Button("停止生成")
        batchtxt_img = gr.Image()
        cancel_event = batchtxt_img.change(fn=batchtxt, inputs=forever, outputs=batchtxt_img, show_progress="hidden")
        generate_button.click(fn=batchtxt, inputs=forever, outputs=batchtxt_img)
        stop.click(None, None, None, cancels=[cancel_event])
    with gr.Tab("局部重绘"):
        gr.Markdown("> 通过蒙版对图片重绘(重绘区域为白色, 其余透明而不是黑色)")
        generate = gr.Button(value="开始生成")
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理图片路径(仅在本程序运行的电脑生效)", scale=5)
                mask_path = gr.Textbox(value="", label="批量处理蒙版路径(仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(label="重绘图片", type="pil", scale=1)
                input_mask = gr.Image(image_mode="RGBA", label="重绘蒙版", type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image(scale=2)
        generate.click(fn=inpaint, inputs=[input_path, mask_path, input_img, input_mask, open_button], outputs=[output_img, output_info])
    with gr.Tab("超分降噪"):
        gr.Markdown("> 使用不同引擎放大并降噪图片")
        with gr.Tab("waifu2x-nv"):
            engine = gr.Textbox("waifu2x-ncnn-vulkan", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    waifu2x_noise = gr.Slider(minimum=-1, maximum=3, value=3, step=1, label="降噪强度", scale=2)
                    waifu2x_scale = gr.Radio([1, 2, 4, 8, 16, 32], value=2, label="放大倍数", scale=2)
                    tta = gr.Radio([True, False], value=False, label="是否开启tta模式")
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, waifu2x_noise, waifu2x_scale, tta], outputs=[output_info, output_img])
        with gr.Tab("Anime4K"):
            engine = gr.Textbox("Anime4K", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                zoomFactor = gr.Slider(1, maximum=32, value=2, step=1, label="放大倍数")
                with gr.Row():
                    GPUMode = gr.Radio([True, False], label="是否开启GPU加速", value=True)
                    CNNMode = gr.Radio([True, False], label="是否开启ACNet模式", value=True)
                    HDN = gr.Radio([True, False], label="是否为ACNet开启HDN", value=True)
                    HDNLevel = gr.Slider(minimum=1, maximum=3, step=1, value=3, label="HDN等级")
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, zoomFactor, GPUMode, CNNMode, HDN, HDNLevel], outputs=[output_info, output_img])
        with gr.Tab("realcugan-nv"):
            engine = gr.Textbox("realcugan-ncnn-vulkan", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    realcugan_noise = gr.Slider(minimum=-1, maximum=3, value=3, step=1, label="降噪强度", scale=2)
                    realcugan_scale = gr.Slider(minimum=1, maximum=4, value=2, step=1, label="放大倍数", scale=2)
                    realcugan_model = gr.Radio(["models-se", "models-pro", "models-nose"], value="models-se", label="超分模型", scale=3)
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, realcugan_noise, realcugan_scale, realcugan_model], outputs=[output_info, output_img])
        with gr.Tab("realesrgan-nv"):
            engine = gr.Textbox("realesrgan-ncnn-vulkan", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    with gr.Row():
                        realesrgan_scale = gr.Slider(minimum=2, maximum=4, value=4, step=1, label="放大倍数", scale=1)
                        tta = gr.Radio([True, False], value=True, label="是否开启tta模式")
                    realesrgan_model = gr.Radio(["esrgan-x4", "Photo-Conservative-x4", "realesr-animevideov3-x2", "realesr-animevideov3-x3", "realesr-animevideov3-x4", "RealESRGANv2-animevideo-xsx2", "RealESRGANv2-animevideo-xsx4", "realesrgan-x4plus", "realesrgan-x4plus-anime", "realesr-general-wdn-x4v3", "realesr-general-x4v3", "realesrnet-x4plus", "Universal-Fast-W2xEX"], value="realesr-animevideov3-x4", label="超分模型", scale=3)
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, realesrgan_scale, realesrgan_model, tta], outputs=[output_info, output_img])
        with gr.Tab("realsr-nv"):
            engine = gr.Textbox("realsr-ncnn-vulkan", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    realsr_model = gr.Radio(["models-DF2K_JPEG", "models-DF2K"], value="models-DF2K_JPEG", label="超分模型")
                    tta = gr.Radio([True, False], value=True, label="是否开启tta模式")
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, realsr_model, tta], outputs=[output_info, output_img])
        with gr.Tab("srmd-cuda"):
            engine = gr.Textbox("srmd-cuda", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    srmd_noise = gr.Slider(minimum=-1, maximum=10, value=3, step=1, label="降噪强度", scale=3)
                    srmd_scale = gr.Radio([2, 3, 4], value=2, label="放大倍数", scale=1)
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, srmd_noise, srmd_scale], outputs=[output_info, output_img])
        with gr.Tab("srmd-nv"):
            engine = gr.Textbox("srmd-ncnn-vulkan", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Column():
                with gr.Row():
                    srmd_ncnn_noise = gr.Slider(minimum=-1, maximum=10, value=3, step=1, label="降噪强度", scale=2)
                    srmd_ncnn_scale = gr.Slider(minimum=2, maximum=4, value=2, step=1, label="放大倍数", scale=2)
                    tta = gr.Radio([True, False], value=True, label="是否开启tta模式", scale=1)
                with gr.Row():
                    input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                    open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
                with gr.Row():
                    input_img = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        output_info = gr.Textbox(label="输出信息")
                        output_img = gr.Image(scale=2)
            generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, srmd_ncnn_noise, srmd_ncnn_scale, tta], outputs=[output_info, output_img])
        with gr.Tab("waifu2x-caffe"):
            engine = gr.Textbox("waifu2x-caffe", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Row():
                mode = gr.Radio(["noise", "scale", "noise_scale"], value="noise_scale", label="模式", scale=4)
                scale = gr.Slider(minimum=1, maximum=32, value=2, label="放大倍数", scale=1)
                noise = gr.Slider(minimum=0, maximum=3, step=1, value=3, label="降噪等级", scale=1)
                process = gr.Radio(["cpu", "gpu", "cudnn"], value="gpu", label="处理模式", scale=3)
                tta = gr.Radio([True, False], value=False, label="是否开启 tta 模式", scale=2)
            model = gr.Radio(["models/anime_style_art_rgb", "models/anime_style_art", "models/photo", "models/upconv_7_anime_style_art_rgb", "models/upconv_7_photo", "models/upresnet10", "models/cunet", "models/ukbench"], value="models/cunet", label="超分模型")
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image(scale=2)
        generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, mode, scale, noise, process, tta, model], outputs=[output_info, output_img])
        with gr.Tab("waifu2x-converter"):
            engine = gr.Textbox("waifu2x-converter", visible=False)
            generate = gr.Button(value="开始生成")
            with gr.Row():
                mode = gr.Radio(["noise", "scale", "noise-scale"], value="noise-scale", label="模式", scale=3)
                scale = gr.Slider(minimum=1, maximum=32, step=1, value=2, label="放大倍数", scale=2)
                noise = gr.Slider(minimum=0, maximum=3, step=1, value=3, label="降噪等级", scale=2)
                jobs = gr.Slider(1, maximum=10, value=5, step=1, label="处理线程数", scale=2)
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理路仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image(scale=2)
        generate.click(fn=upscale, inputs=[engine, input_img, input_path, open_button, scale, noise, mode, jobs], outputs=[output_info, output_img])
    with gr.Tab("自动打码"):
        gr.Markdown("> 对关键部位进行自动打码")
        generate = gr.Button(value="开始生成")
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image(scale=2)
        generate.click(fn=mosaic, inputs=[input_path, input_img, open_button], outputs=[output_img, output_info])
    with gr.Tab("添加水印"):
        output_path = gr.Textbox("./output/water", visible=False)
        with gr.Row():
            input_path = gr.Textbox(label="图片路径", scale=4)
            start_button = gr.Button("确定", scale=1)
        output_info = gr.Textbox(label="输出信息")
        start_button.click(fn=water, inputs=[input_path, output_path], outputs=output_info)
    with gr.Tab("上传Pixiv"):
        gr.Markdown("> 将图片或图片组上传至 Pixiv, 你可以在命令行查看上传进度")
        with gr.Column():
            input_path = gr.Textbox(label="上传路径(其中可包含单张图片或文件夹, 仅在本程序运行的电脑生效)")
            with gr.Row():
                output_info = gr.Textbox(label="输出信息", scale=4)
                generate = gr.Button("开始上传", scale=1)
        generate.click(fn=pixiv, inputs=input_path, outputs=output_info)
    with gr.Tab("法术解析"):
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
        # gr.Markdown("> 包含各种模型的免费 GPT, 来自项目 [GPT4FREE](https://github.com/xtekky/gpt4free)")
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
    with gr.Tab("图片筛选"):
        gr.Markdown("> 方便人工筛选图片(很简单的几个按钮, 应该不用说怎么用叭...)")
        with gr.Column():
            with gr.Row():
                input_path = gr.Textbox(label="图片路径", scale=4)
                select_button = gr.Button("确定", scale=1)
            with gr.Row():
                output_path = gr.Textbox(label="输出路径1")
                output_path_ = gr.Textbox(label="输出路径2")
        with gr.Row():
            show_img = gr.Image(scale=7)
            with gr.Column(scale=1):
                next_button = gr.Button("跳过", size="lg")
                move_button = gr.Button("移动1", size="lg")
                move_button_ = gr.Button("移动2", size="lg")
                del_button = gr.Button("删除", size="lg")
        current_img = gr.Textbox(visible=False)
        select_button.click(fn=show_first_img, inputs=[input_path], outputs=[show_img, current_img])
        next_button.click(fn=show_next_img, outputs=[show_img, current_img])
        move_button.click(fn=move_current_img, inputs=[current_img, output_path], outputs=[show_img, current_img])
        move_button_.click(fn=move_current_img, inputs=[current_img, output_path_], outputs=[show_img, current_img])
        del_button.click(fn=del_current_img, inputs=[current_img], outputs=[show_img, current_img])


demo.queue().launch(inbrowser=True, share=env.share, server_port=env.port, favicon_path="./files/logo.png")
