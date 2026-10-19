# LoRA Bot

## Description

This is an early, local version of the **LoRA-Bot**, a networked generative text-to-image (t2i) stream that can be viewed at [surfacecollider.net/lora-bot](https://surfacecollider.net/lora-bot/).

The project automatically generates images in **Stable Diffusion XL (SDXL)** using [**Automatic1111**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and a custom LoRA. The LoRA is trained on synthetic images rendered in Blender and Three.js.

Each image has a POV description or alt-text, which is stored in a text bank. The script cuts up these passages of writing into fragments and recombines them to form prompts, generating a unique image each iteration.

You can run the project locally on a desktop computer or laptop by following the instructions below.

## Table of Contents
1. [Description](#description)
2. [Models](#models)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Repository Structure](#repository-structure)
6. [Notes](#notes)

## Models

The model weights are not included in this repository. Download them from Hugging Face:

- **LoRA:** [digital_texture-000008.safetensors](https://huggingface.co/surfacecollider/vastai-lora/blob/main/digital_texture-000008.safetensors), trained on the Blender renders and Three.js screenshots described in `text_bank.txt`
- **Base model:** [Stable Diffusion XL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) (`sd_xl_base_1.0.safetensors`), by Stability AI
- **VAE (optional):** [SDXL VAE fp16 fix](https://huggingface.co/madebyollin/sdxl-vae-fp16-fix), by madebyollin, which avoids NaN/black images when running SDXL in half precision

## Installation

1. Clone this repository:
```
git clone https://github.com/jamesairwin/lora-bot.git
```

2. Navigate to the project directory:
```
cd lora-bot
```

3. Set up a virtual environment (recommended):
```
python -m venv venv
```

4. **Activate the virtual environment:**

**Windows:**
```
.\venv\Scripts\activate
```

**macOS/Linux:**
```
source venv/bin/activate
```

5. Install Python dependencies:
```
pip install -r requirements.txt
```

6. The text bank:

The repository includes `text_bank.txt`, which contains the POV descriptions of the 30 training images, one per line. Each line is a comma-separated description, for example:
```
a glossy, crumpled surface, with red, yellow and blue worm-like shapes on a grey background. ...
```

For each prompt, the script picks one comma-separated fragment from each description, shuffles them, and joins six of them into the template `A Blender render of ..., digital texture.` No setup is needed. To use your own descriptions, replace the lines in `text_bank.txt`, keeping one description per line.

7. Add the LoRA:

Download [digital_texture-000008.safetensors](https://huggingface.co/surfacecollider/vastai-lora/blob/main/digital_texture-000008.safetensors) (see [Models](#models)) and copy it into:
```
stable-diffusion-webui/models/Lora/
```

The script expects the file name:
```
digital_texture-000008.safetensors
```

(Change `lora_name` in `main.py` if you use a different LoRA.)

8. Add the base model:

Download `sd_xl_base_1.0.safetensors` from [Stable Diffusion XL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) and copy it into:
```
stable-diffusion-webui/models/Stable-diffusion/
```

Select it as the checkpoint in Automatic1111 before running the script.

## Usage

1. Start Automatic1111 with API mode enabled:

**Windows:**
```
webui-user.bat --api
```

**macOS/Linux:**
```
./webui.sh --api
```

The script uses:
```
http://127.0.0.1:7860
```

Enable progress preview in Automatic1111 (recommended):
**Settings → API → ✔ Allow progress images**

2. Run the script:
```
python main.py
```

The program will:

- Build a new cut-up prompt for each iteration
- Display a **Prompt & Metadata** window
- Stream a **Live Preview** of the evolving SDXL image
- Save each final output to:
```
generated_images/generated_YYYYMMDD-HHMMSS.png
generated_images/generated_YYYYMMDD-HHMMSS.txt
```

Press **Q** in any window to exit.

## Requirements for Automatic1111

Before running the script, ensure:

- **Stable Diffusion XL Base 1.0** is installed in `models/Stable-diffusion/` and selected as the checkpoint
- Optional: **SDXL Refiner**
- The LoRA is placed in `models/Lora/`
- API mode is enabled using `--api`
- Progress images are enabled (for live preview)

## Recommended Settings Used by the Script

- Sampler: `DPM++ 2M Karras` (auto-resolved via API)
- Resolution: 960×1080
- CFG Scale: 17
- Steps: 50
- LoRA Weight: 1.0
- Scheduler: Automatic
- Seed: 252479142 (modify or randomise as desired)

## Repository Structure

```
lora-bot/
│
├── main.py
├── text_bank.txt
├── dataset.json
├── requirements.txt
├── README.md
└── generated_images/    (created on first run)
```

- `text_bank.txt`: the POV descriptions that `main.py` cuts up into prompts.
- `dataset.json`: the 30 training images' filenames paired with their full alt-text. It is not used by `main.py`. The image gallery at [surfacecollider.net/lora-bot](https://surfacecollider.net/lora-bot/) loads it directly from this repository, so it must keep its name and location.

## Notes

- The script loops indefinitely and is suitable for generative installations.
- PNGs are saved exactly as generated by Automatic1111, preserving embedded metadata.
- A separate `.txt` file is saved for each image, enabling easy external cataloguing or reuse.
