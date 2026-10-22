# LoRA Bot

## Description

This repository contains an early, local version of **LoRA Bot**, a networked generative text-to-image (t2i) stream. The live work runs at [surfacecollider.net/lora-bot](https://surfacecollider.net/lora-bot/). This version runs on your own computer.

The project automatically generates images in **Stable Diffusion XL (SDXL)** using [**Automatic1111**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and a custom LoRA. The LoRA is trained on synthetic images rendered in Blender and three.js.

Each image has a POV description or alt-text, which is stored in a text bank. The script cuts up these passages of writing into fragments and recombines them to form prompts, generating a unique image each iteration.

You can run the project locally on a desktop computer or laptop by following the instructions below.

### How the prompts are made

`text_bank.txt` contains the POV descriptions of the 30 training images, one per line. Each line is a comma-separated description, for example:

```
a glossy, crumpled surface, with red, yellow and blue worm-like shapes on a grey background. ...
```

For each prompt, the script picks one comma-separated fragment from each description, shuffles them, and joins six of them into the template `A Blender render of ..., digital texture.` To use your own descriptions, replace the lines in `text_bank.txt`, keeping one description per line.

## Table of Contents
1. [Description](#description)
2. [The Local Version and the Live Work](#the-local-version-and-the-live-work)
3. [Models](#models)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Recommended Settings Used by the Script](#recommended-settings-used-by-the-script)
7. [Repository Structure](#repository-structure)
8. [Notes](#notes)

## The Local Version and the Live Work

This repository and the live LoRA Bot are linked, but they are not the same piece of software.

**Shared by both:**

- The custom LoRA, trained on 30 Blender renders and three.js screenshots
- `text_bank.txt`, the POV descriptions of those 30 images
- The cut-up method: each prompt is assembled from fragments of those descriptions
- `dataset.json`, the training images and their alt-text. The Training Dataset gallery on the LoRA Bot page loads this file directly from this repository.

**Different:**

- **Where it runs:** the live work runs on an NVIDIA 3090 GPU, rented on demand through a VPS for each generation session. This version runs through Automatic1111 on your own machine.
- **How it starts:** the live work is triggered from the LoRA Bot page and is password protected. This version starts when you run `main.py` and loops until you press **Q**.
- **Where the images go:** the live work streams its images to the web page. This version shows them in a local preview window and saves each one to `generated_images/`.

## Models

The model weights are not included in this repository. Download them from Hugging Face:

- **LoRA:** [digital_texture-000008.safetensors](https://huggingface.co/surfacecollider/vastai-lora/blob/main/digital_texture-000008.safetensors), trained on the Blender renders and three.js screenshots described in `text_bank.txt`
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

4. Activate the virtual environment:

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

6. Add the LoRA (see [Models](#models)) to:

   ```
   stable-diffusion-webui/models/Lora/
   ```

   The script expects the file name `digital_texture-000008.safetensors`. Change `lora_name` in `main.py` if you use a different LoRA.

7. Add the base model (see [Models](#models)) to:

   ```
   stable-diffusion-webui/models/Stable-diffusion/
   ```

   Select it as the checkpoint in Automatic1111 before running the script.

## Usage

1. Start Automatic1111 with API mode enabled:

   **Windows:** open `webui-user.bat` in a text editor, change the `COMMANDLINE_ARGS` line to:

   ```
   set COMMANDLINE_ARGS=--api
   ```

   then run `webui-user.bat`.

   **macOS/Linux:**

   ```
   ./webui.sh --api
   ```

   The script connects to Automatic1111 at `http://127.0.0.1:7860`.

   The script's **Live Preview** window reads Automatic1111's in-progress image, so keep live previews enabled in Automatic1111's settings (they are on by default).

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

`dataset.json` is not used by `main.py`, but the website's gallery loads it from this repository, so it must keep its name and location.

## Notes

- The script is suitable for generative installations.
- PNGs are saved exactly as generated by Automatic1111, preserving embedded metadata.
- A separate `.txt` file is saved for each image, enabling easy external cataloguing or reuse.
