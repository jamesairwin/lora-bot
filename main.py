import os
import random
import time
import base64
import requests
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import threading

# Load text bank from a file
def load_text_bank(file_path):
    """Loads text from a file and returns it as a list of lines."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text_bank = [line.strip() for line in file.readlines() if line.strip()]
        return text_bank
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

def generate_prompt(text_bank):
    """
    Generates a cut-up style prompt by mixing and matching fragments from multiple descriptions.
    """
    fragments = []
    for desc in text_bank:
        split_desc = desc.split(', ')
        if len(split_desc) > 1:
            fragments.append(random.choice(split_desc))
    
    random.shuffle(fragments)
    main_description = ', '.join(fragments[:6])
    return f"A Blender render of {main_description}, digital texture."

def get_exact_sampler_name(target_name):
    """Gets the exact case-sensitive sampler name from A1111."""
    try:
        samplers_url = "http://127.0.0.1:7860/sdapi/v1/samplers"
        response = requests.get(samplers_url)
        response.raise_for_status()
        samplers = response.json()
        for sampler in samplers:
            if sampler["name"].lower() == target_name.lower():
                return sampler["name"]
        print(f"Warning: Sampler '{target_name}' not found. Using '{target_name}' as given.")
        return target_name
    except Exception as e:
        print("Error fetching samplers:", e)
        return target_name

def generate_image_with_preview(prompt):
    """Generates an image and shows live preview updates."""
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    progress_url = "http://127.0.0.1:7860/sdapi/v1/progress?skip_current_image=false"

    exact_sampler = get_exact_sampler_name("DPM++ 2M Karras")

    lora_name = "digital_texture-000008"
    lora_weight = 1.0
    full_prompt = f"<lora:{lora_name}:{lora_weight}> {prompt}"

    payload = {
        "prompt": full_prompt,
        "steps": 50,
        "width": 960,
        "height": 1080,
        "sampler_name": exact_sampler,
        "scheduler": "Automatic",
        "cfg_scale": 17,
        "n_iter": 1,
        "batch_size": 1,
        "seed": 252479142
    }

    result = {}
    thread_exception = None

    def run_generation():
        nonlocal result, thread_exception
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            thread_exception = e

    gen_thread = threading.Thread(target=run_generation)
    gen_thread.start()

    preview_image = None
    while gen_thread.is_alive():
        try:
            progress_resp = requests.get(progress_url)
            progress_data = progress_resp.json()
            if "current_image" in progress_data and progress_data["current_image"]:
                image_data = base64.b64decode(progress_data["current_image"])
                image_array = np.frombuffer(image_data, dtype=np.uint8)
                preview_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                if preview_image is not None:
                    cv2.namedWindow("Live Preview", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Live Preview", 960, 1080)
                    cv2.imshow("Live Preview", preview_image)
                    cv2.waitKey(1)
        except Exception as e:
            print("Error fetching progress:", e)
        time.sleep(0.5)

    gen_thread.join()
    if thread_exception:
        print("Error during image generation:", thread_exception)
        return None, None

    if "images" not in result or not result["images"]:
        print("No image returned in result")
        return None, None

    # Keep raw PNG data (with metadata)
    final_image_data = base64.b64decode(result["images"][0])

    # Also decode a copy for display
    final_image_array = np.frombuffer(final_image_data, dtype=np.uint8)
    final_image = cv2.imdecode(final_image_array, cv2.IMREAD_COLOR)

    return final_image, final_image_data

def wrap_text(text, font, max_width, draw):
    """Wrap text so that each line is within max_width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def display_prompt_window(prompt_text):
    """Displays the prompt in a separate styled window."""
    img_width, img_height = 400, 350
    margin = 20
    max_text_width = img_width - 2 * margin

    image = Image.new("RGB", (img_width, img_height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("WorkSans-Medium.ttf", 18)
    except IOError:
        print("TrueType font not found. Using default font.")
        font = ImageFont.load_default()

    text_color = (255, 255, 255)
    wrapped_lines = wrap_text(prompt_text, font, max_text_width, draw)

    y_offset = margin
    for line in wrapped_lines:
        bbox = draw.textbbox((margin, y_offset), line, font=font)
        text_height = bbox[3] - bbox[1]
        draw.text((margin, y_offset), line, font=font, fill=text_color)
        y_offset += text_height + 10

    cv2.imshow("Prompt & Metadata", np.array(image))

def save_image(final_image_data, prompt):
    """Saves PNG with metadata intact + separate .txt metadata file."""
    folder = "generated_images"
    os.makedirs(folder, exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = os.path.join(folder, f"generated_{timestamp}.png")
    metadata_path = os.path.join(folder, f"generated_{timestamp}.txt")

    # Save PNG exactly as returned by A1111 (with metadata)
    with open(image_path, "wb") as f:
        f.write(final_image_data)

    # Save prompt to text file
    with open(metadata_path, "w", encoding="utf-8") as meta_file:
        meta_file.write(f"Prompt: {prompt}\n")

    print(f"Saved image with metadata: {image_path}")
    print(f"Saved prompt metadata: {metadata_path}")

def main():
    text_bank = load_text_bank("text_bank.txt")
    if not text_bank:
        return

    while True:
        prompt = generate_prompt(text_bank)

        # --- Safe prompt display ---
        try:
            display_prompt_window(prompt)
        except Exception as e:
            print("Warning: Could not display prompt window:", e)
        # ---------------------------

        final_image, final_image_data = generate_image_with_preview(prompt)
        if final_image is None or final_image_data is None:
            print("Error generating image. Skipping...")
            continue

        save_image(final_image_data, prompt)

        cv2.imshow("Final Image", final_image)
        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
