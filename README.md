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

## 💬 介绍

English document: [README_EN.md](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/README_EN.md)

✨ **目前已实现的功能**:

| 功能 | 介绍 | 示例 | 说明 |
|:---:|:---:|:---:|:---:|
| 文生图 | 使用 Gradio 为 NovelAI 写的一个用户界面, 除了界面不同, 其它完全等同于使用 NovelAI 网站 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/252b2455-3185-47b4-8606-3a736b3bc99f) | 生成的图片将保存到 `./output/t2i` 文件夹 |
| 图生图 | 等同于使用 NovelAI 网站, 支持任何图片, 另外, 我为它添加了批量图生图 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/43d99c78-70ec-42fe-9762-fcacf0b34d4b) | 生成的图片将保存到 `./output/i2i` 文件夹, 但会在 `./output` 文件夹内生成一张名为 `temp.png` 的临时图片, 可以删除, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_i2i` |
| 随机涩图 | 通过随机组合 `./files/favorite.json` 中的 tag 生成一张涩图或无限生成涩图 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/faf4e7cb-7a63-4cf1-8056-473d986c004e) | 关于随机涩图的配置, 请参考[其它配置](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#%E5%85%B6%E5%AE%83%E9%85%8D%E7%BD%AE)中关于随机涩图部分 |
| 随机图片 | 通过读取 `./file/prompt` 中的 `*.txt` 文件作为提示词无限生成图片, 当文件夹下的所有 `*.txt` 文件均生成过一次后或点击停止生成后, 则将停止运行 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/7bbfa72b-ab54-4011-9a2e-cebf3a6bd275) | 关于随机图片的配置, 请参考[其它配置](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#%E5%85%B6%E5%AE%83%E9%85%8D%E7%BD%AE)中关于随机图片部分 |
| 局部重绘 | 仅支持 NovelAI 生成的图片, 并且需要上传蒙版, 支持批量操作 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/57e91754-c2ec-4bca-9149-cad424569de1) | 上传的蒙版应为: 重绘区域为白色, 其余透明而不是黑色, 分辨率等于重绘图像, 批量操作时, 请将图片和蒙版放置于两个文件夹, 并且保证图片和蒙版文件名相同, 例如: `./output/inpaint/img`, `./output/inpaint/mask`, 生成的图片将保存到 `./output/inpaint` |
| 超分降噪 | 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目对图片进行超分降噪, 支持任何图片单张或批量处理 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/3465c6be-4326-423d-848b-1a281e1e32ae) | 生成的图片将保存到 `./output/upscale` 文件夹, 不建议使用 **srmd-cuda**, 因为它不稳定. 当使用 **waifu2x-caffe** 或 **waifu2x-converter** 时, 将会在 `./output` 文件夹内生成一个名为 `temp_waifu2x.bat` 的临时批处理文件, 可以删除, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_upscale` |
| 自动打码 | 自动检测图片中的关键部位, 并对其打码 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/98650568-c58f-4571-8dcd-222e1b48e5be) | 不能确保 100% 检测出来, 生成的图片将保存到 `./output/mosaic` 文件夹, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_mosaic` |
| 添加水印 | 在图片左上, 右上, 左下, 右下随机某个位置范围添加指定数量的随机透明度的随机水印 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/4016b4f5-6c83-4c8c-b1db-e372eddae425) | 使用时, 请输入需要处理的图片目录并按确定, 处理后的图片将保存到 `./output/water` |
| 上传Pixiv | 批量将图片上传到 Pixiv |![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/95603593-6bff-47aa-a5c6-5ba21067e306) | 关于上传Pixiv的配置, 请参考[其它配置](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#%E5%85%B6%E5%AE%83%E9%85%8D%E7%BD%AE)中关于上传Pixiv部分 |
| 法术解析 | 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目进行读取 png info | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/08fcf698-4be3-4ee3-b4a5-4225810740ca) | 使用 iframe 嵌套入本项目 |
| GPT Free | 免费, 多模型的 GPT, 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a3ae56b2-4fc4-47e1-8d1d-aa01b7114892) | 使用 iframe 嵌套入本项目 |
| 图片筛选 | 人工对图片进行筛选的工具 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/47a261bc-f962-489f-83b1-2f7381fb5e0a) | 使用时, 请先输入图片目录并按下确定, 然后输入输出目录. 会在 `./output` 文件夹下生成一个名为 `array_data.npy` 的文件, 它会保存上次筛选的进度, 即你可以不选择图片目录继续筛选, 筛选完毕后会自动删除. |

<p>
    <text>灵感来自于我的朋友们: </text> 
    <a href="https://github.com/huliku"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/dc90cc04-7dc0-4dce-968f-39199ca73d4c" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/LittleApple-fp16"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6d9fefe5-44c0-4b58-a54e-baa1b5aca170" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/CyanAutumn"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d82e85ee-2468-41bd-95b7-8e732bd291c4" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/wochenlong"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/1e9821ad-aab3-47c1-8528-7f3f70cd722b" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/zhulinyv"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a3cbe72e-67f6-4aa3-a2dd-e936b8bf9cd9" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
</p>

正在学习 Gradio, 尝试为本项目写一个 WebUI

## 💻 配置需求

| 项目 | 说明 |
|:---:|:---:|
| NovelAI 会员 | 为了无限生成图片, 建议 25$/month 会员|
| 魔法网络 | 为了成功发送 post 请求, 需要魔法网络 |
| 1GB 显存 | 为了使用超分降噪所有引擎, 需要至少 1GB 显存 |
| 2GB 内存 | 为了流畅使用本项目, 需要至少 2GB 内存 |
| Windows 10/11(x64) | 为了使用全部功能, 需要使用 64 位 Windows10/11 |
| [Microsoft Visual C++ 2015](https://www.microsoft.com/en-us/download/details.aspx?id=53587) | 为了使用超分降噪所有引擎, 需要安装运行库 |

## 💿 部署

### 1️⃣ 安装 Python

推荐安装 [Python 3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe), 安装时请勾选 **Add Python to PATH**, 其余保持默认

### 2️⃣ 接下来的路

现在你可以直接运行项目根目录下的 `run.bat` 来启动 WebUI, 首次启动会自动创建虚拟环境并安装依赖, 耗时较长, 可以去冲杯咖啡或继续看下方的文档

## ⚙️ 配置

⚠️ 1.请不要跳过这一步, 它非常重要, 确保你已经将所有配置浏览过一遍

⚠️ 2.如果你已经启动了 WebUI, 但没有进行必要配置, 那么请关闭它

⚠️ 3.使用项目前, 你需要复制一份 `env.example` 并重命名为 `.env`

⚠️ 4.如果你已经启动过一次, 脚本将会自动进行复制和重命名操作

⚠️ 5.以下配置仅有三项为必须配置(不配置将无法使用相关功能), 其余可以按需配置

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
| alpha | 否 | float | 0.7 | 水印透明度(0~1, 越大越透明) | 0.5 |
| water_height | 否 | int | 135 | 调整水印的高度 | 100 |
| position | 否 | list[str] | ["左上", "右上", "左下", "右下"] | 水印可能出现的位置 | ["左上"] |
| water_num | 否 | int | 1 | 水印的数量 | 2 |

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

- 关于随机图片, 请将提示词文件(例如: example.txt, 文件内含有 prompt 放到 `./files/prompt` 文件夹

```
例如:
.\files
  └---\prompt
        └---可莉.txt -> 文件内容: tianliang duohe fangdongye, loli, klee_(genshin_impact)
        └---loli.txt -> 文件内容: {{{loli}}}
        └---114514.txt -> 文件内容: {henghengheng aaaaa}
