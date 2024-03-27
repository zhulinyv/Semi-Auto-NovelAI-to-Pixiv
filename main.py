import gradio as gr

from t2i import t2i, t2i_by_band
from i2i import i2i_by_band
from waifu2x import main as waifu2x
from mosaic import main as mosaic
from pixiv import main as pixiv

from utils.utils import env



with gr.Blocks() as demo:
    gr.Markdown("# [Semi-Auto-NovelAI-to-Pixiv](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv) | 半自动 NovelAI 上传 Pixiv")
    with gr.Tab("文生图"):
        gr.Markdown("> 等同于使用 NovelAI 官网, 支持你喜欢的画风串. 如果未返回图片, 多半是 500(服务器负载过高) 或 429(请求过快), 反正不是我的问题 ヾ(≧▽≦*)o")
        with gr.Column():
            with gr.Column(scale=3):
                positive = gr.Textbox(value="[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,", label="正面提示词")
                with gr.Row():
                    negative = gr.Textbox(value="lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], mosaic censoring, bar censor, censored, {{{{{chibi,doll}}}}}, silhouette,", label="负面提示词", scale=3)
                    generate = gr.Button(value="开始生成", scale=1)
            with gr.Row():
                with gr.Column(scale=1):
                    resolution = gr.Radio(["832x1216", "1216x832", "1024x1024", "512x768", "768x768", "640x640"], value="832x1216", label="分辨率(宽x高)")
                    scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label="提示词相关性")
                    sampler = gr.Radio(["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral", "k_dpmpp_2m", "k_dpmpp_sde", "ddim_v3"], value="k_euler", label="采样器")
                    noise_schedule = gr.Radio(["native", "karras", "exponential", "polyexponential"], value="native", label="噪声计划表")
                    steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label="采样步数")
                    sm = gr.Radio([True, False],value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label="sm_dyn(开启需同时开启 sm)")
                    seed = gr.Textbox(value="-1", label="随机种子")
                output_img = gr.Image(scale=2)
        generate.click(fn=t2i_by_band, inputs=[positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, sm_dyn, seed], outputs=output_img)
    with gr.Tab("图生图"):
        gr.Markdown("> 等同于使用 NovelAI 官网, 支持你喜欢的画风串. 如果未返回图片, 多半是 500(服务器负载过高) 或 429(请求过快), 反正不是我的问题 ヾ(≧▽≦*)o")
        with gr.Column():
            with gr.Column():
                positive = gr.Textbox(value="[suimya, muririn], artist:ciloranko,[artist:sho_(sho_lwlw)],[[tianliang duohe fangdongye]], [eip (pepai)], [rukako], [[[memmo]]], [[[[[hoshi (snacherubi)]]]]], year 2023, 1girl, cute, loli,", label="正面提示词")
                with gr.Row():
                    negative = gr.Textbox(value="lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], mosaic censoring, bar censor, censored, {{{{{chibi,doll}}}}}, silhouette,", label="负面提示词", scale=3)
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
                    resolution = gr.Radio(["832x1216", "1216x832", "1024x1024", "512x768", "768x768", "640x640"], value="832x1216", label="分辨率(宽x高)")
                    scale = gr.Slider(minimum=0, maximum=10, value=5, step=0.1, label="提示词相关性")
                    steps = gr.Slider(minimum=0, maximum=28, value=28, step=1, label="采样步数")
                    strength = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, label="重绘幅度")
                with gr.Row():
                    sampler = gr.Radio(["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral", "k_dpmpp_2m", "k_dpmpp_sde", "ddim_v3"], value="k_euler", label="采样器")
                    noise_schedule = gr.Radio(["native", "karras", "exponential", "polyexponential"], value="native", label="噪声计划表")
                    sm = gr.Radio([True, False],value=False, label="sm")
                    sm_dyn = gr.Radio([True, False], value=False, label="sm_dyn(开启需同时开启 sm)")
            generate.click(fn=i2i_by_band, inputs=[input_img, input_path, open_button, positive, negative, resolution, scale, sampler, noise_schedule, steps, strength, sm, sm_dyn], outputs=output_img)
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
    with gr.Tab("Waifu2x放大"):
        gr.Markdown("> 使用 Waifu2x 放大并降噪图片")
        generate = gr.Button(value="开始生成")
        with gr.Column():
            with gr.Row():
                waifu2x_noise = gr.Slider(minimum=-1, maximum=3, value=3, step=1, label="降噪强度")
                waifu2x_scale = gr.Radio([1, 2, 4, 8, 16, 32], value=2, label="放大倍数")
            with gr.Row():
                input_path = gr.Textbox(value="", label="批量处理路径(仅在本程序运行的电脑生效)", scale=5)
                open_button = gr.Radio([True, False], value=False, label="是否启用批处理", scale=1)
            with gr.Row():
                input_img = gr.Image(type="pil", scale=1)
                with gr.Column(scale=2):
                    output_info = gr.Textbox(label="输出信息")
                    output_img = gr.Image(scale=2)
        generate.click(fn=waifu2x, inputs=[input_img, input_path, open_button, waifu2x_noise, waifu2x_scale], outputs=[output_info, output_img])
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
    with gr.Tab("上传Pixiv"):
        gr.Markdown("> 将图片或图片组上传至 Pixiv, 你可以在命令行查看上传进度")
        with gr.Column():
            input_path = gr.Textbox(label="上传路径(其中可包含单张图片或文件夹, 仅在本程序运行的电脑生效)")
            with gr.Row():
                output_info =gr.Textbox(label="输出信息", scale=4)
                generate = gr.Button("开始上传", scale=1)
        generate.click(fn=pixiv, inputs=input_path, outputs=output_info)
    with gr.Tab("法术解析"):
        gr.HTML("""
<iframe id="myiframe" src="https://spell.novelai.dev/"></iframe>
<style>
    #myiframe {
        width: 100%;
        height: 650px;
    }
</style>
""".replace("650", str(env.height)))
        


demo.queue().launch(inbrowser=env.share, share=True, server_port=11451)