<p align="center" >
  <img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/0fbed41e-1b2b-44f4-9562-6eb7aeeb2c7c" width="256" height="256" alt="NJS"></a>
</p>
<h1 align="center">Semi-Auto-NovelAI-to-Pixiv</h1>
<h4 align="center">✨通过 NovelAI 生图并上传 Pixiv✨</h4>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue">
    <a href="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/raw/main/LICENSE"><img src="https://img.shields.io/github/license/zhulinyv/Semi-Auto-NovelAI-to-Pixiv" alt="license"></a>
    <img src="https://img.shields.io/github/issues/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
    <img src="https://img.shields.io/github/stars/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
    <img src="https://img.shields.io/github/forks/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
</p>

## 💬 前言

英文版文档: [README_EN.md](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/README_EN.md)

这是一个 NovelAI 自动生成图片, 经过人工筛选后上传 Pixiv 的脚本

<details>
<summary><b>查看运行示例</b></summary>

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d6059625-0640-46dd-97b6-ecbfcb37b646)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/685a034f-e66b-4afd-8e2e-5e0a2ebca709)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/74874ed3-6686-4cd2-b80e-3b3a3dca4b0a)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a6c3973a-76e3-47b6-aa1e-b3e20850cf41)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/5f30cb40-f014-4aff-81ef-f86b02ae2fdb)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/b76c93a0-bddc-4792-8a39-8673c0edc30d)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/f0b4ab5c-3ebb-489c-83b7-3b32676c28ae)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6b794c4f-2a9a-4d2c-96f1-394c801d880e)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/30e22047-ce6c-4016-896b-852e55b9e724)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/12f73504-e7b8-420b-aa90-9a8610cd1a0e)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/b1f43335-fff8-440d-a50e-5399dee10c67)

</details>

<p>
    <text>灵感来自于我的朋友们: </text> 
    <a href="https://github.com/huliku"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/dc90cc04-7dc0-4dce-968f-39199ca73d4c" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/LittleApple-fp16"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6d9fefe5-44c0-4b58-a54e-baa1b5aca170" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/CyanAutumn"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d82e85ee-2468-41bd-95b7-8e732bd291c4" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/wochenlong"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/1e9821ad-aab3-47c1-8528-7f3f70cd722b" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/zhulinyv"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a3cbe72e-67f6-4aa3-a2dd-e936b8bf9cd9" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
</p>

正在学习 Gradio, 尝试为本项目写一个 WebUI

## 💿 部署

请确保你已经安装了 Python 并将其添加到环境变量中

这些脚本均可独立运行, 如有需要请展开 ↓

<details>
<summary>已过时(请直接运行 run.bat)</summary>

在命令行中依次执行以下代码

```
.\venv\Scripts\activate
pip install -r requirements.txt
```

</details>

## ⚙️ 配置

使用项目前, 你需要复制一份 `env.example` 并重命名为 `.env`, 并对照下方表格按照需要修改配置

