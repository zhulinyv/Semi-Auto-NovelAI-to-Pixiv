def modify_env(**kwargs: dict):
    keys = list(kwargs.keys())
    for target_key in keys:
        new_value = kwargs[target_key]
        with open(".env", "r", encoding="utf-8") as f:
            lines = f.readlines()
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
    magnification,
    hires_strength,
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
    meta_data,
    share,
    height,
    port,
    g4f_port,
    theme,
    webui_lang,
):
    position = []
    if ul:
        position.append("左上")
    if ll:
        position.append("左下")
    if ur:
        position.append("右上")
    if lr:
        position.append("右下")
    position = str(position)
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
        magnification=magnification,
        hires_strength=hires_strength,
        pixiv_cookie=f'"{pixiv_cookie}"',
        pixiv_token=f'"{pixiv_token}"',
        allow_tag_edit=allow_tag_edit,
        caption_prefix=f'"{caption_prefix}"',
        rep_tags=rep_tags,
        rep_tags_per=rep_tags_per,
        rep_tags_with_tag=f'"{rep_tags_with_tag}"',
        pixiv_cool_time=pixiv_cool_time,
        neighbor=neighbor,
        alpha=alpha,
        water_height=water_height,
        position=position,
        water_num=water_num,
        meta_data=f'"{meta_data}"',
        share=share,
        height=height,
        port=port,
        g4f_port=g4f_port,
        theme=f'"{theme}"',
        webui_lang=f'"{webui_lang}"',
    )
    return otp_info
