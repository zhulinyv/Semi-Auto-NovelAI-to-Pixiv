<p align="center" >
  <img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/0fbed41e-1b2b-44f4-9562-6eb7aeeb2c7c" width="256" height="256" alt="NJS"></a>
</p>
<h1 align="center">Semi-Auto-NovelAI-to-Pixiv</h1>
<h4 align="center">✨Generate Images with NovelAI and Upload to Pixiv✨</h4>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue">
    <a href="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/raw/main/LICENSE"><img src="https://img.shields.io/github/license/zhulinyv/Semi-Auto-NovelAI-to-Pixiv" alt="license"></a>
    <img src="https://img.shields.io/github/issues/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
    <img src="https://img.shields.io/github/stars/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
    <img src="https://img.shields.io/github/forks/zhulinyv/Semi-Auto-NovelAI-to-Pixiv">
</p>

## 💬 Introduction

**Translated by ChatGPT**

This is a script that generates images with NovelAI, manually selects them, and uploads them to Pixiv.

<details>
<summary><b>See Example Outputs</b></summary>

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d6059625-0640-46dd-97b6-ecbfcb37b646)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/685a034f-e66b-4afd-8e2e-5e0a2ebca709)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/74874ed3-6686-4cd2-b80e-3b3a3dca4b0a)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/5f30cb40-f014-4aff-81ef-f86b02ae2fdb)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/b76c93a0-bddc-4792-8a39-8673c0edc30d)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/f0b4ab5c-3ebb-489c-83b7-3b32676c28ae)

![image](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6b794c4f-2a9a-4d2c-96f1-394c801d880e)

</details>

<p>
    <text>Inspired by my friends: </text> 
    <a href="https://github.com/huliku"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/dc90cc04-7dc0-4dce-968f-39199ca73d4c" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/LittleApple-fp16"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/6d9fefe5-44c0-4b58-a54e-baa1b5aca170" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/CyanAutumn"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/d82e85ee-2468-41bd-95b7-8e732bd291c4" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/wochenlong"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/1e9821ad-aab3-47c1-8528-7f3f70cd722b" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
    <a href="https://github.com/zhulinyv"><img src="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a3cbe72e-67f6-4aa3-a2dd-e936b8bf9cd9" width="50" height="50" style="border-radius:50%; overflow:hidden;"></a>
</p>

Learning Gradio, trying to create a WebUI for this project.

## 💿 Deployment

Make sure you have Python installed and added to the environment variables.

These scripts can be run independently. If needed, expand ↓

<details>
<summary>Outdated (Please run run.bat directly)</summary>

Execute the following commands in the command line one by one:

```
.\venv\Scripts\activate
pip install -r requirements.txt
```

</details>

## ⚙️ Configuration

Before using the project, you need to make a copy of `env.example` and rename it to `.env`, then modify the configuration according to the table below:

| Item | Required | Type | Default | Description | Example |
|:---:|:---:|:---:|:---:|:---:|:---:|
| token |Yes| str | "xxx" | Token required for generating images | "eyJhbG..." |
| img_size |No| int \| list[int] | -1 | Resolution of the generated images | [832, 1216] |
| scale |No| float | 5.0 | Relevance of prompts | 7.0 |
| censor |No| bool | False | Whether to censor the generated images | True |
| sampler |No| str | "k_euler" | Sampler | "k_dpmpp_2m" |
| steps |No| int | 28 | Sampling steps | 20 |
| sm |If sm_dyn is enabled| bool | False | sm | True |
| sm_dyn |No| bool | False | sm_dyn | True |
| noise_schedule |No| str | "native" | Noise schedule | "karras" |
| seed | No | int | -1 | Random seed | 2468751262 |
| magnification | No | float | 1.5 | Magnification for generating images | 1.3 |
| hires_strength | No | float | 0.5 | Redraw strength | 0.6 |
| pixiv_cookie | Yes | str | "xxx" | Cookie for uploading to Pixiv | "first_..." |
| pixiv_token | Yes | str | "xxx" | x-csrf-token for uploading to Pixiv | "655c0c..." |
| allow_tag_edit | No | bool | True | Whether to allow other users to edit tags | False |
| waifu2x_scale | No | int | 2 | Scale for waifu2x | 4 |
| waifu2x_noise | No | int | 3 | Noise reduction level for waifu2x | 2 |
| share | No | bool | False | Whether to share the Gradio link | True |
| height | No | int | 650 | Height of the Gradio interface | 800 |
| port | No | int | 11451 | Port for local deployment | 13579 |