| 项目 | 必须 | 类型 | 默认 | 说明 | 示例 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| token |是| str | "xxx" |生成图片需要的 token | "eyJhbG..." |
| img_size |否| int \| list[int] | -1 |生成图片的分辨率| [832, 1216] |
| scale |否| float | 5.0 |提示词相关性| 7.0 |
| censor |否| bool | False | 是否对生成的图片打码 | True |
| sampler |否| str | "k_euler" | 采样器 | "k_dpmpp_2m" |
| steps |否| int | 28 | 采样步数 | 20 |
| sm |若开启 sm_dyn 则是| bool | False | sm | True |
| sm_dyn |否| bool | False | sm_dyn | True |
| noise_schedule |否| str | "native" |噪声计划表| "karras" |
| seed | 否 | int | -1 | 随机种子 | 2468751262 |
| magnification | 否 | float | 1.5 | 图生图的放大倍数 | 1.3 |
| hires_strength | 否 | float | 0.5 |重绘幅度| 0.6 |
| pixiv_cookie | 是 | str | "xxx" | 上传 Pixiv 使用的 cookie | "first_..." |
| pixiv_token | 是 | str | "xxx" | 上传 Pixiv 使用的 x-csrf-token | "655c0c..." |
| allow_tag_edit | 否 | bool | True | 是否允许其它用户编辑标签 | False |
| waifu2x_scale | 否 | int | 2 | waifu2x 放大倍数 | 4 |
| waifu2x_noise | 否 | int | 3 | waifu2x 降噪等级 | 2 |
| share | 否 | bool | False | 是否共享 gradio 链接 | True |
| height | 否 | int | 650 | 法术解析页面的高度 | 800 |
| port | 否 | int | 11451 | 本地启动的端口 | 13579 |
| theme | 否 | str \| None | "NoCrypt/miku" | WebUI 界面主题 | 更多请查看 [Themes Gallery](https://huggingface.co/spaces/gradio/theme-gallery) |
| caption_prefix | 否 | str \| None | "Hi there! 这里是小丫头片子, 芝士我的 QQ 群: 632344043, 欢迎!" | 上传 pixiv 的描述前缀 | 你好 |
| neighbor | 否 | float | 0.01 | 方形马赛克相对于图片的边长 | 0.008 |
| negetive | 否 | str | "nsfw, ..." | 随机图片使用的负面 | "sfw, ..." |

⚠️ token 的获取:

- 1.登录 https://novelai.net/login
- 2.F12 打开控制台并切换到控制台
- 3.输入 `console.log(JSON.parse(localStorage.session).auth_token)` 回车, 返回的字符串即为 token
- ![e3756ce75c6f6850efa633dbaa3a5ae6](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/502c9a49-6a73-446d-9401-e559628ad079)

⚠️ pixiv_cookie 和 pixiv_token 的获取:

- 1.打开 https://www.pixiv.net/illustration/create 并手动上传图片
- 2.选择标签, 年龄限制, AI生成作品, 公开范围, 作品评论功能, 原创作品
- 3.F12 打开控制台并切换到网络视图
- 4.点击投稿
- 5.找到并单击 illustraion, 右侧切换到标头选项
- 6.在请求头部中可以找到 Cookie 和 X-Csrf-Token
- ![97ae3696ad11708ae2eb0474f198de0c](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/e59caaf6-c69d-485e-965d-d7d924397667)

### 其它配置:

关于随机图片, 请将提示词文件(例如: example.txt, 文件内含有 prompt)放到 `./files/prompt` 文件夹

```
例如:
.\files
  └---\prompt
        └---可莉.txt -> 文件内容: tianliang duohe fangdongye, loli, klee_(genshin_impact)
        └---loli.txt -> 文件内容: {{{loli}}}
        └---114514.txt -> 文件内容: {henghengheng aaaaa}
```

关于随机涩图, 可以在对应位置自行添加配置:

```py
{
  "artists": {
    ...,
    "belief": {
      "0.6(以下画风抽取到的概率, 此处概率为 1-0.6)": {
        "画风(你喜欢的画风)": [
          "balabala...",
          0(是否开启 sm, 1 为开启, 0 为关闭),
          6.3(提示词相关性, 若设为 0, 则读取 .env 文件配置)
        ]
      },
      "0.3(以下画风抽取到的概率, 此处概率为 0.6-0.3)": {
        "画风(你喜欢的画风)": [
          "balabala...",
          0(是否开启 sm, 1 为开启, 0 为关闭),
          6.3(提示词相关性, 若设为 0, 则读取 .env 文件配置)
        ]
      }
    },
    ...
  },
  "negative_prompt": {
    ...,
    "belief": [
      "prompt(负面提示词)"
    ]
  },
  "character": {
    "Game(这一组角色出处)": {
      "name(角色名)": [
        "tag1(这个角色的描述)",
        "tag2, tag3(可以为单个, 也可以为一串)"
      ]
    }
  },
  "R18": {
    "动作": {
      "巨乳动作": {
        "name(动作名称)": [
          "tag1(这个动作的描述)",
          "tag2, tag3(可以为单个, 也可以为一串)"
        ]
      },
      "普通动作": {
        "name(动作名称)": [
          "tag1(这个动作的描述)",
          "tag2, tag3(可以为单个, 也可以为一串)"
        ]
      }
    },
    "表情": {
      "口交表情": {
        "name(表情名称)": [
          "tag1(这个表情的描述)",
          "tag2, tag3(可以为单个, 也可以为一串)"
        ]
      },
      "普通表情": {
        "name(表情名称)": [
          "tag1(这个表情的描述)",
          "tag2, tag3(可以为单个, 也可以为一串)"
        ]
      }
    },
    "场景": {
      "仅场景": {
        "name(场景名称)": [
          "tag1(这个场景的描述)",
          "tag2, tag3(可以为单个, 也可以为一串)"
        ]
      },
      ...
    },
    ...
  },
  "labels": {
    "Game(对应上方添加的出处)": {
      "name(对应上方添加的角色)": [
        "char_name(上传 Pixiv 对这个角色添加的标签)",
        "char_jp_name(上传 Pixiv 对这个角色添加的标签)"
      ]
    },
    "description": {
      "tag (某个提示词)": [
        "tag_label(上传 Pixiv 对这个提示词添加的标签)"
      ]
    }
  }
}
```

这些脚本均可独立运行, 如有需要请展开 ↓

<details>
<summary>已过时(请直接运行 run.bat)</summary>

> 对于图生图, 需要将 NovelAI 生成的图片放到 `.\output\choose_for_i2i` 文件夹

```
例如:
需要放大的图片:
.\output
  └---\choose_to_i2i
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
放大之后的图片:
.\output
  └---\i2i
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> 对于上传 Pixiv, 需要将选择上传的图片或文件夹放到 `.\output\pixiv` 文件夹

```
例如:
.\output
  └---\pixiv
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
        └---\Nahida
              └---5264942125_GenshinImpact_纳西妲.png
              └---4351819919_GenshinImpact_纳西妲.png
```

> 对于 [waifu2x](https://github.com/nagadomi/waifu2x) 放大, 需要将图片放到 `.\output\choose_for_upscale` 文件夹

```
例如:
.\output
  └---\choose_to_upscale
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> 对于打马赛克, 需要将图片放到 `.\output\choose_to_mosaic` 文件夹

```
例如:
.\output
  └---\mosaic
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> 对于局部重绘, 需要将重绘图片放到 `.\output\inpaint\img` 文件夹, 蒙版图片放到 `.\output\inpaint\mask` 文件夹

```
例如:
.\output
  └---\inpaint
        └---img
            └---7589641258_GenshinImpact_可莉.png
            └---6594641258_AzureLane_拉菲.png
        └---mask
            └---7589641258_GenshinImpact_可莉.png
            └---6594641258_AzureLane_拉菲.png
```

</details>

## 🎉 使用

运行 `run.bat`, 即可在[浏览器打开的链接](http://127.0.0.1:11451/)进行生成图片

运行 `selector.py`, 即可在打开的窗口进行筛选图片

这些脚本均可独立运行, 如有需要请展开 ↓

<details>
<summary>已过时(请直接运行 run.bat)</summary>

### 1️⃣ 激活虚拟环境

```
.\venv\Scripts\activate
```

### 2️⃣ 根据需要选择脚本

#### t2i.py

```
python t2i.py
```

随机生成涩图到 `.\output`


#### i2i.py

```
python i2i.py
```

放大 `.\output\choose_for_i2i` 中的图片到  `.\output\i2i`

#### pixiv.py

```
python pixiv.py
```

上传 `.\output\pixiv` 中的图片或文件加到 Pixiv

#### waifu2x.py

```
python pixiv.py
```

使用 [waifu2x-ncnn-vulkan](https://github.com/nagadomi/waifu2x-ncnn-vulkan) 放大图片

![效果](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a304d3bd-181f-4d94-ac18-a2c53b9f2f79)

#### mosaic.py

```
python mosaic.py
```

对关键部位打马赛克

#### inpaint.py

```
python inpaint.py
```

</details>


## 📖 待办

+ [x] 批量文生图
+ [x] 批量图生图
+ [x] 批量上传 Pixiv
+ [x] 计算剩余水晶
+ [x] 批量 [waifu2x](https://github.com/nagadomi/waifu2x)
+ [x] 批量局部重绘
+ [ ] ~~批量 vibe~~
+ [x] 批量打码
+ [x] 用 Gradio 写一个 WebUI
+ [ ] 将项目放到容器持久化运行
+ [x] 修改界面样式
+ [x] ~~添加 ChatGPT~~
+ [x] ~~写一个图片筛选器~~
+ [ ] 通过账号密码获取 token
+ [x] 添加更多超分引擎
+ [x] 添加文生图方式
+ [ ] ...

## 🤝 鸣谢

本项目使用 [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) | [Anime4KCPP](https://github.com/TianZerL/Anime4KCPP) | [realcugan-ncnn-vulkan](https://github.com/nihui/realcugan-ncnn-vulkan/) | [realesrgan-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | [realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan/) | [srmd-cuda](https://github.com/MrZihan/Super-resolution-SR-CUDA) | [srmd-ncnn-vulkan](https://github.com/nihui/srmd-ncnn-vulkan) | [waifu2x-caffe](https://github.com/lltcggie/waifu2x-caffe) | [waifu2x-converter](https://github.com/DeadSix27/waifu2x-converter-cpp) 降噪和放大图片

本项目使用 [stable-diffusion-inspector](https://spell.novelai.dev/) 解析图片元数据

本项目使用 [Genshin-Sync](https://huggingface.co/spaces/AppleHarem/Genshin-Sync/tree/main) 上传图片至 Pixiv

<hr>
<img width="300px" src="https://count.getloli.com/get/@zhulinyv?theme=rule34"></img>
