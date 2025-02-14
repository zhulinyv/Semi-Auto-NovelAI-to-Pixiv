<p align="center" >
  <img src="https://socialify.git.ci/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/image?description=1&descriptionEditable=%E2%9C%A8%E5%B8%A6%E6%9C%89%20WebUI%20%E7%9A%84%20NovelAI%20%E9%87%8F%E4%BA%A7%E5%B7%A5%E5%85%B7%E2%9C%A8&font=KoHo&forks=1&issues=1&language=1&logo=https%3A%2F%2Fi.postimg.cc%2FTwffWVkX%2F00003-XYTPZ-520621529-1x1-waifu2x-1000x1000-3n-png.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto" alt="Semi-Auto-NovelAI-to-Pixiv" width="640" height="320" />
</p>

<img decoding="async" align=right src="https://i.postimg.cc/0jSHMMJm/kb.png" width="35%">

## 💬 Introduction

**Chinese document: [README.md](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/README.md)**

- This is a magical project that achieves batch image generation, which NovelAI itself cannot accomplish!
  
- It not only generates images but also integrates various practical functions into one super user interface!

- **If you encounter any issues during usage, please join the QQ group for consultation: [559063963](https://qm.qq.com/cgi-bin/qm/qr?k=I9FqVFb_wn-y5Ejid9CIae57KLLlvDuj&jump_from=webapi&authKey=i+DvSe2nFRBsKNu+D9NK0sFd7Qr1u/vakfRUFDGDCWaceBQOsuiHwkxDa3kRLfup)**

> [!TIP]
> On that day, heavy rain poured, thunder roared, and the wind was noisy, as if the whole world was trembling for some unknown force.

✨ **Functions currently implemented by Cheese:**

### [https://sanp-docs.netlify.app](https://sanp-docs.netlify.app/)

### 🔌 Plugins

- Implementation of dynamically loading plugins to enhance the project's scalability!

- Plugins submitted to the store: [Plugin List](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/webui/files/plugins.json)

> [!TIP]
> I walked alone on the slippery and muddy streets, with only a few street lamps blinking lonely in the dark night.

## 💿 Deployment

### 💻 Configuration Requirements

- Extremely low configuration requirements for the ultimate user experience!

| Item | Description |
|:---:|:---:|
| NovelAI Membership | To generate images infinitely, it is recommended to have a $25/month membership. |
| Network | To successfully send POST requests, please make sure that you can access these website: [novelai.net](https://novelai.net), [huggingface.co](https://huggingface.co), [github.com](https://github.com) |
| 1GB VRAM | At least 1GB of VRAM is required to use all engines for super-resolution denoising. |
| 2GB RAM | At least 2GB of RAM is required for smooth operation of this project. |
| Windows 10/11(x64) | To use all features, a 64-bit version of Windows 10/11 is required. |
| [Microsoft Visual C++ 2015](https://www.microsoft.com/en-us/download/details.aspx?id=53587) | Installation of the runtime library is required to use all engines for super-resolution denoising. |

> [!WARNING]
> In the distance, a few cat cries came, as if the only notes of the night, the darkness desolate, the biting cold wind, desolate and lonely.

### 🎉 Getting Started with Deployment

#### 0️⃣ Star this project

- If you enjoy this project, please consider giving it a Star🌟. It's the greatest motivation for the developers.

#### 1️⃣ Install Python

- I recommend installing [Python 3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe). During installation, please ensure to check the option **Add Python to PATH**, and keep the rest as **default**.

#### 2️⃣ Install Git

- Suggested to install [Latest Version](https://git-scm.com/download/win), you just need to click **Next** button.

#### 3️⃣ Clone Repositories

- Open cmd or powershell, run `git clone -b main --depth=1 https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv.git`

#### 4️⃣ Next step

- Now you can launch the `run.bat` at the origin directory to start WebUI, it will create the virtual environment and install the dependences at the first time, it will take a long time, so you can drink some coffe or read the documents below

#### 5️⃣ Modpack download

If you find it difficult to get started or have problems with the above operations, please join the group to consult or download the modpack [Semi-Auto-NovelAI-to-Pixiv](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/releases/tag/modpack)

To unzip and use, modpack users need to run `Modpack launcher.bat`

> [!TIP]
> Moonlight seeps through sparse clouds, casting its glow upon the ground, sketching out a scene of ethereal beauty.

## ⚙️ Configuration

- ⚠️ 1. If you have started the WebUI but haven't performed necessary configurations, please navigate to the settings page for necessary configurations.

- ⚠️ 2. Please do not skip this step, it's crucial. Make sure you have reviewed all configurations thoroughly.

- ⚠️ 3. Alternatively, you can directly edit the `.env` file for configurations.

> [!WARNING]
> The cries of those cats, sometimes distant, sometimes drawing near, leaving uncertainty about the path ahead.

⚠️ Getting the token:

- ![jc](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/82f657fe-81bc-412b-a63c-11a878fde7d2)

⚠️ Getting pixiv_cookie and pixiv_token:

- 1. Open https://www.pixiv.net/illustration/create and manually upload an image.
- 2. Choose tags, age restrictions, AI-generated work, public range, comments on works, and original works.
- 3. Press F12 to open the console and switch to the Network tab.
- 4. Click on the submit button.
- 5. Find and click on the 'illustraion' request, then switch to the Headers tab.
- 6. In the request headers, you can find the Cookie and X-Csrf-Token.
- ![97ae3696ad11708ae2eb0474f198de0c](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/assets/66541860/e59caaf6-c69d-485e-965d-d7d924397667)

## 🌟 Usage

- **Run `run.bat`, it will automatically open the default browser and navigate to [127.0.0.1:11451](http://127.0.0.1:11451)**

- For old version users: It's no longer recommended to run individual scripts. Please use the WebUI.

- If it's really necessary (for example, if the browser has added the sleep whitelist but cannot continue generating on an inactive page), please configure the directory and other parameters in the WebUI and click **Generate Standalone Scripts** (you can also read the source code to write standalone scripts by yourself), then run **run_stand_alone_scripts.bat** in the root directory.

- For plugin development, please refer to: [Wiki](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/wiki/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91)

> [!TIP]
> Above is endless darkness, below is endless darkness, as if trapped in an endless vortex.

## 📖 To-Do

> [!TIP]
> Darkness is like invisible hands, tightly embracing me, deeply devouring my thoughts.

<details>
<summary><b>展开查看待办列表</b></summary>

+ [x] Batch text-to-image generation
+ [x] Batch image-to-image generation
+ [x] Batch upload to Pixiv
+ [x] Calculate remaining crystals
+ [x] Batch [waifu2x](https://github.com/nagadomi/waifu2x)
+ [x] Batch local redraw
+ [x] ~~Batch vibe~~
+ [x] Batch mosaic
+ [x] Write a WebUI using Gradio
+ [ ] ~~Containerize the project for persistent running~~
+ [x] Change the style of the interface
+ [x] ~~Add ChatGPT~~
+ [x] ~~White a picture selector~~
+ [ ] ~~Get token by account and password~~
+ [x] Add more upscale engine
+ [x] Add more ways to t2i
+ [x] Batch watermarking
+ [x] Batch PNG info processing
+ [x] Configuration item interface
+ [x] Open related folders functionality
+ [x] Merge interfaces such as random NSFW
+ [x] Hotkey for quick image filtering
+ [x] Tutorial and instruction pages
+ [x] Custom plugins
+ [x] Automatically generate standalone script
+ [x] Specify the number of Text-to-Image outputs
+ [x] Wensheng diagram seed click to switch randomly
+ [x] Add whether to restore image information in the configuration item
+ [x] Complete independent script generation
+ [x] Picture save category
+ [x] Support for non-literate diagram plugins
+ [x] Video redrawing
+ [x] Prompts inferr
+ [x] Tile upscale
+ [ ] ~~Add more interpolation engines~~
+ [x] Translate the rest of the page
+ [x] Auto updata
+ [x] Plugins store
+ [x] Custom eraser meta data
+ [x] Auto install plugins
+ [x] Proxy setting
+ [x] Batch enhance
+ [ ] ~~Custom save path~~
+ [ ] Learn the C# and write a luncher with wpfui
+ [x] Yolo detects Ensford
+ [x] Activate Loggo (even added a beep)
+ [x] Rename functions and variables
+ [x] T2I interrupt
+ [x] The list of plugins reads the remote repository
+ [x] Plugin updates and uninstallations
+ [x] Add copy operations for image filtering
+ [x] Modpacks
+ [x] New mosaic
+ [x] Partial redraw to optimize mask upload
+ [x] Graffiti repaint
+ [ ] ~~Partial zoom in and repaint~~
+ [x] Image compression and categorization
+ [ ] Vibe save style
+ [x] Fallback Vibe random chart
+ [x] Simplification of Favorit. Edited by Ethan
+ [ ] Learn to write an autocomplete for Is
+ [x] Simplify Vibe image uploading
+ [ ] Custom resolution
+ [x] Sound
+ [ ] Connect to stable-diffusion-webui
+ [ ] ...

</details>

## 🤝 Acknowledgements

This project uses [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) | [Anime4KCPP](https://github.com/TianZerL/Anime4KCPP) | [realcugan-ncnn-vulkan](https://github.com/nihui/realcugan-ncnn-vulkan/) | [realesrgan-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | [realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan/) | [srmd-cuda](https://github.com/MrZihan/Super-resolution-SR-CUDA) | [srmd-ncnn-vulkan](https://github.com/nihui/srmd-ncnn-vulkan) | [waifu2x-caffe](https://github.com/lltcggie/waifu2x-caffe) | [waifu2x-converter](https://github.com/DeadSix27/waifu2x-converter-cpp) for denoising and upscaling images.

This project uses [Genshin-Sync](https://huggingface.co/spaces/AppleHarem/Genshin-Sync/tree/main) for uploading images to Pixiv.

This project uses [GPT4FREE](https://github.com/xtekky/gpt4free) to provide GPT services.

This project uses [novelai-image-metadata](https://github.com/NovelAI/novelai-image-metadata) to eraser the metadata.

This project uses [SmilingWolf/wd-tagger](https://huggingface.co/spaces/SmilingWolf/wd-tagger) to inferr Prompts.

This project uses [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) to process tile redrawing slice seams.

This project uses some of the art style strings provided by the [3300画风法典] (https://docs.qq.com/sheet/DZWZMemxNZkpVR0VB).

This item uses a variety of actions provided by [涩涩法典梦神版](QQ:3298853270).


> [!NOTE]
> Falling, falling.

## 🔊 Declaration

Disclaimer: **This software only provides technical services, and the developer is not responsible for any legal liability or loss that may arise from the user's use of this software, and the user shall be fully responsible for its use of this software and its results**

<p align="center" >
  <a href="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/CODE_OF_CONDUCT.md"><b>Code of conduct</b></a> | <a href="https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/blob/main/SECURITY.md"><b>Security</b></a>
</p>

<hr>
<img src="https://count.getloli.com/@zhulinyv?name=zhulinyv&theme=moebooru-h&padding=6&offset=0&align=top&scale=1.5&pixelated=1&darkmode=auto&prefix=769854"></img>

<!-- <a href="https://smms.app/image/ydhHvFDw53GCAfj" target="_blank"><img src="https://s2.loli.net/2022/08/28/ydhHvFDw53GCAfj.png" alt="skirt.png"></a> -->