⚠️ Getting the token:

- 1. Log in to https://novelai.net/login
- 2. Press F12 to open the console and switch to the console tab.
- 3. Enter `console.log(JSON.parse(localStorage.session).auth_token)` and press Enter. The returned string is the token.
- ![e3756ce75c6f6850efa633dbaa3a5ae6](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/502c9a49-6a73-446d-9401-e559628ad079)

⚠️ Getting pixiv_cookie and pixiv_token:

- 1. Open https://www.pixiv.net/illustration/create and manually upload an image.
- 2. Choose tags, age restrictions, AI-generated work, public range, comments on works, and original works.
- 3. Press F12 to open the console and switch to the Network tab.
- 4. Click on the submit button.
- 5. Find and click on the 'illustraion' request, then switch to the Headers tab.
- 6. In the request headers, you can find the Cookie and X-Csrf-Token.
- ![97ae3696ad11708ae2eb0474f198de0c](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/e59caaf6-c69d-485e-965d-d7d924397667)

### Other Configurations:

These scripts can be run independently. If needed, expand ↓

<details>
<summary>Outdated (Please run run.bat directly)</summary>

> For generating images, you need to place the images generated by NovelAI in the `.\output\choose_for_i2i` folder.

```
e.g.
Images that need to be enlarged:
.\output
  └---\choose_to_i2i
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
The images after enlargement:
.\output
  └---\i2i
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> For uploading to Pixiv, you need to place the selected images or folders to upload in the `.\output\pixiv` folder.

```
e.g.
.\output
  └---\pixiv
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
        └---\Nahida
              └---5264942125_GenshinImpact_纳西妲.png
              └---4351819919_GenshinImpact_纳西妲.png
```

> For [waifu2x](https://github.com/nagadomi/waifu2x) upscaling, you need to place the images in the `.\output\choose_for_upscale` folder.

```
e.g.
.\output
  └---\choose_to_upscale
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> "For adding mosaic, you need to place the images in the `.\output\mosaic` folder."

```
e.g.
.\output
  └---\mosaic
        └---7589641258_GenshinImpact_可莉.png
        └---6594641258_AzureLane_拉菲.png
```

> For local redraw, you need to place the redrawn images in the `.\output\inpaint\img` folder and the mask images in the `.\output\inpaint\mask` folder.

```
e.g.
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



## 🎉 Use

run `run.bat`

These scripts can be run independently. If needed, expand ↓

<details>
<summary>Outdated (Please run run.bat directly)</summary>

### 1️⃣ Activate the virtual environment

```
.\venv\Scripts\activate
```

### 2️⃣ Select scripts as needed

#### t2i.py

```
python t2i.py
```

Randomly generate NSFW images to `.\output`


#### i2i.py

```
python i2i.py
```

Upscale the images in `.\output\choose_for_i2i` to `.\output\i2i`

#### pixiv.py

```
python pixiv.py
```

Upload images or folders in `.\output\pixiv` to Pixiv

#### waifu2x.py

```
python pixiv.py
```

Upscale images using [waifu2x-ncnn-vulkan](https://github.com/nagadomi/waifu2x-ncnn-vulkan)

![Effect](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/a304d3bd-181f-4d94-ac18-a2c53b9f2f79)

#### mosaic.py

```
python mosaic.py
```

Mosaic key areas

#### inpaint.py

```
python inpaint.py
```

</details>


## 📖 To-Do

+ [x] Batch text-to-image generation
+ [x] Batch image-to-image generation
+ [x] Batch upload to Pixiv
+ [x] Calculate remaining crystals
+ [x] Batch [waifu2x](https://github.com/nagadomi/waifu2x)
+ [x] Batch local redraw
+ [ ] ~~Batch vibe~~
+ [x] Batch mosaic
+ [x] Write a WebUI using Gradio
+ [ ] Containerize the project for persistent running
+ [ ] ...

## 🤝 Acknowledgements

This project uses [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) for denoising and upscaling images.

This project uses [stable-diffusion-inspector](https://spell.novelai.dev/) for parsing image metadata.

This project uses [Genshin-Sync](https://huggingface.co/spaces/AppleHarem/Genshin-Sync/tree/main) for uploading images to Pixiv.

<hr>
<img width="300px" src="https://count.getloli.com/get/@zhulinyv?theme=rule34"></img>