```

- 关于上传 Pixiv, 需要将选择上传的图片或文件夹放到同一个文件夹, 例如 `./output/pixiv`

```
例如:
.\output
  └---\pixiv
        └---7589641258_GenshinImpact_可莉.png -> 注意: 图片的名称为: 种子_出处_角色.png 的形式, 将会根据生成信息以及出处和角色进行打标签, 角色将作为标题
        └---6594641258dwuibuib_None_None.png  -> 注意: 图片的名称为: 内容_None_None.png 的形式, 将会根据生成信息进行打标签, None 将作为标题
        └---拉菲.png                          -> 注意: 这样的图片将会导致错误, 不用担心, 如果完全使用本项目生成的图片, 生成的图片名均是符合标准的
        └---\Nahida                           -> 注意: 可以将文件夹作为图片组, 即上传的一个作品中含有多张图片
              └---5264942125_GenshinImpact_纳西妲.png
              └---4351819919_GenshinImpact_纳西妲.png
```

- 关于随机涩图, 请根据说明在对应位置自行添加配置:

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
+ [x] 批量水印
+ [ ] 批量图片信息处理
+ [ ] ...

## 🤝 鸣谢

本项目使用 [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) | [Anime4KCPP](https://github.com/TianZerL/Anime4KCPP) | [realcugan-ncnn-vulkan](https://github.com/nihui/realcugan-ncnn-vulkan/) | [realesrgan-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | [realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan/) | [srmd-cuda](https://github.com/MrZihan/Super-resolution-SR-CUDA) | [srmd-ncnn-vulkan](https://github.com/nihui/srmd-ncnn-vulkan) | [waifu2x-caffe](https://github.com/lltcggie/waifu2x-caffe) | [waifu2x-converter](https://github.com/DeadSix27/waifu2x-converter-cpp) 降噪和放大图片

本项目使用 [stable-diffusion-inspector](https://spell.novelai.dev/) 解析图片元数据

本项目使用 [Genshin-Sync](https://huggingface.co/spaces/AppleHarem/Genshin-Sync/tree/main) 上传图片至 Pixiv

本项目使用 [GPT4FREE](https://github.com/xtekky/gpt4free) 提供 GPT 服务

<hr>
<img width="300px" src="https://count.getloli.com/get/@zhulinyv?theme=rule34"></img>
