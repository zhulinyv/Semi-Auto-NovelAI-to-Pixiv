import os
import shutil
from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from moviepy.editor import AudioFileClip, VideoFileClip
from PIL import Image

from src.i2i import i2i_by_hand
from utils.utils import file_path2name, format_str, read_txt


def video2audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(audio_path)


def audio2video(video_path, audio_path, otp_path):
    vd = VideoFileClip(video_path)
    ad = AudioFileClip(audio_path)
    vd2 = vd.set_audio(ad)
    vd2.write_videofile(otp_path)


def video2frame(video_path, frames_save_path, time_interval, save_audio, audio_path):
    logger.info(f"正在将 {file_path2name(video_path)} 拆分...")
    vidcap = cv2.VideoCapture(video_path)
    frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    count = 0
    while success:
        try:
            success, image = vidcap.read()
            count += 1
            if count % time_interval == 0:
                cv2.imencode(".png", image)[1].tofile(str(Path(frames_save_path) / f"frame{count}.png"))
        except Exception:
            pass
    if save_audio:
        video2audio(video_path, str(Path(audio_path) / file_path2name(video_path).replace(".mp4", ".mp3")))
    logger.debug(f"\nframes: {int(frames)}\nfps: {int(fps)}")
    return file_path2name(video_path), int(frames), int(fps), "处理完成!"


def frame2video(im_dir, video_dir, fps):
    im_list: list[str] = os.listdir(im_dir)
    im_list.sort(key=lambda x: int(x.replace("frame", "").split(".")[0]))
    with Image.open(Path(im_dir) / im_list[0]) as img:
        img_size = img.size

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

    for i in im_list:
        with Image.open(Path(im_dir) / i) as png:
            png = png.convert("RGB")
            png.save("./output/temp.jpg")
        frame = cv2.imdecode(np.fromfile("./output/temp.jpg", dtype=np.uint8), -1)
        videoWriter.write(frame)

    videoWriter.release()


def m2m(
    frames_save_path,
    frames_m2m_path,
    pref,
    negative,
    position,
    resolution,
    scale,
    steps,
    sampler,
    noise_schedule,
    strength,
    noise,
    sm,
    sm_dyn,
    seed,
):
    frame_list: list[str] = os.listdir(frames_save_path)
    for frame in frame_list:
        if frame.endswith(".txt"):
            pass
        else:
            prompt = format_str(read_txt(Path(frames_save_path) / file_path2name(frame).replace(".png", ".txt")))
            if position == "最前面(Top)":
                prompt = f"{format_str(pref)}, {prompt}"
            else:
                prompt = f"{prompt}, {format_str(pref)}"
            while 1:
                logger.info(f"正在转绘: {frame}...")
                try:
                    saved_path, _ = i2i_by_hand(
                        Path(frames_save_path) / frame,
                        None,
                        False,
                        prompt,
                        negative,
                        resolution,
                        scale,
                        sampler,
                        noise_schedule,
                        steps,
                        strength,
                        noise,
                        sm,
                        sm_dyn,
                        seed,
                    )
                    shutil.move(saved_path, Path(frames_m2m_path) / file_path2name(frame))
                    break
                except Exception as e:
                    logger.error(f"出现错误: {e}")
                    logger.warning("正在重试...")
    return "处理完成!"


def merge_av(name: str, fps, time_interval, frames_save_path, video_save_path, merge_audio, audio_path):
    frame2video(frames_save_path, str(Path(video_save_path) / name), fps)
    if merge_audio:
        audio2video(str(Path(video_save_path) / name), audio_path, str(Path(video_save_path) / name))
    return "处理完成!"
