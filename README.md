# SDXL Cut-Up LoRA Generator

## Description

**SDXL Cut-Up LoRA Generator** is an automated image-generation system that uses **Stable Diffusion XL (SDXL)** running in **Automatic1111** together with a **custom LoRA** trained on synthetic Blender renders.  
Each Blender render in the training dataset includes **alt-text POV descriptions**, and these textual descriptions become a **text bank** from which the Python script builds new prompts using a *cut-up* generative technique.

The script automatically:

- Loads POV/descriptive text fragments  
- Cuts, recombines, and shuffles them  
- Generates prompts in the format:  
  **“A Blender render of {fragments}, digital texture.”**  
- Sends the prompt to Automatic1111 via the **txt2img API**  
- Applies your custom LoRA with a specified weight  
- Shows a **live evolving preview** of the SDXL diffusion process  
- Displays a **styled prompt window**  
- Saves the final PNG *with full metadata intact*  
- Saves a matching `.txt` metadata file  
- Loops indefinitely to produce an evolving stream of images

This project is intended for artistic, generative, or installation-based workflows requiring continuous, algorithmic production of images from textual recombination.

---

## Table of Contents
1. [Description](#description)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Requirements for Automatic1111](#requirements-for-automatic1111)

---

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/sdxl-cutup-lora-generator.git
   ```
   
2. **Navigate to the project directory:**

    ```bash
    cd sdxl-cutup-lora-generator
    ```

3. **Set up a virtual environment (recommended):**

   ```bash
   python -m venv venv
   ```


4. **Activate the virtual environment:**

Windows:

.\venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Install Python dependencies:

pip install -r requirements.txt


Add your text bank:

Create a file named text_bank.txt in the project root.
Each line should be a descriptive fragment taken from your POV alt-text dataset, e.g.:

reflective polymer surface catching occlusion shadows, volumetric haze
matte sandstone lattice structure viewed from the ground looking upward
bioluminescent surface glow diffusing across curved geometry
