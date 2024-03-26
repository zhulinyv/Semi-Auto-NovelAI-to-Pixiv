import gradio as gr

from t2i import t2i

with gr.Blocks() as demo:
    gr.Markdown("# Semi-Auto-NovelAI-to-Pixiv | 半自动 NovelAI 上传 Pixiv")
    with gr.Tab("文生图"):
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