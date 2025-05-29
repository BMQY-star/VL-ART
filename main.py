import os
import json
from moudle.api import QwenImageAnalyzer

def parse_result_to_dict(result_text):
    result_dict = {}
    lines = result_text.strip().split("\n")
    for line in lines:
        if line.startswith("[") and "：" in line and line.endswith("]"):
            key_value = line[1:-1].split("：", 1)
            if len(key_value) == 2:
                key, value = key_value
                result_dict[key.strip()] = value.strip()
    return result_dict

def process_images_in_folder(folder_path, analyzer, prompt, save_path=None):
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            try:
                result_text = analyzer.analyze_image(img_path, prompt=prompt)
                result_dict = parse_result_to_dict(result_text)
                result_dict["filename"] = filename
                results.append(result_dict)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    return results
