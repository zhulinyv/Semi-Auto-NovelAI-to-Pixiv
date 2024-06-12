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
    remove_info,
    r18,
    default_tag,
    neighbor,
    alpha,
    water_height,
    water_position,
    water_num,
    rotate,
    meta_data,
    revert_info,
    share,
    height,
    port,
    g4f_port,
    theme,
    webui_lang,
    skip_update_check,
    skip_start_sound,
):
    position = str(water_position)
    position = position.replace("'", '"')
    if img_size == "832x1216":
        img_size = [832, 1216]
    elif img_size == "1216x832":
        img_size = [1216, 832]
    else:
        pass
    otp_info = modify_env(
        token=f'"{token}"',
        img_size=img_size,
        scale=scale,
        censor=censor,
        sampler=f'"{sampler}"',
        steps=steps,
        sm=sm,
        sm_dyn=sm_dyn,
        noise_schedule=f'"{noise_schedule}"',
        seed=seed,
        t2i_cool_time=t2i_cool_time,
        save_path=f'"{save_path}"',
        proxy=f'"{proxy}"',
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
        default_tag=str(default_tag).replace("'", '"'),
        neighbor=neighbor,
        alpha=alpha,
        water_height=water_height,
        position=position,
        water_num=water_num,
        rotate=rotate,
        meta_data=f'"{meta_data}"',
        revert_info=revert_info,
        share=share,
        height=height,
        port=port,
        g4f_port=g4f_port,
        theme=f'"{theme}"',
        webui_lang=f'"{webui_lang}"',
        skip_update_check=skip_update_check,
        skip_start_sound=skip_start_sound,
    )
    return otp_info
