import os
import random
import time
import traceback
import uuid

import requests
from loguru import logger

from utils.utils import proxies


def keep_alive(task_func, max_retries=50, base_delay=1, max_delay=64):
    retries = 0
    delay = base_delay

    while retries < max_retries:
        try:
            return task_func()
        except Exception:
            logger.error("[保活] 出现错误:\n>>>>>")
            traceback.print_exc()
            logger.error("<<<<<")
            retries += 1
            # 指数增长
            if retries > 5:
                delay = min(delay * 2, max_delay)
            else:
                delay = min(delay, max_delay)
            delay += random.uniform(0, delay / 3)
            time.sleep(delay)

    logger.error(f"[保活] 保活重试次数用尽 ({max_retries}), 退出.")


def pixiv_upload(
    image_paths: list,
    title: str,
    caption: str,
    labels: list,
    cookie: str,
    x_token: str,
    allow_tag_edit: bool,
    is_r18: bool,
    title_en: str = "",
    caption_en: str = "",
):
    trace_id = uuid.uuid4().hex  # Generates a random UUID and converts it to a hexadecimal string
    span_id = uuid.uuid4().hex[:16]  # Generates a new UUID, but only uses the first 16 characters
    sampled = "0"
    sentry_trace = f"{trace_id}-{span_id}-{sampled}"
    post_url = "https://www.pixiv.net/ajax/work/create/illustration"

    def generate_image_order(files, payload):
        image_order = {}
        for index, file_data in enumerate(files):
            key = f"imageOrder[{index}][fileKey]"
            file_key = str(index)
            image_order[key] = file_key

            key = f"imageOrder[{index}][type]"
            file_type = "newFile"
            image_order[key] = file_type

        # 寻找 'captionTranslations[en]' 字段的位置
        caption_index = None
        for key, value in payload.items():
            if key == "captionTranslations[en]":
                caption_index = list(payload.keys()).index(key)
                break

        # 在 'captionTranslations[en]' 字段的下面插入动态生成的字段
        if caption_index is not None:
            payload = dict(
                list(payload.items())[: caption_index + 1]
                + list(image_order.items())
                + list(payload.items())[caption_index + 1 :]
            )
        else:
            # 如果找不到 'captionTranslations[en]' 字段，则直接在最后插入动态生成的字段
            payload.update(image_order)

        return payload

    def generate_files_list(file_paths):
        files_list = []

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_type = os.path.splitext(file_name)[1]

            if file_type.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
                file_format = "image/png"
            elif file_type.lower() in [".txt", ".pdf", ".doc", ".docx"]:
                file_format = "document"
            else:
                file_format = "unknown"
            files_list.append(("files[]", (file_name, open(file_path, "rb"), file_format)))

        return files_list

    files = generate_files_list(image_paths)

    payload = {
        "aiType": "aiGenerated",
        "allowComment": "true",
        "allowTagEdit": "true" if allow_tag_edit else "false",
        "attributes[bl]": "false",
        "attributes[furry]": "false",
        "attributes[lo]": "false",
        "attributes[yuri]": "false",
        "caption": caption,
        "captionTranslations[en]": caption_en,
        "original": "true",
        "ratings[antisocial]": "false",
        "ratings[drug]": "false",
        "ratings[religion]": "false",
        "ratings[thoughts]": "false",
        "ratings[violent]": "false",
        "responseAutoAccept": "false",
        "restrict": "public",
        "suggestedTags[]": ["女の子"],
        "tags[]": labels,
        "title": title,
        "titleTranslations[en]": title_en,
        "xRestrict": "r18",
    }

    payload = generate_image_order(files, payload)
    if not is_r18:
        payload["xRestrict"] = "general"
        payload["sexual"] = "false"

    headers = {
        "authority": "www.pixiv.net",
        "accept": "application/json",
        "accept-language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
        "baggage": "sentry-environment=production,sentry-release=ee80147438af5620fb60719a59dbba99fc3ba8fb,sentry-public_key=ef1dbbb613954e15a50df0190ec0f023,sentry-trace_id=c995c888a6274d2986a078cf2b335936,sentry-sample_rate=0.1,sentry-transaction=%2Fillustration%2Fcreate,sentry-sampled=false",
        "cookie": cookie,
        "dnt": "1",
        "origin": "https://www.pixiv.net",
        "referer": "https://www.pixiv.net/illustration/create",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sentry-trace": sentry_trace,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "x-csrf-token": x_token,
    }

    post_response = keep_alive(
        lambda: requests.request("POST", post_url, headers=headers, data=payload, files=files, proxies=proxies)
    )
    if not post_response.json().get("error", True):
        get_url = f"https://www.pixiv.net/ajax/work/create/illustration/progress?convertKey={post_response.json()['body']['convertKey']}&lang=zh"
        illust_id = None
        while not illust_id:
            status_resp = keep_alive(
                lambda: requests.request("GET", get_url, headers=headers, data={}, proxies=proxies)
            )
            if status_resp.json()["body"]["status"] == "COMPLETE":
                illust_id = status_resp.json()["body"]["illustId"]
            else:
                time.sleep(1)
        time.sleep(1)
        logger.success(f"上传成功, PID: {illust_id}")
        return illust_id
    else:
        if post_response.json()["body"].get("errors", {}).get("gRecaptchaResponse"):
            logger.warning("上传暂停: 投稿冷却中")
            return 2
        else:
            logger.error(f"上传失败: {post_response.text}")
            return 1
