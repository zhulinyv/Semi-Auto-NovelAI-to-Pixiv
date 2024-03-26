import gradio as gr

from t2i import t2i, generate_by_band



with gr.Blocks() as demo:
    gr.Markdown("# Semi-Auto-NovelAI-to-Pixiv | 半自动 NovelAI 上传 Pixiv")
    with gr.Tab("文生图"):
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
                    seed = gr.Textbox(value="-1", label="随机种子")
                output_img = gr.Image(scale=2)
        generate.click(fn=generate_by_band, inputs=[positive, negative, resolution, scale, sampler, noise_schedule, steps, sm, seed], outputs=output_img)
                
    with gr.Tab("文生图(随机涩图)"):
        with gr.Column():
            gr.Markdown("> 还在写 QWQ... 文生图无限生成还有 bug, 无限生成布吉岛怎么返回图片, 所以全部是 False")
            with gr.Row():
                forever = gr.Radio([False, False], value=False, label="是否无限生成")
                generate_button = gr.Button("开始生成")
        show_img = gr.Image()
        generate_button.click(fn=t2i, inputs=forever, outputs=show_img)
    with gr.Tab("图生图"):
        ...
    with gr.Tab("Waifu2x放大"):
        ...
    with gr.Tab("自动打码"):
        ...
    with gr.Tab("上传Pixiv"):
        ...
    


demo.queue().launch(share=True, server_port=13579)