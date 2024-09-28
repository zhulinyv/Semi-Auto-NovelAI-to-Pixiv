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

- 关于随机蓝图, 请前往 ./files/favorite 自行添加配置:

```py
actions.yaml:     动作
artists.yaml:     画风
characters.yaml:  角色
emotions.yaml:    表情
negative.yaml:    负面
prefixes.yaml:    质量词
stains.yaml:      污渍
surroundings.yaml 场景
```
