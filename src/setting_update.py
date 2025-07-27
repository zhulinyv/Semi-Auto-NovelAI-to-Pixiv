from utils.env import env


def modify_env(**kwargs: dict):
    keys = list(kwargs.keys())
    for target_key in keys:
        new_value = kwargs[target_key]
        with open(".env", "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.seek(0)
            setting = f.read()
        if target_key not in setting:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(setting + f"\n{target_key}={new_value}\n")
        else:
            for i, line in enumerate(lines):
                if line.startswith(target_key + "="):
                    lines[i] = f"{target_key}={new_value}\n"
                    break
            with open(".env", "w", encoding="utf-8") as f:
                f.writelines(lines)
    return "修改已保存, 重启后生效!"


def webui(
    token,
    model,
    img_size,
    scale,
    rescale,
    censor,
    sampler,
    steps,
    sm,
    sm_dyn,
    legacy_uc,
    variety,
    decrisp,
    skip_format_str,
    noise_schedule,
    seed,
    t2i_cool_time,
    save_path,
    proxy,
    times_for_scripts,
    skip_save_grid,
    quality_toggle,
    uc_preset,
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
    remove_info,
    r18,
    default_tag,
    suggest_tag,
    use_file_name_as_title,
    use_old_title_rule,
    neighbor,
    water_num,
    meta_data,
    revert_info,
    share,
    height,
    port,
    g4f_port,
    doc_port,
    theme,
    webui_lang,
    skip_update_check,
    skip_start_sound,
    skip_load_g4f,
    skip_finish_sound,
    skip_else_log,
    new_interface,
    num_of_suggest_tag,
):
    if img_size == -1:
        img_size = -1
    else:
        img_size = [int((img_size.split("x"))[0]), int((img_size.split("x"))[1])]
    if env.model == "nai-diffusion-4-5-full":
        uc_preset_data = {"Heavy": 0, "Light": 1, "Furry Focus": 2, "Human Focus": 3, "None": 4}
    elif env.model in ["nai-diffusion-4-5-curated", "nai-diffusion-3"]:
        uc_preset_data = {"Heavy": 0, "Light": 1, "Human Focus": 2, "None": 3}
    else:
        uc_preset_data = {"Heavy": 0, "Light": 1, "None": 2}
    uc_preset = uc_preset_data[uc_preset]
    otp_info = modify_env(
        token=f'"{token}"'.replace("\n", ""),
        model=f'"{model}"',
        img_size=img_size,
        scale=scale,
        rescale=rescale,
        censor=censor,
        sampler=f'"{sampler}"',
        steps=steps,
        sm=sm,
        sm_dyn=sm_dyn,
        legacy_uc=legacy_uc,
        variety=variety,
        decrisp=decrisp,
        skip_format_str=skip_format_str,
        noise_schedule=f'"{noise_schedule}"',
        seed=seed,
        t2i_cool_time=t2i_cool_time,
        save_path=f'"{save_path}"',
        proxy=f'"{proxy}"',
        times_for_scripts=times_for_scripts,
        skip_save_grid=skip_save_grid,
        quality_toggle=quality_toggle,
        uc_preset=uc_preset,
        magnification=magnification,
        hires_strength=hires_strength,
        hires_noise=hires_noise,
        i2i_cool_time=i2i_cool_time,
        pixiv_cookie=f'"{pixiv_cookie}"',
        pixiv_token=f'"{pixiv_token}"',
        allow_tag_edit=allow_tag_edit,
        caption_prefix=f'"{caption_prefix}"'.replace("\n", "\\n"),
        rep_tags=rep_tags,
        rep_tags_per=rep_tags_per,
        rep_tags_with_tag=f'"{rep_tags_with_tag}"',
        pixiv_cool_time=pixiv_cool_time,
        remove_info=remove_info,
        r18=r18,
        default_tag=str([f"{i}" for i in default_tag.replace(" ", "").split(",")]).replace("'", '"'),
        suggest_tag=suggest_tag,
        use_file_name_as_title=use_file_name_as_title,
        use_old_title_rule=use_old_title_rule,
        neighbor=neighbor,
        water_num=water_num,
        meta_data=f'"{meta_data}"',
        revert_info=revert_info,
        share=share,
        height=height,
        port=port,
        g4f_port=g4f_port,
        doc_port=doc_port,
        theme=f'"{theme}"',
        webui_lang=f'"{webui_lang}"',
        skip_update_check=skip_update_check,
        skip_start_sound=skip_start_sound,
        skip_load_g4f=skip_load_g4f,
        skip_finish_sound=skip_finish_sound,
        skip_else_log=skip_else_log,
        new_interface=new_interface,
        num_of_suggest_tag=num_of_suggest_tag,
    )
    return otp_info
