<p align="center" >
  <img src="https://socialify.git.ci/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/image?description=1&descriptionEditable=%E2%9C%A8%E5%B8%A6%E6%9C%89%20WebUI%20%E7%9A%84%20NovelAI%20%E9%87%8F%E4%BA%A7%E5%B7%A5%E5%85%B7%E2%9C%A8&font=KoHo&forks=1&issues=1&language=1&logo=https%3A%2F%2Fi.postimg.cc%2FTwffWVkX%2F00003-XYTPZ-520621529-1x1-waifu2x-1000x1000-3n-png.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto" alt="Semi-Auto-NovelAI-to-Pixiv" width="640" height="320" />
</p>

<img decoding="async" align=right src="https://i.postimg.cc/0jSHMMJm/kb.png" width="35%">

## 💬 介绍

**English document: [README_EN.md](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/README_EN.md)**

- 这是一个神奇项目, 实现了 NovelAI 本身无法实现的批量生图!

- 它不仅仅只能生图, 是集各种实用功能于一体的超级用户界面!

- **使用中遇到问题请加 QQ 群咨询：[559063963](https://qm.qq.com/cgi-bin/qm/qr?k=I9FqVFb_wn-y5Ejid9CIae57KLLlvDuj&jump_from=webapi&authKey=i+DvSe2nFRBsKNu+D9NK0sFd7Qr1u/vakfRUFDGDCWaceBQOsuiHwkxDa3kRLfup)**

> [!TIP]
> 那天大雨滂沱，雷电交加, 风儿甚是喧嚣，仿佛整个世界都在为某种未知的力量所动摇。

✨ **芝士目前已实现的功能:**

| 功能 | 介绍 | 示例 | 说明 |
|:---:|:---:|:---:|:---:|
| 教程说明 | 本项目的介绍及使用教程 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/15.png?raw=true) | 请仔细阅读 |
|  文生图  | 使用 Gradio 为 NovelAI 写的一个用户界面, 除了界面不同, 其它完全等同于使用 NovelAI 网站 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/1.png?raw=true) | 生成的图片将保存到 `./output/t2i` 文件夹 |
| 随机涩图 | 通过随机组合 `./files/favorite.json` 中的 tag 生成一张涩图或无限生成涩图, 负面提示词将随机选择 favorite.json negative belief 中的负面提示词, 其它参数将使用 env 配置 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/3.png?raw=true) | 关于随机涩图的配置, 请查看 WebUI 配置设置页面的其它部分 |
| 随机图片 | 通过读取 `./file/prompt` 中的 `*.txt` 文件并追加输入的提示词作为提示词无限生成图片, 负面提示词将随机选择 favorite.json negative belief 中的负面提示词, 其它参数将使用 env 配置, 当文件夹下的所有 `*.txt` 文件均生成过一次后或点击停止生成后, 则将停止运行 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/4.png?raw=true) | 关于随机图片的配置, 请查看 WebUI 配置设置页面的其它部分 |
|   Vibe   | 等同于使用 NovelAI 网站, 我为它添加了批量功能 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/16.png?raw=true) | 需要准备一些图片到同一文件夹, 图片名称需要重命名为 `(任意(不含下划线)_(信息提取强度, 浮点型(0, 1))_(参考强度, 浮点型(0, 1)).png)` 的格式, 例如 `hoshino-hinata_1.0_0.6`, 勾选随机涩图时, 无限生成将按照随机涩图的模式生成, 未勾选时, 无限生成将按照随机图片的方式生成 |
|  图生图  | 等同于使用 NovelAI 网站, 支持任何图片, 另外, 我为它添加了批量图生图 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/2.png?raw=true) | 生成的图片将保存到 `./output/i2i` 文件夹, 但会在 `./output` 文件夹内生成一张名为 `temp.png` 的临时图片, 可以删除, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_i2i` |
| 视频转绘 | 将视频用几个步骤重绘, 用于将三次元转绘为二次元 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/18.png?raw=true) | 实验性功能, 欢迎提出建议 |
| 分块重绘 | 将一张大图拆分成 640x640 的小块, 然后将这些小块用图生图的方式放大为 1024x1024, 不需要担心两张图片衔接过硬, 我使用鸣谢列表中的开源项目修复接缝 [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/19.png?raw=true) | 由于耗时较长, 目前仅开放单张放大, 使用时需要提供图片或图片路径(任选其一) |
| 局部重绘 | 仅支持 NovelAI 生成的图片, 并且需要上传蒙版, 支持批量操作 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/5.png?raw=true) | 上传的蒙版应为: 重绘区域为白色, 其余透明而不是黑色, 分辨率等于重绘图像, 批量操作时, 请将图片和蒙版放置于两个文件夹, 并且保证图片和蒙版文件名相同, 例如: `./output/inpaint/img`, `./output/inpaint/mask`, 生成的图片将保存到 `./output/inpaint` |
| 超分降噪 | 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目对图片进行超分降噪, 支持任何图片单张或批量处理 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/6.png?raw=true) | 生成的图片将保存到 `./output/upscale` 文件夹, 不建议使用 **srmd-cuda**, 因为它不稳定. 当使用 **waifu2x-caffe** 或 **waifu2x-converter** 时, 将会在 `./output` 文件夹内生成一个名为 `temp.bat` 的临时批处理文件, 可以删除, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_upscale` |
| 自动打码 | 自动检测图片中的关键部位, 并对其打码 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/7.png?raw=true) | 不能确保 100% 检测出来, 生成的图片将保存到 `./output/mosaic` 文件夹, 批量处理时, 请将图片放到同一个文件夹, 例如: `./output/choose_to_mosaic` |
| 添加水印 | 在图片左上, 右上, 左下, 右下随机某个位置范围添加指定数量的随机透明度的随机水印 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/8.png?raw=true) | 使用前, 请先准备一些自己的水印到 `./files/water` 文件夹. 使用时, 请输入需要处理的图片目录并按确定, 处理后的图片将保存到 `./output/water` |
| 上传Pixiv| 批量将图片上传到 Pixiv |![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/9.png?raw=true) | 关于上传Pixiv的配置, , 请查看 WebUI 配置设置页面的其它部分 |
| 图片筛选 | 人工对图片进行筛选的工具 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/10.png?raw=true) | 使用时, 请先输入图片目录并按下确定, 然后输入输出目录. 会在 `./output` 文件夹下生成一个名为 `array_data.npy` 的文件, 它会保存上次筛选的进度, 即你可以不选择图片目录继续筛选, 筛选完毕后会自动删除. |
| 抹除数据 | 批量抹除, 还原或导出图片生成信息 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/11.png?raw=true) | 还原信息时, 需要准备至少带有 prompt 的 *.png 图片或内容为 prompt 的 *.txt 文件, 并放到某一目录(图片信息文件目录), 选取的待还原图片目录中的文件名(不含扩展名)需要和刚刚的图片信息文件目录中的文件文件名一致 | 
| 法术解析 | 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目进行读取 png info | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/12.png?raw=true) | 使用 iframe 嵌套入本项目 |
|  Tagger  | 使用 [SmilingWolf](https://huggingface.co/spaces/SmilingWolf/wd-tagger) 在 huggingface 上部署的反推模型, 我为它添加了批量操作 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/17.png?raw=true) | 批量处理时, 生成的 prompt 文本会保存到图片的同一目录 |
| GPT Free | 免费, 多模型的 GPT, 使用[鸣谢名单](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv#-%E9%B8%A3%E8%B0%A2)中的开源项目 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/13.png?raw=true) | 使用 iframe 嵌套入本项目 |
| 插件商店 | 展示所有在插件列表(./files/plugins.json)中的插件 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/20.png?raw=true) | 安装时, 将想要安装的插件名称复制粘贴到左上角名称内, 点击安装即可, 重启后生效 |
| 配置设置 | 在 WebUI 更改配置项 | ![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/imgs/14.png?raw=true) | 修改记得保存, 重启后立即生效 |

正在学习 Gradio, 尝试为本项目写一个 WebUI

### 🔌 插件

- 实现动态加载插件, 提高本项目可扩展性!

- 已提交到商店的插件: [插件列表](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/files/plugins.json)

> [!TIP]
> 我独自一人走在湿滑泥泞的街头, 身旁只有寥寥几盏路灯在暗夜中孤寂地闪烁。

## 💿 部署

### 💻 配置需求

- 极低的配置需求, 极致的用户体验!

| 项目 | 说明 |
|:---:|:---:|
| NovelAI 会员 | 为了无限生成图片, 建议 25$/month 会员|
| 魔法网络 | 为了成功发送请求, 确保你可以正常访问相关网站 |
| 1GB 显存 | 为了使用超分降噪所有引擎, 需要至少 1GB 显存 |
| 2GB 内存 | 为了流畅使用本项目, 需要至少 2GB 内存 |
| Windows 10/11(x64) | 为了使用全部功能, 需要使用 64 位 Windows10/11 |
| [Microsoft Visual C++ 2015](https://www.microsoft.com/en-us/download/details.aspx?id=53587) | 为了使用超分降噪所有引擎, 需要安装运行库 |

> [!WARNING]
> 远处传来几声猫的嘶叫，仿佛是夜晚的唯一音符，黑暗荒芜, 寒风刺骨, 伶仃孤苦。

### 🎉 开始部署

#### 0️⃣ Star 本项目

- 如果你喜欢这个项目，请不妨点个 Star🌟，这是对开发者最大的动力

#### 1️⃣ 安装 Python

- 推荐安装 [Python 3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe), 安装时请勾选 **Add Python to PATH**, 其余**保持默认**

#### 2️⃣ 安装 Git

- 推荐安装[最新版本](https://git-scm.com/download/win), 安装时一路 **Next** 即可

#### 3️⃣ 克隆仓库

- 打开 cmd 或 powershell, 执行 `git clone -b main --depth=1 https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv.git`

#### 4️⃣ 接下来的路

- 现在你可以直接运行项目根目录下的 `run.bat` 来启动 WebUI, 首次启动会自动创建虚拟环境并安装依赖, 耗时较长, 可以去冲杯咖啡或继续看下方的文档

> [!TIP]
> 月光透过稀疏的云层，洒在地面上，勾勒出一幅幽冥的画卷。

## ⚙️ 配置

- ⚠️ 1.如果你已经启动了 WebUI, 但没有进行必要配置, 那么请转到设置页面进行必要配置

- ⚠️ 2.请不要跳过这一步, 它非常重要, 确保你已经将所有配置浏览过一遍

- ⚠️ 3.你同样可以直接编辑 `.env` 文件进行配置

> [!WARNING]
> 那几声猫的嘶叫，时而远去，时而又近了, 不知脚下的路究竟是通向何方。

⚠️ token 的获取:

- ![jc](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/82f657fe-81bc-412b-a63c-11a878fde7d2)

⚠️ pixiv_cookie 和 pixiv_token 的获取:

- 1.打开 https://www.pixiv.net/illustration/create 并手动上传图片
- 2.选择标签, 年龄限制, AI生成作品, 公开范围, 作品评论功能, 原创作品
- 3.F12 打开控制台并切换到网络视图
- 4.点击投稿
- 5.找到并单击 illustraion, 右侧切换到标头选项
- 6.在请求头部中可以找到 Cookie 和 X-Csrf-Token
- ![97ae3696ad11708ae2eb0474f198de0c](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/e59caaf6-c69d-485e-965d-d7d924397667)

## 🌟 使用

- **运行 `run.bat`, 会自动打开默认浏览器并跳转到 [127.0.0.1:11451](http://127.0.0.1:11451)**

- 对于旧版用户: 不再建议运行单独脚本, 请使用 WebUI

- 如果真的需要(例如: 浏览器已添加休眠白名单但在非活动页面无法继续生成的情况), 请在 WebUI 中配置好目录等参数并单击**生成独立脚本**(你也可以自己阅读源代码编写独立的脚本), 然后运行根目录下的 **run_stand_alone_scripts.bat**

- 插件开发请移步: [Wiki](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/wiki/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91)

> [!TIP]
> 抬头是无尽的黑暗, 低头是无尽的黑暗, 仿佛陷入一个无边的漩涡中。

## 📖 待办

> [!TIP]
> 黑暗如同一双无形的手，将我紧紧拥抱，深深地吞噬着我的思绪。

<details>
<summary><b>展开查看待办列表</b></summary>

+ [x] 批量文生图
+ [x] 批量图生图
+ [x] 批量上传 Pixiv
+ [x] 计算剩余水晶
+ [x] 批量 [waifu2x](https://github.com/nagadomi/waifu2x)
+ [x] 批量局部重绘
+ [x] ~~批量 vibe~~
+ [x] 批量打码
+ [x] 用 Gradio 写一个 WebUI
+ [ ] ~~将项目放到容器持久化运行~~
+ [x] 修改界面样式
+ [x] ~~添加 ChatGPT~~
+ [x] ~~写一个图片筛选器~~
+ [ ] ~~通过账号密码获取 token~~
+ [x] 添加更多超分引擎
+ [x] 添加文生图方式
+ [x] 批量水印
+ [x] 批量图片信息处理
+ [x] 配置项界面
+ [x] 打开相关文件夹功能
+ [x] 合并随机涩图等界面
+ [x] 热键快速筛图
+ [x] 教程和说明页面
+ [x] 自定义插件
+ [x] 自动生成独立脚本
+ [x] 文生图指定数量
+ [x] 文生图种子点击切换随机
+ [x] 配置项添加是否还原图片信息
+ [x] 补全独立脚本生成
+ [x] 图片保存分类
+ [x] 支持非文生图插件
+ [x] 视频转绘
+ [x] 提示词反推
+ [x] 分块重绘
+ [ ] ~~添加更多插帧引擎~~
+ [x] 翻译剩余页面
+ [x] 自动更新
+ [x] 插件商店
+ [x] 自定义清除元数据
+ [x] 自动安装插件
+ [x] 代理配置
+ [x] 批量 Enhance
+ [ ] ~~自定义保存目录~~
+ [ ] 学习 C# 使用 wpfui 写一个启动器
+ [x] YOLO 检测 NSFW
+ [x] 启动 LOGO(甚至还加了个提示音)
+ [ ] 重新命名函数和变量
+ [ ] 优化保存目录
+ [ ] ...

</details>

## 🤝 鸣谢

本项目使用 [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) | [Anime4KCPP](https://github.com/TianZerL/Anime4KCPP) | [realcugan-ncnn-vulkan](https://github.com/nihui/realcugan-ncnn-vulkan/) | [realesrgan-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | [realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan/) | [srmd-cuda](https://github.com/MrZihan/Super-resolution-SR-CUDA) | [srmd-ncnn-vulkan](https://github.com/nihui/srmd-ncnn-vulkan) | [waifu2x-caffe](https://github.com/lltcggie/waifu2x-caffe) | [waifu2x-converter](https://github.com/DeadSix27/waifu2x-converter-cpp) 降噪和放大图片

本项目使用 [stable-diffusion-inspector](https://spell.novelai.dev/) 解析图片元数据

本项目使用 [Genshin-Sync](https://huggingface.co/spaces/AppleHarem/Genshin-Sync/tree/main) 上传图片至 Pixiv

本项目使用 [GPT4FREE](https://github.com/xtekky/gpt4free) 提供 GPT 服务

本项目使用 [novelai-image-metadata](https://github.com/NovelAI/novelai-image-metadata) 抹除元数据

本项目使用 [SmilingWolf/wd-tagger](https://huggingface.co/spaces/SmilingWolf/wd-tagger) 反推提示词

本项目使用 [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) 处理分块重绘图片接缝

> [!NOTE]
> 坠落, 坠落。

<hr>
<!--img width="500px" src="https://count.getloli.com/get/@zhulinyv?theme=rule34.xxx"></img-->

<a href="https://smms.app/image/ydhHvFDw53GCAfj" target="_blank"><img src="https://s2.loli.net/2022/08/28/ydhHvFDw53GCAfj.png" alt="skirt.png"></a>
