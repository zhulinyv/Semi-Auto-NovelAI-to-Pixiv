# Semi-Auto-NovelAI-to-Pixiv 食用手册

## 前言

这是一个神奇的项目, 实现了 NovelAI 本身无法实现的更多功能!

这里是我的 QQ 群: 559063963, 如有任何开发或使用中的问题请加群!

食用手册将细化到每一个组件, 但当出现类似或重复功能时, 将仅在第一次出现时说明一次.

## 文生图

### 正面提示词

![positive_input](https://github.com/zhulinyv/SANP-Document/raw/main/images/positive_input.png?raw=true)

在这里, 你可以输入你想画的一切!

### 负面提示词

![negative_input](https://github.com/zhulinyv/SANP-Document/raw/main/images/negative_input.png?raw=true)

在这里, 你可以输入你一切你不想画的!

### 生成参数

#### 分辨率

![resolution](https://github.com/zhulinyv/SANP-Document/raw/main/images/resolution.png?raw=true)

在上方的分辨率中, 你快捷选择一些内置的分辨率, 选择后, 下方的宽高输入框将自动变化.

当你想要的分辨率不在上方的分辨率下拉列表时, 你可以手动输入下方的**宽**和**高**来自定义分辨率.

需要注意的是, 在 NovelAI 中, 所有的分辨率数值都必须是 32 的倍数, 但你<u>**无需担心**</u>, 在生成时我会自动帮你修改为最靠近你输入的分辨率数值且为 32 倍数的分辨率(在 NovelAI 官网同样会进行此处理)!

另外, 当输入分辨率较大时, **请注意点数的消耗**.

#### 提示词相关性

![scale](https://github.com/zhulinyv/SANP-Document/raw/main/images/scale.png?raw=true)

该值越大, 图片内容将越符合输入的提示词; 反之, 越偏离输入的提示词.

#### 采样器

![sampler](https://github.com/zhulinyv/SANP-Document/raw/main/images/sampler.png?raw=true)

不同的采样器将会对画风产生一定影响.

#### 噪声计划表

![noise_schedule](https://github.com/zhulinyv/SANP-Document/raw/main/images/noise_schedule.png?raw=true)

不同的噪声计划表将会对画风产生一定影响.

#### 采样步数

![steps](https://github.com/zhulinyv/SANP-Document/raw/main/images/steps.png?raw=true)

在 1 至 28 步内, 步数越大, 画面越细致.

但超过 28 步后, 画面的变化极小.

同时, 在 25 🔪的会员中, 超过 28 步需要**消耗额外点数**.

#### sm & sm_dyn

![sm](https://github.com/zhulinyv/SANP-Document/raw/main/images/sm.png?raw=true)

开启 sm 后, 将对某些画风产生不同程度的影响.

sm_dyn 同理, 但开启 sm_dyn 需要同时开启 sm 才生效.

![seed](https://github.com/zhulinyv/SANP-Document/raw/main/images/seed.png?raw=true)

当需要固定种子时, 直接文本框内修改即可.

当想切换到随机种子时, 单击右侧 "♻️" 按钮, 将自动把左侧文本框内的内容改为 "-1".

#### variety & decrisp

![variety](https://github.com/zhulinyv/SANP-Document/raw/main/images/variety.png?raw=true)

开启 variety 可改善画风和肢体表现等

开启 decrisp 可使动作更加多样性

#### 生成数量

![num](https://github.com/zhulinyv/SANP-Document/raw/main/images/num.png?raw=true)

可通过下方的滑条或小文本框设置生成的数量, 默认最大生成数量是 999.

设置好生成数量后点击 "开始生成" 即可执行重复的图片生成操作.

### wildcards

![wildcards](https://github.com/zhulinyv/SANP-Document/raw/main/images/wildcards.png?raw=true)

这是一个类似于 stable-diffusion-webui 中的 embedding 的功能.

在 "wildcard文件" 下拉列表中选择文件后, 再在 "名称" 下拉列表中选择一个名称, 此时, 在下方 "tag" 文本框中即可看到其中的 tag.

当点击 "添加到文本框" 时, 选定的内容将自动被添加到 "正面提示词" 或 "负面提示词" 文本框末尾.

### 打开保存目录

![open_saved_path](https://github.com/zhulinyv/SANP-Document/raw/main/images/open_saved_path.png?raw=true)

点击此按钮时, 将自动打开图片保存目录.

## 随机蓝图

### 提示词的随机与固定

![random_nsfw_images](https://github.com/zhulinyv/SANP-Document/raw/main/images/random_nsfw_images.png?raw=true)

这里不需要自己输入提示词, 会自动组装文件中的提示词并进行图片生成.

组装的顺序为：<角色>, <画风>, <审查>, <表情>, <动作>, <场景>, <污渍>, <质量词>

当你其中的某一项不想让其随机时, 通过对应的下拉列表将其变成固定的内容即可.

### 更新列表

![update_list_button](https://github.com/zhulinyv/SANP-Document/raw/main/images/update_list_button.png?raw=true)

当添加完新的提示词时, 点击这个按钮即可刷新上方的全部提示词下拉列表.

提示词的添加与删除请继续看下方说明: [添加提示词](#添加提示词) [删除提示词](#删除提示词)

### 生成按钮

![genarate_button](https://github.com/zhulinyv/SANP-Document/raw/main/images/genarate_button.png?raw=true)

```
"开始生成" 按钮: 仅生成一次图片
"无限生成" 按钮: 无限生成按钮
"停止生成" 按钮: 无限生成时用来停止生成
```

### 生成独立脚本

![stand_alone](https://github.com/zhulinyv/SANP-Document/raw/main/images/stand_alone.png?raw=true)

此按钮的意义在于你想要大量生成却又不想将浏览器置于前台时使用.

点击后, 运行项目目录中的 `run_stand_alone_scripts.bat` 即可独立执行该功能, 并且可关闭网页及控制台.

### 添加提示词

提示词的添加有两种方式：

#### 方法1

![file_to_add](https://github.com/zhulinyv/SANP-Document/raw/main/images/file_to_add.png?raw=true)

- 1. 首先, 在此处的下拉框选择想添加 tag 到哪个文件.

```
actions.yaml       : 动作文件
artists.yaml       : 画风文件
characters.yaml    : 角色文件
emotions.yaml      : 表情文件
negative.yaml      : 负面提示词文件
prefixes.yaml      : 质量词文件
stains.yaml        : 污渍文件
surroundings.yaml  : 场景文件
```


![tag_to_add](https://github.com/zhulinyv/SANP-Document/raw/main/images/tag_to_add.png?raw=true)

- 2. 然后, 输入提示词到此处的文本框.

![name_to_add](https://github.com/zhulinyv/SANP-Document/raw/main/images/name_to_add.png?raw=true)

- 3. 输入名称和选中概率

![else_to_add](https://github.com/zhulinyv/SANP-Document/raw/main/images/else_to_add.png?raw=true)

- 4. 当选择某些文件时, 下方的参数为必填项, 请注意.

![add_button](https://github.com/zhulinyv/SANP-Document/raw/main/images/add_button.png?raw=true)

- 5. 上方内容全部填写好后, 点击 "添加" 按钮即可完成添加.

#### 方法2

![dir](https://github.com/zhulinyv/SANP-Document/raw/main/images/dir.png?raw=true)

在如上所示目录中找到对应的文件, 打开后仿照格式进行添加.

![example](https://github.com/zhulinyv/SANP-Document/raw/main/images/example.png?raw=true)

如上图所示, 添加内容时请注意 yaml 文件格式, 英文冒号后必须要有空格, 并且内容完全(比如画风文件必须包含 tag, cfg, sm...)

### 删除提示词

提示词的删除有两种方式:

#### 方法1

![file_to_del](https://github.com/zhulinyv/SANP-Document/raw/main/images/file_to_del.png?raw=true)

依次选择 "想要删除什么内容(哪个文件)", "名称", 完成选择后, 在下方的文本框内即可看到 tag.

点击删除即可删除该名称提示词, 注意：这是一个不可逆操作, 删除后需要重新添加.

#### 方法2

![dir](https://github.com/zhulinyv/SANP-Document/raw/main/images/dir.png?raw=true)

在如上所示目录中找到对应的文件, 打开后仿照格式进行删除.

## 随机图片

### 追加提示词

![add_tag](https://github.com/zhulinyv/SANP-Document/raw/main/images/add_tag.png?raw=true)

在文本框中输入一些你想要的内容(支持 wildcard), 并选择内容追加到哪里.

### 其它参数

![sfw_else_setting](https://github.com/zhulinyv/SANP-Document/raw/main/images/sfw_else_setting.png?raw=true)

随机图片的提示词文件在 `files/prompt` 文件夹, 生成过的 *.txt 文件将被移动到 `files/prompt/done`, 勾选 "组织生成后移动提示词文件" 将不会移动.

```
例如:
.\files
  └---\prompt
        └---可莉.txt -> 文件内容: tianliang duohe fangdongye, loli, klee_(genshin_impact)
        └---loli.txt -> 文件内容: {{{loli}}}
        └---114514.txt -> 文件内容: {henghengheng aaaaa}
```

随机抽取的画风在 `files/favorites/artists.yaml` 文件中, 画风的添加与删除请参照：[添加提示词](#添加提示词) [删除提示词](#删除提示词)

## Vibe

![vibe](https://github.com/zhulinyv/SANP-Document/raw/main/images/vibe.png?raw=true)

在此处添加基底图片

## CasRand

![casrand](https://github.com/zhulinyv/SANP-Document/raw/main/images/casrand.png?raw=true)

请参考上方图片说明或`插件说明`页面的教程.

## 画风生成

### 固定提示词

![random_artist_tag](https://github.com/zhulinyv/SANP-Document/raw/main/images/random_artist_tag.png?raw=true)

希望固定的内容请在此处填写, 并选择 roll 的画风串加到固定提示词的最前面或最后面.

使用固定提示词功能时, 需要将下方的 "固定提示词" 取消勾选.

### 提示词文件路径

![random_artist_tag](https://github.com/zhulinyv/SANP-Document/raw/main/images/random_artist_tag.png?raw=true)

默认与[随机图片](#随机图片)的提示词文件路径一致, 你也可以自定义提示词文件路径.

### 权重与前缀

![random_artist_weight](https://github.com/zhulinyv/SANP-Document/raw/main/images/random_artist_weight.png?raw=true)

当勾选 "随机权重" 时, 下方的所有内容才会生效.

当勾选 "year2023" 时, 将会在 roll 的画风串最后添加 "year2023".

当勾选 "artist前缀" 时, 所有的画师 tag 前都会加上 "artist:".

单画师文件在 `plugins/t2i/sanp_plugin_random_artists/artists.json` 文件中, 可以参照其中的格式添加或删除一些单画师 tag.

## 随机Vibe

![random_vibe](https://github.com/zhulinyv/SANP-Document/raw/main/images/random_vibe.png?raw=true)

当勾选此选项时, 将按照随机蓝图的模式组装 tag；未勾选此选项时, 将按照随机图片的模式读取 tag.

## 图生图

![i2i_path](https://github.com/zhulinyv/SANP-Document/raw/main/images/i2i_path.png?raw=true)

当需要批量处理时, 请填写批量处理的图片目录, 相对路径或绝对路径均可, 并将是否启用批处理切换为 True.

![i2i_image](https://github.com/zhulinyv/SANP-Document/raw/main/images/i2i_image.png?raw=true)

当需要单张处理时, 需要将图片上传至此处, 并将是否启用批处理切换为 False.

## 视频转绘

### 视频拆帧

![m2m1](https://github.com/zhulinyv/SANP-Document/raw/main/images/m2m1.png?raw=true)

视频路径：需要填写 *.mp4 文件的路径, 相对路径或绝对路径均可

帧保存目录(空目录): 提取的帧的保存目录.

间隔取帧：当视频帧率较高或较长时, 请增大它以减少重绘图片数量进而减少所用时间.

提取音频：勾选后, 需要同时填写下方的音频保存目录.

音频保存目录：从视频中分离的音频的保存目录.

### 逐帧转绘

![m2m4](https://github.com/zhulinyv/SANP-Document/raw/main/images/m2m4.png?raw=true)

重绘帧目录：上面说过的帧保存目录.

帧保存目录(空目录)：重绘后的帧的保存目录.

追加的提示词：在反推提示词的开头或末尾添加的提示词(画风等).

### 合并视频

![m2m5](https://github.com/zhulinyv/SANP-Document/raw/main/images/m2m5.png?raw=true)

重绘帧目录：**逐帧转绘**中填写的帧保存目录.

视频保存目录：任意目录, 但不要和原视频在同一目录.

视频帧率：请根据原视频总帧数和间隔取帧的数量调整至合适大小.

是否并入音频：勾选后, 需要在音频路径填写**音频保存目录**中的音频文件路径.

音频路径：**音频保存目录**中的音频文件路径

## 分块重绘

### 图片上传

![tiled_upscale_add_image](https://github.com/zhulinyv/SANP-Document/raw/main/images/tiled_upscale_add_image.png?raw=true)

点击上方区域上传图片或在下方文本框输入单张图片路径, 相对路径或绝对路径均可.

注意, 当同时上传图片并填写图片路径时, 将优先使用图片路径.

### 重回幅度与接缝合并模型

![tiled_upscale_model](https://github.com/zhulinyv/SANP-Document/raw/main/images/tiled_upscale_model.png?raw=true)

由于分块重绘会将图片拆分成若干个小块后重新拼接, 建议重绘幅度不要超过 0.2.

接缝合并模型默认使用 rife-v2.3, 当选择其它模型时, 将会自动从 huggingface 仓库中下载.

## Enhance

NovelAI 的 Enhance 功能, 本质就是图生图, 甚至重绘幅度是固定的 0.2

## 局部重绘

![inpaint](https://github.com/zhulinyv/SANP-Document/raw/main/images/inpaint.png?raw=true)

### 批量处理

批量处理时, 需要将 "是否启用批处理" 改为 True, 并填写蒙版路径和图片路径.

注意：上传的蒙版应为: 重绘区域为白色, 其余透明而不是黑色, 分辨率等于重绘图像, 批量操作时, 请将图片和蒙版放置于两个文件夹, 并且保证图片和蒙版文件名相同.

### 单张处理

![inpaint_draw](https://github.com/zhulinyv/SANP-Document/raw/main/images/inpaint_draw.png?raw=true)

单张处理时, 请将 "是否启用批处理" 改为 False, 并上传图片.

上传后选择画笔工具和橡皮擦工具可涂抹选择重绘区域.

## 涂鸦重绘

### 涂鸦

![draw_inpaint_draw](https://github.com/zhulinyv/SANP-Document/raw/main/images/draw_inpaint_draw.png?raw=true)

与局部重绘不同的是, 此处的笔刷可以选择更多颜色.

## 导演工具

相比于 NovelAI 官网, 支持了批量操作.

以下为各个功能的图片保存目录.

```
去除背景: output/bg-removal
线条画    output/lineart
素描      output/sketch
上色      output/colorize
表情      output/emotion
整理      output/declutter
```

## 超分降噪

项目默认包含 waifu2x-nv 引擎, 当选择其它引擎时, 会自动从 huggingface 仓库中下载.

每个超分引擎都有一些独立的参数, 不同的超分引擎和不同的参数处理后的图片可能会有细微的差异.

## 自动打码

![mosaic](https://github.com/zhulinyv/SANP-Document/raw/main/images/mosaic.png?raw=true)

三个按钮分别对应三种不同的马赛克样式.

## 添加水印

![watermarks](https://github.com/zhulinyv/SANP-Document/raw/main/images/watermarks.png?raw=true)

使用前, 请先准备一些自己的水印到 `files/watermarks` 文件夹.

项目中附带了两个我的水印, 大家可以删除并添加自己的水印.

## 上传Pixiv

![pixiv](https://github.com/zhulinyv/SANP-Document/raw/main/images/pixiv.png?raw=true)

关于上传 Pixiv, 需要将选择上传的图片或文件夹放到同一个文件夹, 例如 `./output/pixiv`

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

## 图片筛选

![selector](https://github.com/zhulinyv/SANP-Document/raw/main/images/selector.png?raw=true)

此功能可以帮助用户大量生成图片后进行快速筛选.

- 1. 在 "图片目录" 文本框中填写图片的目录, 并点击确定.

- 2. 填写 "输出路径1" 和 "输出路径2", 这两个并非必填, 当使用下方 "移动1" 或 "移动2" 按钮时必填.

- 3. 按钮右侧括号内为快捷键, 你可以通过按下小键盘上的方向键实现快速筛选.

## 抹除数据

### 抹除

![del](https://github.com/zhulinyv/SANP-Document/raw/main/images/del.png?raw=true)

当左侧图片上传区域有图片时, 批量处理路径的内容失效, 将进行单张处理, 需要填写保存目录.

通过上方的复选框, 可自定义选择想要清除的内容.

当勾选伪造信息时, 清除数据后会自动添加类似于生产信息的虚假内容.

当输入的批处理路径与保存目录一样时, 将会直接清除输入目录中图片的元数据.

当输入的批处理路径与保存目录不同时, 输入的批处理目录中的图片仍包含元数据, 清除元数据的图片将保存到下方填写的保存目录.

### 还原

![revert](https://github.com/zhulinyv/SANP-Document/raw/main/images/revert.png?raw=true)

"图片信息文件目录" 内需要放有与 "待还原图片目录" 内图片名称一致的图片或 *.txt 文本文件.

### 导出

![export](https://github.com/zhulinyv/SANP-Document/raw/main/images/export.png?raw=true)

批量处理目录内需要放入包含元数据的图片, 下方的保存目录任意, 读取的正面提示词将保存为与图片同名的 *.txt 文本文件.

## 法术解析

![magic](https://github.com/zhulinyv/SANP-Document/raw/main/images/magic.png?raw=true)

可以将图片拖拽或点击上传来提交图片, 上传后将自动展示图片中包含的数据.

## Tagger

![tagger](https://github.com/zhulinyv/SANP-Document/raw/main/images/tagger.png?raw=true)

通过模型下拉列表可以选择不同的反推模型.

通过调整下方的阈值可以调整反推提示词的数量与精度.

## GPT

![gpt](https://github.com/zhulinyv/SANP-Document/raw/main/images/gpt.png?raw=true)

整合包中的次功能默认关闭, 请前往配置设置页面打开.

## 压缩整理

![zip](https://github.com/zhulinyv/SANP-Document/raw/main/images/zip.png?raw=true)

当 "仅压缩" 时, 建议选择 png 格式, 这样可以压缩图片大小并保留元数据.

当选择 "压缩并整理" 时, 两种格式均可, 生成的 *.xlsx 表格文件将保存到图片同目录.

## 插件商店

![plugin_store](https://github.com/zhulinyv/SANP-Document/raw/main/images/plugin_store.png?raw=true)

所有插件的安装与卸载, 都需要在名称文本框内填写名称.

操作完成后, 点击重启按钮等待重启完成后立即生效.

## 配置设置

![setting](https://github.com/zhulinyv/SANP-Document/raw/main/images/setting.png?raw=true)

所有的配置设置均可通过此处进行设置.

设置后记得保存, 重启后生效.

### 其它

**切换到浅色页面:**

[http://127.0.0.1:11451/?__theme=light](http://127.0.0.1:11451/?__theme=light)

**切换到深色页面:**

[http://127.0.0.1:11451/?__theme=dark](http://127.0.0.1:11451/?__theme=dark)

**Novel AI token 和 Pixiv cookie 的获取方法:**

**⚠️ token 的获取:**

- ![jc](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/82f657fe-81bc-412b-a63c-11a878fde7d2)

**⚠️ pixiv_cookie 和 pixiv_token 的获取:**

- 1.打开 https://www.pixiv.net/illustration/create 并手动上传图片
- 2.选择标签, 年龄限制, AI生成作品, 公开范围, 作品评论功能, 原创作品
- 3.F12 打开控制台并切换到网络视图
- 4.点击投稿
- 5.找到并单击 illustraion, 右侧切换到标头选项
- 6.在请求头部中可以找到 Cookie 和 X-Csrf-Token
- ![97ae3696ad11708ae2eb0474f198de0c](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/e59caaf6-c69d-485e-965d-d7d924397667)


