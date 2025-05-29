import os
import json
from tqdm import tqdm  # ✅ 引入进度条模块
from moudle.api import QwenImageAnalyzer  # 自定义 API 封装类

import re

def parse_result_to_dict(result_text):
    """
    将模型返回的五行格式内容解析为字典。
    """
    result_dict = {}
    # 匹配格式：[标签：内容]
    pattern = r"\[(.+?)：(.*?)\]"

    matches = re.findall(pattern, result_text.strip())
    for key, value in matches:
        result_dict[key.strip()] = value.strip()

    return result_dict



def process_images_in_folder(folder_path, analyzer: QwenImageAnalyzer, prompt: str, save_path=None):
    """
    批量处理文件夹中的图像，调用大模型分析内容，并解析为结构化结果。

    参数：
    - folder_path: 图像所在目录
    - analyzer: QwenImageAnalyzer 实例
    - prompt: 提示词（用于指导模型返回结构化文本）
    - save_path: 可选，保存最终结果到 JSON 文件

    返回：
    - 所有图片的分析结果列表
    """
    results = []
    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
    print(f"🔍 共检测到 {len(image_files)} 张图像。开始处理...\n")

    # ✅ 使用 tqdm 添加进度条
    for filename in tqdm(image_files, desc="🚀 正在处理图像", unit="张"):
        img_path = os.path.join(folder_path, filename)

        try:
            result_text = analyzer.analyze_image(img_path, prompt=prompt)
            print("\n<UNK> <UNK>\n", result_text)
            result_dict = parse_result_to_dict(result_text)
            result_dict["filename"] = filename
            results.append(result_dict)
        except Exception as e:
            print(f"\n❌ 处理失败：{filename}，原因：{e}")

    # ✅ 保存 JSON 文件（可选）
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 所有结果已保存到：{save_path}")

    return results
