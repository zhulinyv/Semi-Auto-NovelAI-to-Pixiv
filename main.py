import multiprocessing as mp

import gradio as gr

from utils.env import env
from utils.gpt4free import main as g4f
from utils.prepare import logger


def main():
    import os
    from pathlib import Path

    from src.batch_inpaint import for_webui as inpaint
    from src.batch_mosaic import main as mosaic
    from src.batch_tagger import SWINV2_MODEL_DSV3_REPO, dropdown_list, tagger
    from src.batch_vibe_transfer import vibe_by_hand
    from src.batch_waifu2x import main as upscale
    from src.batch_watermark import main as water
    from src.director_tools import (
        director_tools_colorize,
        director_tools_declutter,
        director_tools_emotion,
        director_tools_line_art,
        director_tools_remove_bg,
        director_tools_sketch,
    )
    from src.image2image import i2i_by_hand
    from src.image2pixiv import main as pixiv
    from src.movie2movie import m2m, merge_av, video2frame
    from src.pnginfo_modify import export_info, remove_info, revert_info
    from src.setting_update import webui as setting
    from src.text2image_nsfw import return_resolution, t2i, t2i_by_hand
    from src.text2image_sfw import main as batchtxt
    from src.tiled_upscale import tile_upscale
    from utils.imgtools import _return_pnginfo, return_pnginfo
    from utils.plugin import install_plugin, load_plugins, plugin_list, uninstall_plugin
    from utils.restart import restart
    from utils.selector import copy_current_img, del_current_img, move_current_img, show_first_img, show_next_img
    from utils.update import check_update, update
    from utils.utils import (
        FAVORTES_FILE,
        MODEL,
        NOISE_SCHEDULE,
        RESOLUTION,
        SAMPLER,
        add_item_for_yaml,
        add_wildcard_to_textbox,
        cancel_probabilities_for_item,
        del_item_for_yaml,
        gen_script,
        list_to_str,
        open_folder,
        read_json,
        read_txt,
        read_yaml,
        return_names_list,
        return_random,
        return_source_or_type_list,
        return_wildcard_tag,
        update_image_size,
        update_name_to_dropdown_list,
        update_t2i_nsf_dropdown_list,
    )

    # ------------------------------ #

    webui_language = read_json(f"./files/languages/{env.webui_lang}/webui.json")

    default_positive_input = (
        webui_language["example"]["positive"]
        if not os.path.exists("start.json")
        else read_json("start.json")["positive"]
    )
    default_negative_input = (
        webui_language["example"]["negative"]
        if not os.path.exists("start.json")
        else read_json("start.json")["negative"]
    )

    # ------------------------------ #

    def open_output_folder_block(output_folder):
        open_output_folder_folder = gr.Button(webui_language["t2i"]["open_folder"], scale=1)
        open_output_folder_folder.click(
            open_folder, inputs=gr.Textbox(Path(f"./output/{output_folder}"), visible=False)
        )

    # ------------------------------ #

    with gr.Blocks(
        theme=env.theme, title="Semi-Auto-NovelAI-to-Pixiv", head=read_txt("./files/webui/select_by_hot_key.html")
    ) as sanp:
        # ---------- 标题 ---------- #
        gr.Markdown(webui_language["title"] + "    " + check_update())
        # ---------- 教程说明 ---------- #
        with gr.Tab(webui_language["info"]["tab"]):
            gr.Markdown(read_txt("./files/languages/README.md"))
        # ---------- 文生图 ---------- #
        with gr.Tab(webui_language["t2i"]["tab"]):
            with gr.Tab(webui_language["t2i"]["tab"]):
                with gr.Row():
                    with gr.Column(scale=5):
                        gr.Markdown(webui_language["t2i"]["description"])
                    open_output_folder_block("t2i")
                with gr.Column():
                    with gr.Column(scale=3):
                        text2image_positive_input = gr.Textbox(
                            value=default_positive_input,
                            lines=2,
                            label=webui_language["t2i"]["positive"],
                        )
                        with gr.Row():
                            text2image_negative_input = gr.Textbox(
                                value=default_negative_input,
                                lines=2,
                                label=webui_language["t2i"]["negative"],
                                scale=3,
                            )
                            with gr.Column(scale=1):
                                text2image_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                                text2image_quantity = gr.Slider(
                                    minimum=1, maximum=999, value=1, step=1, label=webui_language["t2i"]["times"]
                                )
                    with gr.Tab("生成参数"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                text2image_resolution = gr.Dropdown(
                                    RESOLUTION,
                                    value=(
                                        "832x1216"
                                        if env.img_size == -1
                                        else "{}x{}".format((env.img_size)[0], (env.img_size)[1])
                                    ),
                                    label=webui_language["t2i"]["resolution"],
                                )
                                with gr.Row():
                                    text2image_width = gr.Textbox(
                                        value=(env.img_size)[0] if env.img_size != -1 else "832",
                                        label=webui_language["t2i"]["width"],
                                    )
                                    text2image_height = gr.Textbox(
                                        value=(env.img_size)[1] if env.img_size != -1 else "1216",
                                        label=webui_language["t2i"]["height"],
                                    )
                                    text2image_resolution.change(
                                        return_resolution,
                                        text2image_resolution,
                                        outputs=[text2image_width, text2image_height],
                                        show_progress="hidden",
                                    )
                                text2image_scale = gr.Slider(
                                    minimum=0,
                                    maximum=10,
                                    value=env.scale,
                                    step=0.1,
                                    label=webui_language["t2i"]["scale"],
                                )
                                text2image_sampler = gr.Dropdown(
                                    SAMPLER,
                                    value=env.sampler,
                                    label=webui_language["t2i"]["sampler"],
                                )
                                text2image_noise_schedule = gr.Dropdown(
                                    NOISE_SCHEDULE,
                                    value=env.noise_schedule,
                                    label=webui_language["t2i"]["noise_schedule"],
                                )
                                text2image_steps = gr.Slider(
                                    minimum=0, maximum=50, value=env.steps, step=1, label=webui_language["t2i"]["steps"]
                                )
                                with gr.Row():
                                    text2image_sm = gr.Checkbox(value=env.sm, label="sm")
                                    text2image_sm_dyn = gr.Checkbox(
                                        value=env.sm_dyn, label=webui_language["t2i"]["smdyn"]
                                    )
                                with gr.Row():
                                    text2image_variety = gr.Checkbox(value=env.variety, label="variety")
                                    text2image_decrisp = gr.Checkbox(value=env.decrisp, label="decrisp")
                                with gr.Row():
                                    text2image_seed = gr.Textbox(
                                        value=str(env.seed), label=webui_language["t2i"]["seed"], scale=7
                                    )
                                    text2image_random_seed = gr.Button(value="♻️", size="sm", scale=1)
                                    text2image_random_seed.click(return_random, inputs=None, outputs=text2image_seed)
                            text2image_output_image = gr.Image(scale=2)
                    with gr.Tab("wildcards"):
                        with gr.Row():
                            text2image_wildcard_file = gr.Dropdown(
                                choices=FAVORTES_FILE,
                                label="wildcard文件",
                            )
                            text2image_wildcard_name = gr.Dropdown(label="名称")
                            text2image_wildcard_file.change(
                                update_name_to_dropdown_list,
                                inputs=text2image_wildcard_file,
                                outputs=text2image_wildcard_name,
                            )
                            text2image_add_wildcard_button = gr.Button("添加到文本框")
                            text2image_add_wildcard_button.click(
                                add_wildcard_to_textbox,
                                inputs=[
                                    text2image_positive_input,
                                    text2image_negative_input,
                                    text2image_wildcard_file,
                                    text2image_wildcard_name,
                                ],
                                outputs=[text2image_positive_input, text2image_negative_input],
                            )
                        text2image_wildcard_tag = gr.Textbox(label="tag")
                        text2image_wildcard_name.change(
                            return_wildcard_tag,
                            inputs=[text2image_wildcard_file, text2image_wildcard_name],
                            outputs=text2image_wildcard_tag,
                        )
                    text2image_generate_button.click(
                        fn=t2i_by_hand,
                        inputs=[
                            text2image_positive_input,
                            text2image_negative_input,
                            text2image_width,
                            text2image_height,
                            text2image_scale,
                            text2image_sampler,
                            text2image_noise_schedule,
                            text2image_steps,
                            text2image_sm,
                            text2image_sm_dyn,
                            text2image_variety,
                            text2image_decrisp,
                            text2image_seed,
                            text2image_quantity,
                        ],
                        outputs=text2image_output_image,
                    )
            with gr.Tab(webui_language["random blue picture"]["tab"]):
                with gr.Tab(webui_language["random blue picture"]["tab"]):
                    with gr.Row():
                        with gr.Column(scale=6):
                            gr.Markdown(webui_language["random blue picture"]["description"])
                        with gr.Row():
                            open_output_folder_block("t2i")
                            generate_text2image_nsfw_script_button = gr.Button(webui_language["t2i"]["script_gen"])
                    with gr.Row():
                        text2image_nsfw_fixed_artist = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/artists.yaml")),
                            value="随机",
                            label="固定画风",
                        )
                        text2image_nsfw_fixed_prefix = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/prefixes.yaml")),
                            value="随机",
                            label="固定质量词",
                        )
                        text2image_nsfw_fixed_negative = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/negative.yaml")),
                            value="随机",
                            label="固定负面",
                        )
                    with gr.Row():
                        text2image_nsfw_fixed_source = gr.Dropdown(
                            choices=["随机"]
                            + return_source_or_type_list(
                                cancel_probabilities_for_item(read_yaml("./files/favorites/characters.yaml"))
                            ),
                            value="随机",
                            label="固定角色出处",
                        )
                        text2image_nsfw_fixed_character = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/characters.yaml")),
                            value="随机",
                            label="固定角色",
                        )
                        text2image_nsfw_fixed_action_type = gr.Dropdown(
                            choices=["随机"]
                            + return_source_or_type_list(
                                cancel_probabilities_for_item(read_yaml("./files/favorites/actions.yaml"))
                            ),
                            value="随机",
                            label="固定动作类型",
                        )
                        text2image_nsfw_fixed_action = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/actions.yaml")),
                            value="随机",
                            label="固定动作",
                        )
                    with gr.Row():
                        text2image_nsfw_fixed_emotion = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/emotions.yaml")),
                            value="随机",
                            label="固定表情",
                        )
                        text2image_nsfw_fixed_surrounding = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/surroundings.yaml")),
                            value="随机",
                            label="固定场景",
                        )
                        text2image_nsfw_fixed_fixed_stains = gr.Dropdown(
                            choices=return_names_list(read_yaml("./files/favorites/stains.yaml")),
                            value="随机",
                            label="固定污渍",
                        )
                    with gr.Row():
                        text2image_nsfw_update_dropdown_list_button = gr.Button(
                            webui_language["t2i"]["update_dropdown_list"]
                        )
                        text2image_nsfw_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                        text2image_nsfw_generate_forever_button = gr.Button(
                            webui_language["random blue picture"]["generate_forever"]
                        )
                        text2image_nsfw_stop_button = gr.Button(webui_language["random blue picture"]["stop_button"])
                    with gr.Row():
                        text2image_nsfw_output_image = gr.Image()
                        text2image_nsfw_forever_output_image = gr.Image()
                    text2image_nsfw_cancel_event = text2image_nsfw_forever_output_image.change(
                        fn=t2i,
                        inputs=[
                            gr.Radio(value=False, visible=False),
                            text2image_nsfw_fixed_artist,
                            text2image_nsfw_fixed_prefix,
                            text2image_nsfw_fixed_negative,
                            text2image_nsfw_fixed_source,
                            text2image_nsfw_fixed_character,
                            text2image_nsfw_fixed_action_type,
                            text2image_nsfw_fixed_action,
                            text2image_nsfw_fixed_emotion,
                            text2image_nsfw_fixed_surrounding,
                            text2image_nsfw_fixed_fixed_stains,
                        ],
                        outputs=text2image_nsfw_forever_output_image,
                        show_progress="hidden",
                    )
                    text2image_nsfw_generate_button.click(
                        fn=t2i,
                        inputs=[
                            gr.Radio(value=False, visible=False),
                            text2image_nsfw_fixed_artist,
                            text2image_nsfw_fixed_prefix,
                            text2image_nsfw_fixed_negative,
                            text2image_nsfw_fixed_source,
                            text2image_nsfw_fixed_character,
                            text2image_nsfw_fixed_action_type,
                            text2image_nsfw_fixed_action,
                            text2image_nsfw_fixed_emotion,
                            text2image_nsfw_fixed_surrounding,
                            text2image_nsfw_fixed_fixed_stains,
                        ],
                        outputs=text2image_nsfw_output_image,
                    )
                    text2image_nsfw_generate_forever_button.click(
                        fn=t2i,
                        inputs=[
                            gr.Radio(value=False, visible=False),
                            text2image_nsfw_fixed_artist,
                            text2image_nsfw_fixed_prefix,
                            text2image_nsfw_fixed_negative,
                            text2image_nsfw_fixed_source,
                            text2image_nsfw_fixed_character,
                            text2image_nsfw_fixed_action_type,
                            text2image_nsfw_fixed_action,
                            text2image_nsfw_fixed_emotion,
                            text2image_nsfw_fixed_surrounding,
                            text2image_nsfw_fixed_fixed_stains,
                        ],
                        outputs=text2image_nsfw_forever_output_image,
                    )
                    text2image_nsfw_stop_button.click(None, None, None, cancels=[text2image_nsfw_cancel_event])
                    generate_text2image_nsfw_script_button.click(
                        gen_script,
                        inputs=[
                            gr.Textbox("随机蓝图", visible=False),
                            text2image_nsfw_fixed_artist,
                            text2image_nsfw_fixed_prefix,
                            text2image_nsfw_fixed_negative,
                            text2image_nsfw_fixed_source,
                            text2image_nsfw_fixed_character,
                            text2image_nsfw_fixed_action_type,
                            text2image_nsfw_fixed_action,
                            text2image_nsfw_fixed_emotion,
                            text2image_nsfw_fixed_surrounding,
                            text2image_nsfw_fixed_fixed_stains,
                        ],
                        outputs=None,
                    )
                    text2image_nsfw_update_dropdown_list_button.click(
                        update_t2i_nsf_dropdown_list,
                        inputs=None,
                        outputs=[
                            text2image_nsfw_fixed_artist,
                            text2image_nsfw_fixed_prefix,
                            text2image_nsfw_fixed_negative,
                            text2image_nsfw_fixed_source,
                            text2image_nsfw_fixed_character,
                            text2image_nsfw_fixed_action_type,
                            text2image_nsfw_fixed_action,
                            text2image_nsfw_fixed_emotion,
                            text2image_nsfw_fixed_surrounding,
                            text2image_nsfw_fixed_fixed_stains,
                        ],
                    )
                with gr.Tab("添加提示词"):
                    item_to_add = gr.Dropdown(
                        choices=FAVORTES_FILE,
                        label="想追加什么内容?(必填)",
                    )
                    tag_to_add = gr.Textbox("", lines=3, label="提示词(必填)")
                    with gr.Row():
                        name_to_add = gr.Textbox(label="名称(必填)")
                        probability_to_add = gr.Dropdown(
                            choices=["较大概率选中", "中等概率选中", "较小概率选中"],
                            value="中等概率选中",
                            label="概率(必填)",
                        )
                        source_to_add = gr.Textbox(label="出处(选择 characters.yaml 时必填)")
                        type_to_add = gr.Textbox(label="类型(选择 actions.yaml 时必填)")
                    with gr.Row():
                        sampler_to_add = gr.Dropdown(
                            choices=SAMPLER, value="k_euler", label="采样器(选择 artists.yaml 时必填)"
                        )
                        noise_schedule_to_add = gr.Dropdown(
                            choices=NOISE_SCHEDULE, value="native", label="噪声计划表(选择 artists.yaml 时必填)"
                        )
                        cfg_to_add = gr.Slider(0, 10, 5, step=0.1, label="cfg(选择 artists.yaml 时必填)")
                    with gr.Row():
                        sm_to_add = gr.Dropdown(
                            choices=[True, False], value=False, label="sm(选择 artists.yaml 时必填)"
                        )
                        sm_dyn_to_add = gr.Dropdown(
                            choices=[True, False], value=False, label="sm_dyn(选择 artists.yaml 时必填)"
                        )
                        variety_to_add = gr.Dropdown(
                            choices=[True, False], value=False, label="variety(选择 artists.yaml 时必填)"
                        )
                        decrisp_to_add = gr.Dropdown(
                            choices=[True, False], value=False, label="decrisp(选择 artists.yaml 时必填)"
                        )
                    add_button = gr.Button("添加")
                    add_button.click(
                        add_item_for_yaml,
                        inputs=[
                            item_to_add,
                            tag_to_add,
                            name_to_add,
                            probability_to_add,
                            source_to_add,
                            type_to_add,
                            sampler_to_add,
                            noise_schedule_to_add,
                            cfg_to_add,
                            sm_to_add,
                            sm_dyn_to_add,
                            variety_to_add,
                            decrisp_to_add,
                        ],
                        outputs=[
                            item_to_add,
                            tag_to_add,
                            name_to_add,
                            probability_to_add,
                            source_to_add,
                            type_to_add,
                            sampler_to_add,
                            noise_schedule_to_add,
                            cfg_to_add,
                            sm_to_add,
                            sm_dyn_to_add,
                        ],
                    )
                with gr.Tab("删除提示词"):
                    item_to_del = gr.Dropdown(
                        choices=FAVORTES_FILE,
                        label="想删除什么内容?(必填)",
                    )
                    name_to_del = gr.Dropdown(label="名称(必填)")
                    item_to_del.change(update_name_to_dropdown_list, inputs=item_to_del, outputs=name_to_del)
                    tag_to_del = gr.Textbox(label="tag")
                    name_to_del.change(
                        return_wildcard_tag,
                        inputs=[item_to_del, name_to_del],
                        outputs=tag_to_del,
                    )
                    del_button = gr.Button("删除")
                    del_button.click(
                        del_item_for_yaml, inputs=[item_to_del, name_to_del], outputs=[item_to_del, name_to_del]
                    )

            with gr.Tab(webui_language["random picture"]["tab"]):
                with gr.Row():
                    with gr.Column(scale=6):
                        gr.Markdown(webui_language["random picture"]["description"])
                    with gr.Row():
                        open_output_folder_block("t2i")
                        generate_text2image_sfw_script_button = gr.Button(webui_language["t2i"]["script_gen"])
                with gr.Row():
                    text2image_sfw_prefix = gr.Textbox(
                        "", label=webui_language["random picture"]["pref"], lines=2, scale=4
                    )
                    text2image_sfw_position = gr.Radio(
                        value="最前面(Top)",
                        choices=["最前面(Top)", "最后面(Last)"],
                        label=webui_language["random picture"]["position"],
                        scale=1,
                    )
                    with gr.Column():
                        text2image_sfw_random_artists_top_switch = gr.Checkbox(
                            value=False,
                            label=webui_language["random picture"]["text2image_sfw_random_artists_top_switch"],
                        )
                        text2image_sfw_random_artists_last_switch = gr.Checkbox(
                            value=False,
                            label=webui_language["random picture"]["text2image_sfw_random_artists_last_switch"],
                        )
                        text2image_sfw_prevent_to_move_switch = gr.Checkbox(
                            value=False, label=webui_language["random picture"]["text2image_sfw_prevent_to_move_switch"]
                        )
                with gr.Row():
                    text2image_sfw_generate_forever_button = gr.Button(
                        webui_language["random blue picture"]["generate_forever"]
                    )
                    text2image_sfw_stop_button = gr.Button(webui_language["random blue picture"]["stop_button"])
                text2image_sfw_output_image = gr.Image()
                text2image_sfw_cancel_event = text2image_sfw_output_image.change(
                    fn=batchtxt,
                    inputs=[
                        gr.Radio(value=False, visible=False),
                        text2image_sfw_prefix,
                        text2image_sfw_position,
                        text2image_sfw_random_artists_top_switch,
                        text2image_sfw_random_artists_last_switch,
                        text2image_sfw_prevent_to_move_switch,
                    ],
                    outputs=text2image_sfw_output_image,
                    show_progress="hidden",
                )
                text2image_sfw_generate_forever_button.click(
                    fn=batchtxt,
                    inputs=[
                        gr.Radio(value=False, visible=False),
                        text2image_sfw_prefix,
                        text2image_sfw_position,
                        text2image_sfw_random_artists_top_switch,
                        text2image_sfw_random_artists_last_switch,
                        text2image_sfw_prevent_to_move_switch,
                    ],
                    outputs=text2image_sfw_output_image,
                )
                text2image_sfw_stop_button.click(None, None, None, cancels=[text2image_sfw_cancel_event])
                generate_text2image_sfw_script_button.click(
                    gen_script,
                    inputs=[
                        gr.Textbox("随机图片", visible=False),
                        text2image_sfw_prefix,
                        text2image_sfw_position,
                        text2image_sfw_random_artists_top_switch,
                        text2image_sfw_random_artists_last_switch,
                        text2image_sfw_prevent_to_move_switch,
                    ],
                )
            with gr.Tab("Vibe"):
                with gr.Row():
                    with gr.Column(scale=5):
                        gr.Markdown(webui_language["t2i"]["description"])
                    open_output_folder_block("vibe")
                with gr.Column():
                    with gr.Column(scale=3):
                        vibe_transfer_positive_input = gr.Textbox(
                            value=default_positive_input,
                            lines=2,
                            label=webui_language["t2i"]["positive"],
                        )
                        with gr.Row():
                            vibe_transfer_negative_input = gr.Textbox(
                                value=default_negative_input,
                                lines=2,
                                label=webui_language["t2i"]["negative"],
                                scale=3,
                            )
                            with gr.Column(scale=1):
                                vibe_transfer_generate_button = gr.Button(
                                    value=webui_language["t2i"]["generate_button"], scale=1
                                )
                                vibe_transfer_quantity = gr.Slider(
                                    minimum=1, maximum=999, value=1, step=1, label=webui_language["t2i"]["times"]
                                )
                    with gr.Tab("生成参数"):
                        vibe_transfer_input_images = gr.Textbox("", label=webui_language["vibe"]["input_imgs"])
                        with gr.Row():
                            with gr.Column(scale=1):
                                vibe_transfer_resolution = gr.Dropdown(
                                    RESOLUTION,
                                    value=(
                                        "832x1216"
                                        if env.img_size == -1
                                        else "{}x{}".format((env.img_size)[0], (env.img_size)[1])
                                    ),
                                    label=webui_language["t2i"]["resolution"],
                                )
                                with gr.Row():
                                    vibe_transfer_width = gr.Textbox(
                                        value=(env.img_size)[0] if env.img_size != -1 else "832",
                                        label=webui_language["t2i"]["width"],
                                    )
                                    vibe_transfer_height = gr.Textbox(
                                        value=(env.img_size)[1] if env.img_size != -1 else "1216",
                                        label=webui_language["t2i"]["height"],
                                    )
                                    vibe_transfer_resolution.change(
                                        return_resolution,
                                        vibe_transfer_resolution,
                                        outputs=[vibe_transfer_width, vibe_transfer_height],
                                        show_progress="hidden",
                                    )
                                vibe_transfer_scale = gr.Slider(
                                    minimum=0,
                                    maximum=10,
                                    value=env.scale,
                                    step=0.1,
                                    label=webui_language["t2i"]["scale"],
                                )
                                vibe_transfer_sampler = gr.Dropdown(
                                    SAMPLER,
                                    value=env.sampler,
                                    label=webui_language["t2i"]["sampler"],
                                )
                                vibe_transfer_noise_schedule = gr.Dropdown(
                                    NOISE_SCHEDULE,
                                    value=env.noise_schedule,
                                    label=webui_language["t2i"]["noise_schedule"],
                                )
                                vibe_transfer_steps = gr.Slider(
                                    minimum=0, maximum=50, value=env.steps, step=1, label=webui_language["t2i"]["steps"]
                                )
                                with gr.Row():
                                    vibe_transfer_sm = gr.Checkbox(value=env.sm, label="sm")
                                    vibe_transfer_sm_dyn = gr.Checkbox(
                                        value=env.sm_dyn, label=webui_language["t2i"]["smdyn"]
                                    )
                                with gr.Row():
                                    vibe_transfer_variety = gr.Checkbox(value=env.variety, label="variety")
                                    vibe_transfer_decrisp = gr.Checkbox(value=env.decrisp, label="decrisp")
                                vibe_transfer_seed = gr.Textbox(
                                    value=str(env.seed), label=webui_language["t2i"]["seed"]
                                )
                            vibe_transfer_output_image = gr.Image(scale=2)
                    with gr.Tab("wildcards"):
                        with gr.Row():
                            vibe_transfer_wildcard_file = gr.Dropdown(
                                choices=FAVORTES_FILE,
                                label="wildcard文件",
                            )
                            vibe_transfer_wildcard_name = gr.Dropdown(label="名称")
                            vibe_transfer_wildcard_file.change(
                                update_name_to_dropdown_list,
                                inputs=vibe_transfer_wildcard_file,
                                outputs=vibe_transfer_wildcard_name,
                            )
                            vibe_transfer_add_wildcard_button = gr.Button("添加到文本框")
                            vibe_transfer_add_wildcard_button.click(
                                add_wildcard_to_textbox,
                                inputs=[
                                    vibe_transfer_positive_input,
                                    vibe_transfer_negative_input,
                                    vibe_transfer_wildcard_file,
                                    vibe_transfer_wildcard_name,
                                ],
                                outputs=[vibe_transfer_positive_input, vibe_transfer_negative_input],
                            )
                        vibe_transfer_wildcard_tag = gr.Textbox(label="tag")
                        vibe_transfer_wildcard_name.change(
                            return_wildcard_tag,
                            inputs=[vibe_transfer_wildcard_file, vibe_transfer_wildcard_name],
                            outputs=vibe_transfer_wildcard_tag,
                        )
                    vibe_transfer_generate_button.click(
                        fn=vibe_by_hand,
                        inputs=[
                            vibe_transfer_positive_input,
                            vibe_transfer_negative_input,
                            vibe_transfer_width,
                            vibe_transfer_height,
                            vibe_transfer_scale,
                            vibe_transfer_sampler,
                            vibe_transfer_noise_schedule,
                            vibe_transfer_steps,
                            vibe_transfer_sm,
                            vibe_transfer_sm_dyn,
                            vibe_transfer_variety,
                            vibe_transfer_decrisp,
                            vibe_transfer_seed,
                            vibe_transfer_input_images,
                            vibe_transfer_quantity,
                        ],
                        outputs=vibe_transfer_output_image,
                    )
            # ---------- 文生图插件 ---------- #
            text2image_plugins = load_plugins(Path("./plugins/t2i"))
            for plugin_name, plugin_module in text2image_plugins.items():
                if hasattr(plugin_module, "plugin"):
                    plugin_module.plugin()
                    logger.success(f" 成功加载插件: {plugin_name}")
                else:
                    logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
        # ---------- 图生图 ---------- #
        with gr.Tab(webui_language["i2i"]["tab"]):
            with gr.Tab(webui_language["i2i"]["tab"]):
                with gr.Row():
                    with gr.Column(scale=8):
                        gr.Markdown(webui_language["t2i"]["description"])
                    open_output_folder_block("i2i")
                with gr.Column():
                    with gr.Column():
                        image2image_positive_input = gr.Textbox(
                            value=default_positive_input,
                            lines=2,
                            label=webui_language["t2i"]["positive"],
                        )
                        with gr.Row():
                            image2image_negative_input = gr.Textbox(
                                value=default_negative_input,
                                lines=3,
                                label=webui_language["t2i"]["negative"],
                                scale=3,
                            )
                            image2image_generate_button = gr.Button(
                                value=webui_language["t2i"]["generate_button"], scale=1
                            )
                    with gr.Tab("生成参数"):
                        with gr.Row():
                            image2image_input_path = gr.Textbox(
                                value="", label=webui_language["i2i"]["input_path"], scale=5
                            )
                            image2image_batch_switch = gr.Radio(
                                [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                            )
                        with gr.Row():
                            image2image_input_image = gr.Image(type="pil")
                            with gr.Column():
                                image2image_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                                image2image_output_image = gr.Image()
                        with gr.Column():
                            with gr.Row():
                                image2image_resolution = gr.Dropdown(
                                    RESOLUTION,
                                    value=(
                                        "832x1216"
                                        if env.img_size == -1
                                        else "{}x{}".format((env.img_size)[0], (env.img_size)[1])
                                    ),
                                    label=webui_language["t2i"]["resolution"],
                                )
                                image2image_width = gr.Textbox(value="832", label=webui_language["t2i"]["width"])
                                image2image_height = gr.Textbox(value="1216", label=webui_language["t2i"]["height"])
                                image2image_resolution.change(
                                    return_resolution,
                                    image2image_resolution,
                                    outputs=[image2image_width, image2image_height],
                                    show_progress="hidden",
                                )
                                image2image_sampler = gr.Dropdown(
                                    SAMPLER,
                                    value=env.sampler,
                                    label=webui_language["t2i"]["sampler"],
                                )
                                image2image_noise_schedule = gr.Dropdown(
                                    NOISE_SCHEDULE,
                                    value=env.noise_schedule,
                                    label=webui_language["t2i"]["noise_schedule"],
                                )
                            with gr.Row():
                                image2image_strength = gr.Slider(
                                    minimum=0,
                                    maximum=1,
                                    value=env.hires_strength,
                                    step=0.1,
                                    label=webui_language["i2i"]["strength"],
                                )
                                image2image_noise = gr.Slider(
                                    minimum=0,
                                    maximum=1,
                                    value=env.hires_noise,
                                    step=0.1,
                                    label=webui_language["i2i"]["noise"],
                                )
                                image2image_scale = gr.Slider(
                                    minimum=0,
                                    maximum=10,
                                    value=env.scale,
                                    step=0.1,
                                    label=webui_language["t2i"]["scale"],
                                )
                                image2image_steps = gr.Slider(
                                    minimum=0, maximum=50, value=env.steps, step=1, label=webui_language["t2i"]["steps"]
                                )
                            with gr.Row():
                                with gr.Column():
                                    image2image_sm = gr.Checkbox(value=env.sm, label="sm", scale=2)
                                    image2image_sm_dyn = gr.Checkbox(
                                        value=env.sm_dyn, label=webui_language["t2i"]["smdyn"], scale=2
                                    )
                                with gr.Column():
                                    image2image_variety = gr.Checkbox(value=env.variety, label="variety")
                                    image2image_decrisp = gr.Checkbox(value=env.decrisp, label="decrisp")
                                with gr.Column(scale=1):
                                    image2image_seed = gr.Textbox(
                                        value=str(env.seed), label=webui_language["t2i"]["seed"], scale=7
                                    )
                                    image2image_random_button = gr.Button(value="♻️", size="sm", scale=1)
                                image2image_random_button.click(return_random, inputs=None, outputs=image2image_seed)
                    with gr.Tab("wildcards"):
                        with gr.Row():
                            image2image_wildcard_file = gr.Dropdown(
                                choices=FAVORTES_FILE,
                                label="wildcard文件",
                            )
                            image2image_wildcard_name = gr.Dropdown(label="名称")
                            image2image_wildcard_file.change(
                                update_name_to_dropdown_list,
                                inputs=image2image_wildcard_file,
                                outputs=image2image_wildcard_name,
                            )
                            image2image_add_wildcard_button = gr.Button("添加到文本框")
                            image2image_add_wildcard_button.click(
                                add_wildcard_to_textbox,
                                inputs=[
                                    image2image_positive_input,
                                    image2image_negative_input,
                                    image2image_wildcard_file,
                                    image2image_wildcard_name,
                                ],
                                outputs=[image2image_positive_input, image2image_negative_input],
                            )
                        image2image_wildcard_tag = gr.Textbox(label="tag")
                        image2image_wildcard_name.change(
                            return_wildcard_tag,
                            inputs=[image2image_wildcard_file, image2image_wildcard_name],
                            outputs=image2image_wildcard_tag,
                        )
                    image2image_generate_button.click(
                        fn=i2i_by_hand,
                        inputs=[
                            image2image_input_image,
                            image2image_input_path,
                            image2image_batch_switch,
                            image2image_positive_input,
                            image2image_negative_input,
                            image2image_width,
                            image2image_height,
                            image2image_scale,
                            image2image_sampler,
                            image2image_noise_schedule,
                            image2image_steps,
                            image2image_strength,
                            image2image_noise,
                            image2image_sm,
                            image2image_sm_dyn,
                            image2image_variety,
                            image2image_decrisp,
                            image2image_seed,
                        ],
                        outputs=[image2image_output_image, image2image_output_information],
                    )
            with gr.Tab(webui_language["m2m"]["tab"]):
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab0"]):
                    gr.Markdown(webui_language["m2m"]["description"]["tab0_1"])
                    gr.Markdown(webui_language["m2m"]["description"]["tab0_2"])
                    gr.Markdown(webui_language["m2m"]["description"]["tab0_3"])
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab1"]):
                    movie2movie_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                    movie2movie_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                    movie2movie_video_path = gr.Textbox(label=webui_language["m2m"]["func"]["video_path"])
                    movie2movie_frames_save_path = gr.Textbox(label=webui_language["m2m"]["func"]["frames_save_path"])
                    with gr.Row():
                        movie2movie_time_interval = gr.Slider(
                            1, 30, 3, step=1, label=webui_language["m2m"]["func"]["interval_framing"], scale=5
                        )
                        movie2movie_save_audio_switch = gr.Checkbox(
                            True, label=webui_language["m2m"]["func"]["extract_audio"], scale=1
                        )
                    movie2movie_audio_path = gr.Textbox(label=webui_language["m2m"]["func"]["audio_save_path"])
                    movie2movie_name = gr.Textbox("video_.mp4", visible=False)
                    movie2movie_frames = gr.Slider(visible=False)
                    _movie2movie_fps = gr.Slider(visible=False)
                    movie2movie_generate_button.click(
                        video2frame,
                        inputs=[
                            movie2movie_video_path,
                            movie2movie_frames_save_path,
                            movie2movie_time_interval,
                            movie2movie_save_audio_switch,
                            movie2movie_audio_path,
                        ],
                        outputs=[
                            movie2movie_name,
                            movie2movie_frames,
                            _movie2movie_fps,
                            movie2movie_output_information,
                        ],
                    )
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab2"]):
                    gr.Markdown(webui_language["m2m"]["description"]["tab2"])
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab3"]):
                    gr.Markdown(webui_language["m2m"]["description"]["tab3"])
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab4"]):
                    movie2movie_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                    movie2movie_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                    movie2movie_frames_save_path = gr.Textbox(label=webui_language["m2m"]["func"]["i2i_frames_path"])
                    movie2movie_frames_m2m_path = gr.Textbox(label=webui_language["m2m"]["func"]["frames_save_path"])
                    with gr.Row():
                        movie2movie_prompt = gr.Textbox(
                            "", label=webui_language["random picture"]["pref"], lines=2, scale=5
                        )
                        movie2movie_position = gr.Radio(
                            value="最前面(Top)",
                            choices=["最前面(Top)", "最后面(Last)"],
                            label=webui_language["random picture"]["position"],
                            scale=1,
                        )
                    movie2movie_negative = gr.Textbox(
                        default_negative_input,
                        label=webui_language["t2i"]["negative"],
                        lines=2,
                    )
                    movie2movie_resolution = gr.Dropdown(
                        RESOLUTION,
                        value=(
                            "832x1216" if env.img_size == -1 else "{}x{}".format((env.img_size)[0], (env.img_size)[1])
                        ),
                        label=webui_language["t2i"]["resolution"],
                    )
                    movie2movie_scale = gr.Slider(
                        minimum=0, maximum=10, value=env.scale, step=0.1, label=webui_language["t2i"]["scale"]
                    )
                    movie2movie_steps = gr.Slider(
                        minimum=0, maximum=50, value=env.steps, step=1, label=webui_language["t2i"]["steps"]
                    )
                    movie2movie_strength = gr.Slider(
                        minimum=0, maximum=1, value=0.5, step=0.1, label=webui_language["i2i"]["strength"]
                    )
                    movie2movie_noise = gr.Slider(
                        minimum=0, maximum=1, value=0, step=0.1, label=webui_language["i2i"]["noise"]
                    )
                    movie2movie_sampler = gr.Dropdown(
                        SAMPLER,
                        value=env.sampler,
                        label=webui_language["t2i"]["sampler"],
                    )
                    movie2movie_noise_schedule = gr.Dropdown(
                        NOISE_SCHEDULE,
                        value=env.noise_schedule,
                        label=webui_language["t2i"]["noise_schedule"],
                    )
                    with gr.Row():
                        movie2movie_sm = gr.Checkbox(value=False, visible=False)
                        movie2movie_sm_dyn = gr.Checkbox(value=False, visible=False)
                        movie2movie_variety = gr.Checkbox(value=env.variety, label="variety")
                        movie2movie_decrisp = gr.Checkbox(value=env.decrisp, label="decrisp")
                        with gr.Row():
                            movie2movie_seed = gr.Textbox(
                                value=str(env.seed), label=webui_language["t2i"]["seed"], scale=7
                            )
                            movie2movie_random_button = gr.Button(value="♻️", size="sm", scale=1)
                            movie2movie_random_button.click(return_random, inputs=None, outputs=movie2movie_seed)
                    movie2movie_generate_button.click(
                        fn=m2m,
                        inputs=[
                            movie2movie_frames_save_path,
                            movie2movie_frames_m2m_path,
                            movie2movie_prompt,
                            movie2movie_negative,
                            movie2movie_position,
                            movie2movie_resolution,
                            movie2movie_scale,
                            movie2movie_steps,
                            movie2movie_sampler,
                            movie2movie_noise_schedule,
                            movie2movie_strength,
                            movie2movie_noise,
                            movie2movie_sm,
                            movie2movie_sm_dyn,
                            movie2movie_variety,
                            movie2movie_decrisp,
                            movie2movie_seed,
                        ],
                        outputs=movie2movie_output_information,
                    )
                with gr.Tab(webui_language["m2m"]["sub_tab"]["tab5"]):
                    movie2movie_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                    movie2movie_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                    movie2movie_frames_save_path = gr.Textbox(label=webui_language["m2m"]["func"]["i2i_frames_path"])
                    movie2movie_video_save_path = gr.Textbox(label=webui_language["m2m"]["func"]["video_save_path"])
                    movie2movie_fps = gr.Slider(0, 60, 8, step=1, label=webui_language["m2m"]["func"]["fps"])
                    with gr.Row():
                        movie2movie_audio_path = gr.Textbox(label=webui_language["m2m"]["func"]["audio_path"])
                        movie2movie_merge_audio = gr.Checkbox(True, label=webui_language["m2m"]["func"]["merge_audio"])
                    movie2movie_generate_button.click(
                        merge_av,
                        inputs=[
                            movie2movie_name,
                            movie2movie_fps,
                            movie2movie_time_interval,
                            movie2movie_frames_save_path,
                            movie2movie_video_save_path,
                            movie2movie_merge_audio,
                            movie2movie_audio_path,
                        ],
                        outputs=movie2movie_output_information,
                    )
            with gr.Tab(webui_language["tile"]["tab"]):
                gr.Markdown(webui_language["tile"]["description"])
                with gr.Row():
                    with gr.Column():
                        tiled_upscale_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                        tiled_upscale_image = gr.Image(label=webui_language["tile"]["image"], type="pil")
                        tiled_upscale_img_path = gr.Textbox(value=None, label=webui_language["tile"]["img_path"])
                        tiled_upscale_positive_input = gr.Textbox("", lines=2, label=webui_language["tile"]["positive"])
                        tiled_upscale_negative_input = gr.Textbox(
                            default_negative_input,
                            label="负面提示词",
                            lines=3,
                        )
                        tiled_upscale_strength = gr.Slider(
                            0, 0.5, 0.15, step=0.01, label=webui_language["i2i"]["strength"]
                        )
                        tiled_upscale_engine = gr.Radio(
                            [
                                "rife",
                                "rife-anime",
                                "rife-HD",
                                "rife-UHD",
                                "rife-v2",
                                "rife-v2.3",
                                "rife-v2.4",
                                "rife-v3.0",
                                "rife-v3.1",
                                "rife-v4",
                                "rife-v4.6",
                                "rife-v4.13-lite",
                                "rife-v4.14",
                            ],
                            value="rife-v2.3",
                            label=webui_language["tile"]["model"],
                        )
                    tiled_upscale_output_image = gr.Image()
                    tiled_upscale_generate_button.click(
                        tile_upscale,
                        inputs=[
                            tiled_upscale_image,
                            tiled_upscale_img_path,
                            tiled_upscale_positive_input,
                            tiled_upscale_negative_input,
                            tiled_upscale_strength,
                            tiled_upscale_engine,
                        ],
                        outputs=tiled_upscale_output_image,
                    )
            # ---------- 图生图插件 ---------- #
            image2image_plugins = load_plugins(Path("./plugins/i2i"))
            for plugin_name, plugin_module in image2image_plugins.items():
                if hasattr(plugin_module, "plugin"):
                    plugin_module.plugin()
                    logger.success(f"成功加载插件: {plugin_name}")
                else:
                    logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
        # ---------- 局部重绘 ---------- #
        with gr.Tab(webui_language["inpaint"]["tab"]):
            with gr.Tab(webui_language["inpaint"]["tab"]):
                with gr.Row():
                    with gr.Column(scale=8):
                        gr.Markdown(webui_language["inpaint"]["description"])
                    open_output_folder_block("inpaint")
                with gr.Column():
                    with gr.Column():
                        inpaint_positive_input = gr.Textbox(
                            value=default_positive_input,
                            lines=2,
                            label=webui_language["t2i"]["positive"],
                        )
                        with gr.Row():
                            inpaint_negative_input = gr.Textbox(
                                value=default_negative_input,
                                lines=3,
                                label=webui_language["t2i"]["negative"],
                                scale=3,
                            )
                            inpaint_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"], scale=1)
                    with gr.Tab("生成参数"):
                        with gr.Row():
                            inpaint_input_path = gr.Textbox(
                                value="", label=webui_language["inpaint"]["input_path"], scale=5
                            )
                            inpaint_mask_path = gr.Textbox(
                                value="", label=webui_language["inpaint"]["mask_path"], scale=5
                            )
                            inpaint_batch_switch = gr.Radio(
                                [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                            )
                        with gr.Row():
                            inpaint_input_image = gr.Sketchpad(
                                sources=["upload", "clipboard", "webcam"],
                                type="pil",
                                label=webui_language["inpaint"]["inpaint_img"],
                            )
                            inpaint_input_image.change(
                                update_image_size, inputs=inpaint_input_image, outputs=inpaint_input_image
                            )
                            with gr.Column():
                                inpaint_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                                inpaint_output_image = gr.Image()
                        with gr.Column():
                            with gr.Row():
                                inpaint_resolution = gr.Dropdown(
                                    RESOLUTION,
                                    value=(
                                        "832x1216"
                                        if env.img_size == -1
                                        else "{}x{}".format((env.img_size)[0], (env.img_size)[1])
                                    ),
                                    label=webui_language["t2i"]["resolution"],
                                )
                                inpaint_width = gr.Textbox(value="832", label=webui_language["t2i"]["width"])
                                inpaint_height = gr.Textbox(value="1216", label=webui_language["t2i"]["height"])
                                inpaint_resolution.change(
                                    return_resolution,
                                    inpaint_resolution,
                                    outputs=[inpaint_width, inpaint_height],
                                    show_progress="hidden",
                                )
                                inpaint_sampler = gr.Dropdown(
                                    SAMPLER,
                                    value=env.sampler,
                                    label=webui_language["t2i"]["sampler"],
                                )
                                inpaint_noise_schedule = gr.Dropdown(
                                    NOISE_SCHEDULE,
                                    value=env.noise_schedule,
                                    label=webui_language["t2i"]["noise_schedule"],
                                )
                            with gr.Row():
                                inpaint_strength = gr.Slider(
                                    minimum=0,
                                    maximum=1,
                                    value=env.hires_strength,
                                    step=0.1,
                                    label=webui_language["i2i"]["strength"],
                                )
                                inpaint_noise = gr.Slider(
                                    minimum=0,
                                    maximum=1,
                                    value=env.hires_noise,
                                    step=0.1,
                                    label=webui_language["i2i"]["noise"],
                                )
                                inpaint_scale = gr.Slider(
                                    minimum=0,
                                    maximum=10,
                                    value=env.scale,
                                    step=0.1,
                                    label=webui_language["t2i"]["scale"],
                                )
                                inpaint_steps = gr.Slider(
                                    minimum=0, maximum=50, value=env.steps, step=1, label=webui_language["t2i"]["steps"]
                                )
                            with gr.Row():
                                with gr.Column():
                                    inpaint_sm = gr.Checkbox(value=env.sm, label="sm", scale=2)
                                    inpaint_sm_dyn = gr.Checkbox(
                                        value=env.sm_dyn, label=webui_language["t2i"]["smdyn"], scale=2
                                    )
                                with gr.Column():
                                    inpaint_variety = gr.Checkbox(value=env.variety, label="variety")
                                    inpaint_decrisp = gr.Checkbox(value=env.decrisp, label="decrisp")
                                with gr.Column(scale=1):
                                    inpaint_seed = gr.Textbox(
                                        value=str(env.seed), label=webui_language["t2i"]["seed"], scale=7
                                    )
                                    inpaint_random_button = gr.Button(value="♻️", size="sm", scale=1)
                                    inpaint_random_button.click(return_random, inputs=None, outputs=inpaint_seed)
                    with gr.Tab("wildcards"):
                        with gr.Row():
                            inpaint_wildcard_file = gr.Dropdown(
                                choices=FAVORTES_FILE,
                                label="wildcard文件",
                            )
                            inpaint_wildcard_name = gr.Dropdown(label="名称")
                            inpaint_wildcard_file.change(
                                update_name_to_dropdown_list,
                                inputs=inpaint_wildcard_file,
                                outputs=inpaint_wildcard_name,
                            )
                            inpaint_add_wildcard_button = gr.Button("添加到文本框")
                            inpaint_add_wildcard_button.click(
                                add_wildcard_to_textbox,
                                inputs=[
                                    inpaint_positive_input,
                                    inpaint_negative_input,
                                    inpaint_wildcard_file,
                                    inpaint_wildcard_name,
                                ],
                                outputs=[inpaint_positive_input, inpaint_negative_input],
                            )
                        inpaint_wildcard_tag = gr.Textbox(label="tag")
                        inpaint_wildcard_name.change(
                            return_wildcard_tag,
                            inputs=[inpaint_wildcard_file, inpaint_wildcard_name],
                            outputs=inpaint_wildcard_tag,
                        )
                inpaint_generate_button.click(
                    fn=inpaint,
                    inputs=[
                        inpaint_input_path,
                        inpaint_mask_path,
                        inpaint_input_image,
                        inpaint_batch_switch,
                        inpaint_positive_input,
                        inpaint_negative_input,
                        inpaint_width,
                        inpaint_height,
                        inpaint_sampler,
                        inpaint_noise_schedule,
                        inpaint_strength,
                        inpaint_noise,
                        inpaint_scale,
                        inpaint_steps,
                        inpaint_sm,
                        inpaint_sm_dyn,
                        inpaint_variety,
                        inpaint_decrisp,
                        inpaint_seed,
                    ],
                    outputs=[inpaint_output_image, inpaint_output_information],
                )
            # ---------- Inpaint插件 ---------- #
            inpaint_plugins = load_plugins(Path("./plugins/inpaint"))
            for plugin_name, plugin_module in inpaint_plugins.items():
                if hasattr(plugin_module, "plugin"):
                    plugin_module.plugin()
                    logger.success(f"成功加载插件: {plugin_name}")
                else:
                    logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
        # ---------- NAI工具箱 ---------- #
        with gr.Tab(webui_language["director_tools"]["title"]):
            gr.Markdown(webui_language["director_tools"]["description"])
            with gr.Tab(webui_language["director_tools"]["remove_bg"]):
                director_tools_remove_bg_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_remove_bg_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_remove_bg_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_remove_bg_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_remove_bg_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_remove_bg_output_masked = gr.Image(
                            label=webui_language["director_tools"]["masked"]
                        )
                        director_tools_remove_bg_output_generated = gr.Image(
                            label=webui_language["director_tools"]["generated"]
                        )
                        director_tools_remove_bg_output_blend = gr.Image(
                            label=webui_language["director_tools"]["blend"]
                        )
                director_tools_remove_bg_generate_button.click(
                    fn=director_tools_remove_bg,
                    inputs=[
                        director_tools_remove_bg_image_path,
                        director_tools_remove_bg_batch_switch,
                        director_tools_remove_bg_image,
                    ],
                    outputs=[
                        director_tools_remove_bg_output_masked,
                        director_tools_remove_bg_output_generated,
                        director_tools_remove_bg_output_blend,
                        director_tools_remove_bg_output_information,
                    ],
                )
            with gr.Tab(webui_language["director_tools"]["line_art"]):
                director_tools_lineart_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_lineart_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_lineart_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_lineart_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_lineart_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_lineart_output_image = gr.Image()
                director_tools_lineart_generate_button.click(
                    fn=director_tools_line_art,
                    inputs=[
                        director_tools_lineart_image_path,
                        director_tools_lineart_batch_switch,
                        director_tools_lineart_image,
                    ],
                    outputs=[
                        director_tools_lineart_output_image,
                        director_tools_lineart_output_information,
                    ],
                )
            with gr.Tab(webui_language["director_tools"]["sketch"]):
                director_tools_sketch_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_sketch_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_sketch_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_sketch_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_sketch_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_sketch_output_image = gr.Image()
                director_tools_sketch_generate_button.click(
                    fn=director_tools_sketch,
                    inputs=[
                        director_tools_sketch_image_path,
                        director_tools_sketch_batch_switch,
                        director_tools_sketch_image,
                    ],
                    outputs=[
                        director_tools_sketch_output_image,
                        director_tools_sketch_output_information,
                    ],
                )
            with gr.Tab(webui_language["director_tools"]["colorize"]):
                director_tools_colorize_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_colorize_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_colorize_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_colorize_defry = gr.Slider(
                        0, 5, 0, step=1, label=webui_language["director_tools"]["defry"]
                    )
                    director_tools_colorize_prompt = gr.Textbox(label=webui_language["director_tools"]["prompt"])
                with gr.Row():
                    director_tools_colorize_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_colorize_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_colorize_output_image = gr.Image()
                director_tools_colorize_generate_button.click(
                    fn=director_tools_colorize,
                    inputs=[
                        director_tools_colorize_defry,
                        director_tools_colorize_prompt,
                        director_tools_colorize_image,
                        director_tools_colorize_image_path,
                        director_tools_colorize_batch_switch,
                    ],
                    outputs=[director_tools_colorize_output_image, director_tools_colorize_output_information],
                )
            with gr.Tab(webui_language["director_tools"]["emotion"]):
                director_tools_emotion_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_emotion_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_emotion_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_emotion_emotion = gr.Dropdown(
                        [
                            "Neutral",
                            "Happy",
                            "Sad",
                            "Angry",
                            "Scared",
                            "Surprised",
                            "Tired",
                            "Excited",
                            "Nervous",
                            "Thinking",
                            "Confused",
                            "Shy",
                            "Disgusted",
                            "Smug",
                            "Bored",
                            "Laughing",
                            "Irritated",
                            "Aroused",
                            "Embarrassed",
                            "Worried",
                            "Love",
                            "Determined",
                            "Hurt",
                            "Playful",
                        ],
                        value="Neutral",
                        label=webui_language["director_tools"]["emotion"],
                        scale=1,
                    )
                    director_tools_emotion_defry = gr.Dropdown(
                        ["Normal", "Slightly Weak", "Weak", "Even Weaker", "Very Weak", "Weakest"],
                        value="Normal",
                        label=webui_language["director_tools"]["defry"],
                        scale=1,
                    )
                    director_tools_emotion_prompt = gr.Textbox(
                        label=webui_language["director_tools"]["prompt"], scale=2
                    )
                with gr.Row():
                    director_tools_emotion_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_emotion_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_emotion_output_image = gr.Image()
                director_tools_emotion_generate_button.click(
                    fn=director_tools_emotion,
                    inputs=[
                        director_tools_emotion_emotion,
                        director_tools_emotion_defry,
                        director_tools_emotion_prompt,
                        director_tools_emotion_image,
                        director_tools_emotion_image_path,
                        director_tools_emotion_batch_switch,
                    ],
                    outputs=[director_tools_emotion_output_image, director_tools_emotion_output_information],
                )
            with gr.Tab(webui_language["director_tools"]["declutter"]):
                director_tools_declutter_generate_button = gr.Button(webui_language["t2i"]["generate_button"])
                with gr.Row():
                    director_tools_declutter_image_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                    director_tools_declutter_batch_switch = gr.Checkbox(
                        False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    director_tools_declutter_image = gr.Image(type="pil")
                    with gr.Column():
                        director_tools_declutter_output_information = gr.Textbox(
                            label=webui_language["i2i"]["output_info"]
                        )
                        director_tools_declutter_output_image = gr.Image()
                director_tools_declutter_generate_button.click(
                    fn=director_tools_declutter,
                    inputs=[
                        director_tools_declutter_image_path,
                        director_tools_declutter_batch_switch,
                        director_tools_declutter_image,
                    ],
                    outputs=[
                        director_tools_declutter_output_image,
                        director_tools_declutter_output_information,
                    ],
                )
        # ---------- 超分降噪 ---------- #
        with gr.Tab(webui_language["super resolution"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_language["super resolution"]["description"])
                open_output_folder_block("upscale")
            with gr.Tab("waifu2x-nv"):
                waifu2x_nv_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        waifu2x_nv_noise = gr.Slider(
                            minimum=-1,
                            maximum=3,
                            value=3,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_noise"],
                            scale=2,
                        )
                        waifu2x_nv_scale = gr.Radio(
                            [1, 2, 4, 8, 16, 32],
                            value=2,
                            label=webui_language["super resolution"]["waifu2x_scale"],
                            scale=2,
                        )
                        waifu2x_nv_tta = gr.Radio(
                            [True, False], value=False, label=webui_language["super resolution"]["tta"]
                        )
                    with gr.Row():
                        waifu2x_nv_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        waifu2x_nv_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        waifu2x_nv_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            waifu2x_nv_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            waifu2x_nv_output_image = gr.Image(scale=2)
                waifu2x_nv_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("waifu2x-ncnn-vulkan", visible=False),
                        waifu2x_nv_input_image,
                        waifu2x_nv_input_path,
                        waifu2x_nv_batch_switch,
                        waifu2x_nv_noise,
                        waifu2x_nv_scale,
                        waifu2x_nv_tta,
                    ],
                    outputs=[waifu2x_nv_output_information, waifu2x_nv_output_image],
                )
            with gr.Tab("Anime4K"):
                anime4k_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    anime4k_zoomFactor = gr.Slider(
                        1, maximum=32, value=2, step=1, label=webui_language["super resolution"]["waifu2x_scale"]
                    )
                    with gr.Row():
                        anime4k_GPUMode = gr.Radio(
                            [True, False], label=webui_language["super resolution"]["gpumode"], value=True
                        )
                        anime4k_CNNMode = gr.Radio(
                            [True, False], label=webui_language["super resolution"]["cnnmode"], value=True
                        )
                        anime4k_HDN = gr.Radio(
                            [True, False], label=webui_language["super resolution"]["hdn"], value=True
                        )
                        anime4k_HDNLevel = gr.Slider(
                            minimum=1, maximum=3, step=1, value=3, label=webui_language["super resolution"]["hdn_level"]
                        )
                    with gr.Row():
                        anime4k_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        anime4k_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        anime4k_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            anime4k_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            anime4k_output_image = gr.Image(scale=2)
                anime4k_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("Anime4K", visible=False),
                        anime4k_input_image,
                        anime4k_input_path,
                        anime4k_batch_switch,
                        anime4k_zoomFactor,
                        anime4k_GPUMode,
                        anime4k_CNNMode,
                        anime4k_HDN,
                        anime4k_HDNLevel,
                    ],
                    outputs=[anime4k_output_information, anime4k_output_image],
                )
            with gr.Tab("realcugan-nv"):
                realcugan_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        realcugan_noise = gr.Slider(
                            minimum=-1,
                            maximum=3,
                            value=3,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_noise"],
                            scale=2,
                        )
                        realcugan_scale = gr.Slider(
                            minimum=1,
                            maximum=4,
                            value=2,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_scale"],
                            scale=2,
                        )
                        realcugan_model = gr.Radio(
                            ["models-se", "models-pro", "models-nose"],
                            value="models-se",
                            label=webui_language["super resolution"]["realcugan_model"],
                            scale=3,
                        )
                    with gr.Row():
                        realcugan_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        realcugan_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        realcugan_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            realcugan_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            realcugan_output_image = gr.Image(scale=2)
                realcugan_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("realcugan-ncnn-vulkan", visible=False),
                        realcugan_input_image,
                        realcugan_input_path,
                        realcugan_batch_switch,
                        realcugan_noise,
                        realcugan_scale,
                        realcugan_model,
                    ],
                    outputs=[realcugan_output_information, realcugan_output_image],
                )
            with gr.Tab("realesrgan-nv"):
                realesrgan_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        with gr.Row():
                            realesrgan_scale = gr.Slider(
                                minimum=2,
                                maximum=4,
                                value=4,
                                step=1,
                                label=webui_language["super resolution"]["waifu2x_scale"],
                                scale=1,
                            )
                            realesrgan_tta = gr.Radio(
                                [True, False], value=True, label=webui_language["super resolution"]["tta"]
                            )
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
                            label=webui_language["super resolution"]["realcugan_model"],
                            scale=3,
                        )
                    with gr.Row():
                        realesrgan_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        realesrgan_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        realesrgan_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            realesrgan_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            realesrgan_output_image = gr.Image(scale=2)
                realesrgan_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("realesrgan-ncnn-vulkan", visible=False),
                        realesrgan_input_image,
                        realesrgan_input_path,
                        realesrgan_batch_switch,
                        realesrgan_scale,
                        realesrgan_model,
                        realesrgan_tta,
                    ],
                    outputs=[realesrgan_output_information, realesrgan_output_image],
                )
            with gr.Tab("realsr-nv"):
                realsr_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        realsr_model = gr.Radio(
                            ["models-DF2K_JPEG", "models-DF2K"],
                            value="models-DF2K_JPEG",
                            label=webui_language["super resolution"]["realcugan_model"],
                        )
                        realsr_tta = gr.Radio(
                            [True, False], value=True, label=webui_language["super resolution"]["tta"]
                        )
                    with gr.Row():
                        realsr_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        realsr_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        realsr_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            realsr_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            realsr_output_image = gr.Image(scale=2)
                realsr_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("realsr-ncnn-vulkan", visible=False),
                        realsr_input_image,
                        realsr_input_path,
                        realsr_batch_switch,
                        realsr_model,
                        realsr_tta,
                    ],
                    outputs=[realsr_output_information, realsr_output_image],
                )
            with gr.Tab("srmd-cuda"):
                srmd_cuda_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        srmd_cuda_noise = gr.Slider(
                            minimum=-1,
                            maximum=10,
                            value=3,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_noise"],
                            scale=3,
                        )
                        srmd_cuda_scale = gr.Radio(
                            [2, 3, 4], value=2, label=webui_language["super resolution"]["waifu2x_scale"], scale=1
                        )
                    with gr.Row():
                        srmd_cuda_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        srmd_cuda_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        srmd_cuda_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            srmd_cuda_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            srmd_cuda_output_image = gr.Image(scale=2)
                srmd_cuda_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("srmd-cuda", visible=False),
                        srmd_cuda_input_image,
                        srmd_cuda_input_path,
                        srmd_cuda_batch_switch,
                        srmd_cuda_noise,
                        srmd_cuda_scale,
                    ],
                    outputs=[srmd_cuda_output_information, srmd_cuda_output_image],
                )
            with gr.Tab("srmd-nv"):
                srmd_nv_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Column():
                    with gr.Row():
                        srmd_nv_noise = gr.Slider(
                            minimum=-1,
                            maximum=10,
                            value=3,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_noise"],
                            scale=2,
                        )
                        srmd_nv_scale = gr.Slider(
                            minimum=2,
                            maximum=4,
                            value=2,
                            step=1,
                            label=webui_language["super resolution"]["waifu2x_scale"],
                            scale=2,
                        )
                        srmd_nv_tta = gr.Radio(
                            [True, False], value=True, label=webui_language["super resolution"]["tta"], scale=1
                        )
                    with gr.Row():
                        srmd_nv_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                        srmd_nv_batch_switch = gr.Radio(
                            [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                        )
                    with gr.Row():
                        srmd_nv_input_image = gr.Image(type="pil", scale=1)
                        with gr.Column(scale=2):
                            srmd_nv_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                            srmd_nv_output_image = gr.Image(scale=2)
                srmd_nv_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("srmd-ncnn-vulkan", visible=False),
                        srmd_nv_input_image,
                        srmd_nv_input_path,
                        srmd_nv_batch_switch,
                        srmd_nv_noise,
                        srmd_nv_scale,
                        srmd_nv_tta,
                    ],
                    outputs=[srmd_nv_output_information, srmd_nv_output_image],
                )
            with gr.Tab("waifu2x-caffe"):
                waifu2x_caffe_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Row():
                    waifu2x_caffe_mode = gr.Radio(
                        ["noise", "scale", "noise_scale"],
                        value="noise_scale",
                        label=webui_language["super resolution"]["mode"],
                        scale=4,
                    )
                    waifu2x_caffe_scale = gr.Slider(
                        minimum=1,
                        maximum=32,
                        value=2,
                        label=webui_language["super resolution"]["waifu2x_scale"],
                        scale=1,
                    )
                    waifu2x_caffe_noise = gr.Slider(
                        minimum=0,
                        maximum=3,
                        step=1,
                        value=3,
                        label=webui_language["super resolution"]["waifu2x_noise"],
                        scale=1,
                    )
                    waifu2x_caffe_process = gr.Radio(
                        ["cpu", "gpu", "cudnn"],
                        value="gpu",
                        label=webui_language["super resolution"]["process"],
                        scale=3,
                    )
                    waifu2x_caffe_tta = gr.Radio(
                        [True, False], value=False, label=webui_language["super resolution"]["tta"], scale=2
                    )
                waifu2x_caffe_model = gr.Radio(
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
                    label=webui_language["super resolution"]["realcugan_model"],
                )
                with gr.Row():
                    waifu2x_caffe_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                    waifu2x_caffe_batch_switch = gr.Radio(
                        [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    waifu2x_caffe_input_image = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        waifu2x_caffe_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                        waifu2x_caffe_output_image = gr.Image(scale=2)
                waifu2x_caffe_generate_button.click(
                    fn=upscale,
                    inputs=[
                        gr.Textbox("waifu2x-caffe", visible=False),
                        waifu2x_caffe_input_image,
                        waifu2x_caffe_input_path,
                        waifu2x_caffe_batch_switch,
                        waifu2x_caffe_mode,
                        waifu2x_caffe_scale,
                        waifu2x_caffe_noise,
                        waifu2x_caffe_process,
                        waifu2x_caffe_tta,
                        waifu2x_caffe_model,
                    ],
                    outputs=[waifu2x_caffe_output_information, waifu2x_caffe_output_image],
                )
            with gr.Tab("waifu2x-converter"):
                waifu2x_converter_generate_button = gr.Button(value=webui_language["t2i"]["generate_button"])
                with gr.Row():
                    waifu2x_converter_mode = gr.Radio(
                        ["noise", "scale", "noise-scale"],
                        value="noise-scale",
                        label=webui_language["super resolution"]["mode"],
                        scale=3,
                    )
                    waifu2x_converter_scale = gr.Slider(
                        minimum=1,
                        maximum=32,
                        step=1,
                        value=2,
                        label=webui_language["super resolution"]["waifu2x_scale"],
                        scale=2,
                    )
                    waifu2x_converter_noise = gr.Slider(
                        minimum=0,
                        maximum=3,
                        step=1,
                        value=3,
                        label=webui_language["super resolution"]["waifu2x_noise"],
                        scale=2,
                    )
                    waifu2x_converter_jobs = gr.Slider(
                        1, maximum=10, value=5, step=1, label=webui_language["super resolution"]["jobs"], scale=2
                    )
                with gr.Row():
                    waifu2x_converter_input_path = gr.Textbox(
                        value="", label=webui_language["i2i"]["input_path"], scale=5
                    )
                    waifu2x_converter_batch_switch = gr.Radio(
                        [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    waifu2x_converter_input_image = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        waifu2x_converter_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                        waifu2x_converter_output_image = gr.Image(scale=2)
            waifu2x_converter_generate_button.click(
                fn=upscale,
                inputs=[
                    gr.Textbox("waifu2x-converter", visible=False),
                    waifu2x_converter_input_image,
                    waifu2x_converter_input_path,
                    waifu2x_converter_batch_switch,
                    waifu2x_converter_scale,
                    waifu2x_converter_noise,
                    waifu2x_converter_mode,
                    waifu2x_converter_jobs,
                ],
                outputs=[waifu2x_converter_output_information, waifu2x_converter_output_image],
            )
        # ---------- 自动打码 ---------- #
        with gr.Tab(webui_language["mosaic"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_language["mosaic"]["description"])
                open_output_folder_block("mosaic")
            with gr.Row():
                mosaic_generate_button_pixel = gr.Button(value=webui_language["mosaic"]["mosaic_generate_button_pixel"])
                mosaic_generate_button_blurry = gr.Button(
                    value=webui_language["mosaic"]["mosaic_generate_button_blurry"]
                )
                mosaic_generate_button_lines = gr.Button(value=webui_language["mosaic"]["mosaic_generate_button_lines"])
            with gr.Column():
                with gr.Row():
                    mosaic_input_path = gr.Textbox(value="", label=webui_language["i2i"]["input_path"], scale=5)
                    mosaic_batch_switch = gr.Radio(
                        [True, False], value=False, label=webui_language["i2i"]["open_button"], scale=1
                    )
                with gr.Row():
                    mosaic_input_image = gr.Image(type="pil", scale=1)
                    with gr.Column(scale=2):
                        mosaic_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                        mosaic_output_image = gr.Image(scale=2)
            gr.Markdown(webui_language["mosaic"]["yolo"])
            gr.Markdown("`\n.\\venv\\Scripts\\activate`\n\n`pip install ultralytics==8.2.50`")
            gr.Markdown(
                """整合包用户(For Modpack):\n\n```.\\Python310\\python.exe -s -m pip install ultralytics==8.2.50```"""
            )
            mosaic_generate_button_pixel.click(
                fn=mosaic,
                inputs=[mosaic_input_path, mosaic_input_image, mosaic_batch_switch, gr.Textbox("pixel", visible=False)],
                outputs=[mosaic_output_image, mosaic_output_information],
            )
            mosaic_generate_button_blurry.click(
                fn=mosaic,
                inputs=[
                    mosaic_input_path,
                    mosaic_input_image,
                    mosaic_batch_switch,
                    gr.Textbox("blurry", visible=False),
                ],
                outputs=[mosaic_output_image, mosaic_output_information],
            )
            mosaic_generate_button_lines.click(
                fn=mosaic,
                inputs=[mosaic_input_path, mosaic_input_image, mosaic_batch_switch, gr.Textbox("lines", visible=False)],
                outputs=[mosaic_output_image, mosaic_output_information],
            )
        # ---------- 添加水印 ---------- #
        with gr.Tab(webui_language["water mark"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_language["water mark"]["description"])
                open_output_folder_block("water")
            with gr.Row():
                watermark_input_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=4)
                watermark_generate_button = gr.Button(webui_language["water mark"]["generate_button"], scale=1)
            watermark_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
            watermark_generate_button.click(
                fn=water,
                inputs=[watermark_input_path, gr.Textbox("./output/water", visible=False)],
                outputs=watermark_output_information,
            )
        # ---------- 上传 Pixiv ---------- #
        with gr.Tab(webui_language["pixiv"]["tab"]):
            gr.Markdown(webui_language["pixiv"]["description"])
            with gr.Column():
                pixiv_input_path = gr.Textbox(label=webui_language["i2i"]["input_path"])
                with gr.Row():
                    pixiv_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"], scale=4)
                    pixiv_generate_button = gr.Button(webui_language["water mark"]["generate_button"], scale=1)
            pixiv_generate_button.click(fn=pixiv, inputs=pixiv_input_path, outputs=pixiv_output_information)
        # ---------- 图片筛选 ---------- #
        with gr.Tab(webui_language["selector"]["tab"]):
            gr.Markdown(webui_language["selector"]["description"])
            with gr.Column():
                with gr.Row():
                    selector_input_path = gr.Textbox(label=webui_language["selector"]["input_path"], scale=4)
                    selector_select_button = gr.Button(webui_language["selector"]["select_button"], scale=1)
                with gr.Row():
                    selector_output_path = gr.Textbox(label=webui_language["selector"]["output_path"])
                    _selector_output_path = gr.Textbox(label=webui_language["selector"]["output_path_"])
            with gr.Row():
                selector_output_image = gr.Gallery(scale=7, preview=True, label="Image", height=env.height + 120)
                with gr.Column(scale=1):
                    selector_next_button = gr.Button(
                        webui_language["selector"]["next_button"], size="lg", elem_id="arrow_down"
                    )
                    selector_move_button = gr.Button(
                        webui_language["selector"]["move_button"], size="lg", elem_id="arrow_left"
                    )
                    _selector_move_button = gr.Button(
                        webui_language["selector"]["move_button_"], size="lg", elem_id="arrow_right"
                    )
                    selector_copy_button = gr.Button(webui_language["selector"]["copy_button"], size="lg")
                    _selector_copy_button = gr.Button(webui_language["selector"]["copy_button_"], size="lg")
                    selector_delete_button = gr.Button(
                        webui_language["selector"]["del_button"], size="lg", elem_id="arrow_up"
                    )
            selector_current_img = gr.Textbox(visible=False)
            selector_select_button.click(
                fn=show_first_img, inputs=[selector_input_path], outputs=[selector_output_image, selector_current_img]
            )
            selector_next_button.click(fn=show_next_img, outputs=[selector_output_image, selector_current_img])
            selector_move_button.click(
                fn=move_current_img,
                inputs=[selector_current_img, selector_output_path],
                outputs=[selector_output_image, selector_current_img],
            )
            _selector_move_button.click(
                fn=move_current_img,
                inputs=[selector_current_img, _selector_output_path],
                outputs=[selector_output_image, selector_current_img],
            )
            selector_copy_button.click(
                fn=copy_current_img,
                inputs=[selector_current_img, selector_output_path],
                outputs=[selector_output_image, selector_current_img],
            )
            _selector_copy_button.click(
                fn=copy_current_img,
                inputs=[selector_current_img, _selector_output_path],
                outputs=[selector_output_image, selector_current_img],
            )
            selector_delete_button.click(
                fn=del_current_img, inputs=[selector_current_img], outputs=[selector_output_image, selector_current_img]
            )
        # ---------- 抹除数据 ---------- #
        with gr.Tab(webui_language["rm png info"]["tab"]):
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown(webui_language["rm png info"]["description"])
            with gr.Tab(webui_language["rm png info"]["tab_rm"]):
                with gr.Row():
                    remove_pnginfo_image = gr.Image(type="filepath")
                    with gr.Column():
                        remove_pnginfo_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                        with gr.Row():
                            remove_pnginfo_choices = gr.CheckboxGroup(
                                ["Title", "Description", "Software", "Source", "Generation time", "Comment", "dpi"],
                                value=[
                                    "Title",
                                    "Description",
                                    "Software",
                                    "Source",
                                    "Generation time",
                                    "Comment",
                                    "dpi",
                                ],
                                label=webui_language["rm png info"]["choose_to_rm"],
                                scale=2,
                            )
                            remove_pnginfo_data_cloaking_switch = gr.Checkbox(
                                False,
                                label=webui_language["rm png info"]["remove_pnginfo_data_cloaking_switch"],
                                scale=1,
                            )
                        remove_pnginfo_metadate = gr.Textbox(
                            env.meta_data, label=webui_language["rm png info"]["remove_pnginfo_metadate"]
                        )
                        remove_pnginfo_input_path = gr.Textbox(label=webui_language["i2i"]["input_path"])
                        remove_pnginfo_output_path = gr.Textbox(label=webui_language["rm png info"]["save_path"])
                        remove_pnginfo_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                        remove_pnginfo_generate_button.click(
                            fn=remove_info,
                            inputs=[
                                remove_pnginfo_image,
                                remove_pnginfo_input_path,
                                remove_pnginfo_output_path,
                                remove_pnginfo_choices,
                                remove_pnginfo_metadate,
                                remove_pnginfo_data_cloaking_switch,
                            ],
                            outputs=[remove_pnginfo_output_information],
                        )
            with gr.Tab(webui_language["rm png info"]["tab_re"]):
                revert_pnginfo_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                revert_pnginfo_info_file_path = gr.Textbox(label=webui_language["rm png info"]["info_file_path"])
                revert_pnginfo_input_path = gr.Textbox(label=webui_language["rm png info"]["input_path"])
                revert_pnginfo_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                revert_pnginfo_generate_button.click(
                    fn=revert_info,
                    inputs=[revert_pnginfo_info_file_path, revert_pnginfo_input_path],
                    outputs=[revert_pnginfo_output_information],
                )
            with gr.Tab(webui_language["rm png info"]["tab_ex"]):
                export_pnginfo_generate_button = gr.Button(webui_language["water mark"]["generate_button"])
                export_pnginfo_input_path = gr.Textbox(label=webui_language["i2i"]["input_path"])
                export_pnginfo_output_path = gr.Textbox(label=webui_language["rm png info"]["save_path"])
                export_pnginfo_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                export_pnginfo_generate_button.click(
                    fn=export_info,
                    inputs=[export_pnginfo_input_path, export_pnginfo_output_path],
                    outputs=export_pnginfo_output_information,
                )
        # ---------- 法术解析 ---------- #
        with gr.Tab(webui_language["maigic analysis"]["tab"]):
            with gr.Tab(webui_language["maigic analysis"]["tab"]):
                with gr.Row():
                    with gr.Column():
                        pnginfo_image = gr.Image(type="pil", image_mode="RGBA")
                        pnginfo_send2text2image_button = gr.Button(
                            webui_language["maigic analysis"]["pnginfo_send2text2image_button"]
                        )
                        pnginfo_send2image2image_button = gr.Button(
                            webui_language["maigic analysis"]["pnginfo_send2image2image_button"]
                        )
                        pnginfo_send2inpaint_button = gr.Button(
                            webui_language["maigic analysis"]["pnginfo_send2inpaint_button"]
                        )
                    with gr.Column():
                        pnginfo_positive_input = gr.Textbox(label="正面提示词(Positive Prompt)")
                        pnginfo_negative_input = gr.Textbox(label="负面提示词(Negative Prompt)")
                        with gr.Row():
                            pnginfo_width = gr.Textbox(label="宽(Width)")
                            pnginfo_height = gr.Textbox(label="高(Height)")
                        pnginfo_steps = gr.Slider(0, 50, step=1, label="采样步数(Steps)")
                        pnginfo_scale = gr.Slider(0, 10, step=0.1, label="提示词相关性(Scale)")
                        with gr.Row():
                            pnginfo_noise_schedule = gr.Dropdown(
                                choices=NOISE_SCHEDULE, label="噪声计划表(Noise Schedule)"
                            )
                            pnginfo_sampler = gr.Dropdown(choices=SAMPLER, label="采样器(Sampler)")
                        with gr.Row():
                            pnginfo_sm = gr.Checkbox(label="sm")
                            pnginfo_sm_dyn = gr.Checkbox(label="sm_dyn")
                        with gr.Row():
                            pnginfo_variety = gr.Checkbox(label="variety")
                            pnginfo_decrisp = gr.Checkbox(label="decrisp")
                        pnginfo_seed = gr.Textbox(label="种子(Seed)")
                pnginfo_pnginfo = gr.Textbox(label="Png Info")
                pnginfo_image.change(
                    return_pnginfo,
                    inputs=pnginfo_image,
                    outputs=[
                        pnginfo_positive_input,
                        pnginfo_negative_input,
                        pnginfo_width,
                        pnginfo_height,
                        pnginfo_steps,
                        pnginfo_scale,
                        pnginfo_noise_schedule,
                        pnginfo_sampler,
                        pnginfo_sm,
                        pnginfo_sm_dyn,
                        pnginfo_variety,
                        pnginfo_decrisp,
                        pnginfo_seed,
                        pnginfo_pnginfo,
                    ],
                )
                pnginfo_send2text2image_button.click(
                    _return_pnginfo,
                    inputs=[
                        pnginfo_positive_input,
                        pnginfo_negative_input,
                        pnginfo_width,
                        pnginfo_height,
                        pnginfo_steps,
                        pnginfo_scale,
                        pnginfo_noise_schedule,
                        pnginfo_sampler,
                        pnginfo_sm,
                        pnginfo_sm_dyn,
                        pnginfo_variety,
                        pnginfo_decrisp,
                        pnginfo_seed,
                    ],
                    outputs=[
                        text2image_positive_input,
                        text2image_negative_input,
                        text2image_width,
                        text2image_height,
                        text2image_steps,
                        text2image_scale,
                        text2image_noise_schedule,
                        text2image_sampler,
                        text2image_sm,
                        text2image_sm_dyn,
                        text2image_variety,
                        text2image_decrisp,
                        text2image_seed,
                    ],
                )
                pnginfo_send2image2image_button.click(
                    _return_pnginfo,
                    inputs=[
                        pnginfo_positive_input,
                        pnginfo_negative_input,
                        pnginfo_width,
                        pnginfo_height,
                        pnginfo_steps,
                        pnginfo_scale,
                        pnginfo_noise_schedule,
                        pnginfo_sampler,
                        pnginfo_sm,
                        pnginfo_sm_dyn,
                        pnginfo_variety,
                        pnginfo_decrisp,
                        pnginfo_seed,
                        pnginfo_image,
                    ],
                    outputs=[
                        image2image_positive_input,
                        image2image_negative_input,
                        image2image_width,
                        image2image_height,
                        image2image_steps,
                        image2image_scale,
                        image2image_noise_schedule,
                        image2image_sampler,
                        image2image_sm,
                        image2image_sm_dyn,
                        image2image_variety,
                        image2image_decrisp,
                        image2image_seed,
                        image2image_input_image,
                    ],
                )
                pnginfo_send2inpaint_button.click(
                    _return_pnginfo,
                    inputs=[
                        pnginfo_positive_input,
                        pnginfo_negative_input,
                        pnginfo_width,
                        pnginfo_height,
                        pnginfo_steps,
                        pnginfo_scale,
                        pnginfo_noise_schedule,
                        pnginfo_sampler,
                        pnginfo_sm,
                        pnginfo_sm_dyn,
                        pnginfo_variety,
                        pnginfo_decrisp,
                        pnginfo_seed,
                        pnginfo_image,
                    ],
                    outputs=[
                        inpaint_positive_input,
                        inpaint_negative_input,
                        inpaint_width,
                        inpaint_height,
                        inpaint_steps,
                        inpaint_scale,
                        inpaint_noise_schedule,
                        inpaint_sampler,
                        inpaint_sm,
                        inpaint_sm_dyn,
                        inpaint_variety,
                        inpaint_decrisp,
                        inpaint_seed,
                        inpaint_input_image,
                    ],
                )
            with gr.Tab("Tagger"):
                with gr.Row():
                    with gr.Column():
                        tagger_input_image = gr.Image(type="pil", image_mode="RGBA")
                        with gr.Row():
                            tagger_path = gr.Textbox(label=webui_language["i2i"]["input_path"], scale=3)
                            tagger_batch_switch = gr.Checkbox(
                                False, label=webui_language["i2i"]["open_button"], scale=1
                            )
                        tagger_model_repo = gr.Dropdown(
                            dropdown_list,
                            value=SWINV2_MODEL_DSV3_REPO,
                            label=webui_language["tagger"]["model_repo"],
                        )
                        with gr.Row():
                            tagger_general_thresh = gr.Slider(
                                0,
                                1,
                                step=0.01,
                                value=0.35,
                                label=webui_language["tagger"]["general_thresh"],
                                scale=3,
                            )
                            tagger_general_mcut_enabled = gr.Checkbox(
                                value=False,
                                label=webui_language["tagger"]["general_mcut_enabled"],
                                scale=1,
                            )
                        with gr.Row():
                            tagger_character_thresh = gr.Slider(
                                0,
                                1,
                                step=0.01,
                                value=0.85,
                                label=webui_language["tagger"]["character_thresh"],
                                scale=3,
                            )
                            tagger_character_mcut_enabled = gr.Checkbox(
                                value=False,
                                label=webui_language["tagger"]["character_mcut_enabled"],
                                scale=1,
                            )
                        with gr.Row():
                            tagger_clear = gr.ClearButton(
                                components=[
                                    tagger_input_image,
                                    tagger_model_repo,
                                    tagger_general_thresh,
                                    tagger_general_mcut_enabled,
                                    tagger_character_thresh,
                                    tagger_character_mcut_enabled,
                                ],
                                size="lg",
                            )
                            tagger_submit = gr.Button(value=webui_language["tagger"]["submit"], size="lg")
                    with gr.Column():
                        tagger_sorted_general_strings = gr.Textbox(
                            label=webui_language["tagger"]["sorted_general_strings"]
                        )
                        tagger_rating = gr.Label(label=webui_language["tagger"]["rating"])
                        tagger_character_res = gr.Label(label=webui_language["tagger"]["character_res"])
                        tagger_general_res = gr.Label(label=webui_language["tagger"]["general_res"])
                        tagger_clear.add(
                            [
                                tagger_sorted_general_strings,
                                tagger_rating,
                                tagger_character_res,
                                tagger_general_res,
                            ]
                        )
                tagger_submit.click(
                    tagger,
                    [
                        tagger_input_image,
                        tagger_path,
                        tagger_batch_switch,
                        tagger_model_repo,
                        tagger_general_thresh,
                        tagger_general_mcut_enabled,
                        tagger_character_thresh,
                        tagger_character_mcut_enabled,
                    ],
                    outputs=[tagger_sorted_general_strings, tagger_rating, tagger_character_res, tagger_general_res],
                )
        # ---------- GPT ---------- #
        with gr.Tab("GPT"):
            gr.HTML(
                """
    <iframe id="myiframe" src="http://127.0.0.1:19198"></iframe>
    <style>
        #myiframe {
            width: 100%;
            height: 600px;
        }
    </style>
    """.replace(
                    "600", str(env.height + 50)
                ).replace(
                    "19198", str(env.g4f_port)
                )
            )
        # ---------- WebUI插件 ---------- #
        webui_plugins = load_plugins(Path("./plugins/webui"))
        for plugin_name, plugin_module in webui_plugins.items():
            if hasattr(plugin_module, "plugin"):
                plugin_module.plugin()
                logger.success(f"成功加载插件: {plugin_name}")
            else:
                logger.error(f"插件: {plugin_name} 没有 plugin 函数!")
        # ---------- 插件商店 ---------- #
        with gr.Tab(webui_language["plugin"]["tab"]):
            with gr.Row():
                plugin_store_plugin_name = gr.Textbox("", label="名称(Name)")
                plugin_store_output_information = gr.Textbox(label=webui_language["i2i"]["output_info"])
                plugin_store_install_button = gr.Button("安装/更新(Install/Update)")
                plugin_store_uninstall_button = gr.Button("卸载(Uninstall)")
                plugin_store_restart_button = gr.Button("重启(Restart)")
            gr.Markdown(plugin_list())
            plugin_store_install_button.click(
                install_plugin, inputs=plugin_store_plugin_name, outputs=plugin_store_output_information
            )
            plugin_store_uninstall_button.click(
                uninstall_plugin, inputs=plugin_store_plugin_name, outputs=plugin_store_output_information
            )
            plugin_store_restart_button.click(restart)
        # ---------- 配置设置 ---------- #
        with gr.Tab(webui_language["setting"]["tab"]):
            with gr.Row():
                setting_modify_button = gr.Button("保存(Save)")
                setting_restart_button = gr.Button("重启(Restart)")
            setting_output_information = gr.Textbox(
                value=webui_language["setting"]["description"] if env.share else None,
                label=webui_language["i2i"]["output_info"],
            )
            with gr.Tab(webui_language["setting"]["sub_tab"]["necessary"]):
                token = gr.Textbox(
                    value=env.token,
                    label=webui_language["setting"]["description"]["token"],
                    lines=2,
                    visible=True if not env.share else False,
                )
                gr.Markdown(
                    "获取 Token 的方法(The Way to Get Token): [**自述文件(README)**](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#%EF%B8%8F-%E9%85%8D%E7%BD%AE)"
                )
            with gr.Tab(webui_language["setting"]["sub_tab"]["t2i"]):
                with gr.Column():
                    model = gr.Dropdown(MODEL, value="nai-diffusion-3", label="模型(Model)")
                    img_size = gr.Radio(
                        [
                            -1,
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
                        value=("{}x{}".format((env.img_size)[0], (env.img_size)[1]) if env.img_size != -1 else -1),
                        label=webui_language["setting"]["description"]["img_size"],
                    )
                    sampler = gr.Radio(
                        SAMPLER,
                        value=env.sampler,
                        label=webui_language["setting"]["description"]["sampler"],
                    )
                    noise_schedule = gr.Radio(
                        NOISE_SCHEDULE,
                        value=env.noise_schedule,
                        label=webui_language["setting"]["description"]["noise_schedule"],
                    )
                    with gr.Row():
                        scale = gr.Slider(
                            0, 10, env.scale, step=0.1, label=webui_language["setting"]["description"]["scale"]
                        )
                        steps = gr.Slider(
                            1, 50, env.steps, step=1, label=webui_language["setting"]["description"]["steps"]
                        )
                    with gr.Row():
                        censor = gr.Checkbox(value=env.censor, label=webui_language["setting"]["description"]["censor"])
                        sm = gr.Checkbox(env.sm, label=webui_language["setting"]["description"]["sm"])
                        sm_dyn = gr.Checkbox(env.sm_dyn, label=webui_language["setting"]["description"]["sm_dyn"])
                        variety = gr.Checkbox(env.sm, label=webui_language["setting"]["description"]["sm"])
                        decrisp = gr.Checkbox(env.sm, label=webui_language["setting"]["description"]["sm"])
                    with gr.Row():
                        seed = gr.Textbox(env.seed, label=webui_language["setting"]["description"]["seed"])
                        proxy = gr.Textbox(env.proxy, label=webui_language["setting"]["description"]["proxy"])
                    t2i_cool_time = gr.Slider(
                        6,
                        120,
                        env.t2i_cool_time,
                        step=1,
                        label=webui_language["setting"]["description"]["t2i_cool_time"],
                    )
                    i2i_cool_time = gr.Slider(
                        6,
                        120,
                        env.i2i_cool_time,
                        step=1,
                        label=webui_language["setting"]["description"]["i2i_cool_time"],
                    )
                    magnification = gr.Slider(
                        1,
                        1.5,
                        env.magnification,
                        step=0.1,
                        label=webui_language["setting"]["description"]["magnification"],
                    )
                    hires_strength = gr.Slider(
                        0,
                        1,
                        env.hires_strength,
                        step=0.1,
                        label=webui_language["setting"]["description"]["hires_strength"],
                    )
                    hires_noise = gr.Slider(
                        0,
                        1,
                        env.hires_noise,
                        step=0.1,
                        label=webui_language["setting"]["description"]["hires_noise"],
                    )
                    save_path = gr.Radio(
                        ["默认(Default)", "日期(Date)", "角色(Character)", "出处(Origin)", "画风(Artists)"],
                        value=env.save_path,
                        label=webui_language["setting"]["description"]["save_path"],
                    )
            with gr.Tab(webui_language["setting"]["sub_tab"]["pixiv"]):
                pixiv_cookie = gr.Textbox(
                    value=env.pixiv_cookie,
                    label=webui_language["setting"]["description"]["pixiv_cookie"],
                    lines=7,
                    visible=True if not env.share else False,
                )
                pixiv_token = gr.Textbox(
                    value=env.pixiv_token,
                    label=webui_language["setting"]["description"]["pixiv_token"],
                    visible=True if not env.share else False,
                )
                allow_tag_edit = gr.Checkbox(
                    env.allow_tag_edit, label=webui_language["setting"]["description"]["allow_tag_edit"]
                )
                caption_prefix = gr.Textbox(
                    value=str(env.caption_prefix).replace("\n", "\\n"),
                    label=webui_language["setting"]["description"]["caption_prefix"],
                    lines=3,
                )
                rep_tags = gr.Checkbox(env.rep_tags, label=webui_language["setting"]["description"]["rep_tags"])
                rep_tags_per = gr.Slider(
                    0, 1, env.rep_tags_per, step=0.1, label=webui_language["setting"]["description"]["rep_tags_per"]
                )
                rep_tags_with_tag = gr.Textbox(
                    value=env.rep_tags_with_tag, label=webui_language["setting"]["description"]["rep_tags_with_tag"]
                )
                pixiv_cool_time = gr.Slider(
                    10,
                    360,
                    env.pixiv_cool_time,
                    step=1,
                    label=webui_language["setting"]["description"]["pixiv_cool_time"],
                )
                _remove_info = gr.Checkbox(True, label=webui_language["setting"]["description"]["remove_info"])
                r18 = gr.Checkbox(env.r18, label=webui_language["setting"]["description"]["r18"])
                default_tag = gr.Textbox(
                    value=str(list_to_str(env.default_tag)),
                    label=webui_language["setting"]["description"]["default_tag"],
                )
            with gr.Tab(webui_language["setting"]["sub_tab"]["mosaic"]):
                neighbor = gr.Slider(
                    0, 0.25, env.neighbor, step=0.0001, label=webui_language["setting"]["description"]["neighbor"]
                )
            with gr.Tab(webui_language["setting"]["sub_tab"]["eraser"]):
                meta_data = gr.Textbox(value=env.meta_data, label=webui_language["setting"]["description"]["meta_data"])
                revert_info_ = gr.Radio(
                    choices=[True, False],
                    value=env.revert_info,
                    label=webui_language["setting"]["description"]["revert_info_"],
                )
            with gr.Tab(webui_language["setting"]["sub_tab"]["water"]):
                alpha = gr.Slider(0, 1, env.alpha, label=webui_language["setting"]["description"]["alpha"])
                water_height = gr.Slider(
                    10, 300, env.water_height, label=webui_language["setting"]["description"]["water_height"]
                )
                water_position = gr.Dropdown(
                    ["左上(Upper Left)", "左下(Lower Left)", "右上(Upper Right)", "右下(Upper Right)"],
                    value=env.position,
                    label=webui_language["setting"]["description"]["position"],
                )
                water_num = gr.Slider(
                    1, 10, env.water_num, step=1, label=webui_language["setting"]["description"]["water_num"]
                )
                rotate = gr.Slider(0, 360, 45, step=1, label=webui_language["setting"]["description"]["rotate"])
            with gr.Tab("WebUI"):
                share = gr.Checkbox(env.share, label=webui_language["setting"]["description"]["share"])
                height = gr.Slider(
                    300, 1200, env.height, step=10, label=webui_language["setting"]["description"]["height"]
                )
                port = gr.Textbox(value=env.port, label=webui_language["setting"]["description"]["port"])
                g4f_port = gr.Textbox(env.g4f_port, label=webui_language["setting"]["description"]["g4f_port"])
                theme = gr.Textbox(env.theme, label=webui_language["setting"]["description"]["theme"])
                webui_lang = gr.Dropdown(
                    ["zh", "en"], value="zh", label=webui_language["setting"]["description"]["webui_lang"]
                )
                skip_update_check = gr.Checkbox(
                    env.skip_update_check, label=webui_language["setting"]["description"]["skip_update_check"]
                )
                skip_start_sound = gr.Checkbox(
                    env.skip_update_check, label=webui_language["setting"]["description"]["skip_start_sound"]
                )
                skip_load_g4f = gr.Checkbox(
                    env.skip_load_g4f, label=webui_language["setting"]["description"]["skip_load_g4f"]
                )
            with gr.Tab("更新 WebUI(Update WebUI)"):
                update_button = gr.Button("更新 WebUI(Update WebUI)")
                output_info = gr.Textbox(label=webui_language["i2i"]["output_info"])
                update_button.click(update, inputs=gr.Textbox("./", visible=False), outputs=output_info)
            setting_modify_button.click(
                setting,
                inputs=[
                    token,
                    model,
                    img_size,
                    scale,
                    censor,
                    sampler,
                    steps,
                    sm,
                    sm_dyn,
                    variety,
                    decrisp,
                    noise_schedule,
                    seed,
                    t2i_cool_time,
                    save_path,
                    proxy,
                    magnification,
                    hires_strength,
                    hires_noise,
                    i2i_cool_time,
                    pixiv_cookie,
                    pixiv_token,
                    allow_tag_edit,
                    caption_prefix,
                    rep_tags,
                    rep_tags_per,
                    rep_tags_with_tag,
                    pixiv_cool_time,
                    _remove_info,
                    r18,
                    default_tag,
                    neighbor,
                    alpha,
                    water_height,
                    water_position,
                    water_num,
                    rotate,
                    meta_data,
                    revert_info_,
                    share,
                    height,
                    port,
                    g4f_port,
                    theme,
                    webui_lang,
                    skip_update_check,
                    skip_start_sound,
                    skip_load_g4f,
                ],
                outputs=setting_output_information,
            )
            setting_restart_button.click(restart)

    sanp.queue().launch(inbrowser=True, share=env.share, server_port=env.port, favicon_path="./files/webui/logo.png")


if __name__ == "__main__":
    if not env.skip_load_g4f:
        p1 = mp.Process(target=g4f)
    p2 = mp.Process(target=main)
    if not env.skip_load_g4f:
        p1.start()
    p2.start()
    if not env.skip_load_g4f:
        p1.join()
    p2.join()
