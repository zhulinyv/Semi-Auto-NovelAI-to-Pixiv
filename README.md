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

这是一个 NovelAI 自动生成图片, 经过人工筛选后上传 Pixiv 的脚本集合.

<p>
    <text>灵感来自于我的朋友们: </text> 
    <a href="https://github.com/huliku"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/dc90cc04-7dc0-4dce-968f-39199ca73d4c" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/LittleApple-fp16"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6d9fefe5-44c0-4b58-a54e-baa1b5aca170" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/CyanAutumn"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d82e85ee-2468-41bd-95b7-8e732bd291c4" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/wochenlong"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/1e9821ad-aab3-47c1-8528-7f3f70cd722b" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/zhulinyv"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a3cbe72e-67f6-4aa3-a2dd-e936b8bf9cd9" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
</p>


## 💿 部署

请确保你已经安装了 Python 并将其添加到环境变量中

在命令行中依次执行以下代码

```
.\venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ 配置

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

## 🎉 使用

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


## 📖 待办

+ [x] 批量文生图
+ [x] 批量图生图
+ [x] 批量上传 Pixiv
+ [ ] 计算剩余水晶
+ [ ] 批量 Waifu2x
+ [ ] 批量局部重绘
+ [ ] 批量 vibe
+ [ ] 批量打码
+ [ ] ...

<hr>
<img width="300px" src="https://count.getloli.com/get/@zhulinyv?theme=rule34"></img>

