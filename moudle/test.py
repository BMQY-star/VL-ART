from moudle.api import QwenImageAnalyzer

API_KEY = "sk-okeezynetvsoihinhuogqlkwftfmpepcwatpkvqurfwbexat"
analyzer = QwenImageAnalyzer(api_key=API_KEY)

# ✅ 定义测试用 Prompt
prompt = (
    "请分析这张图片，并以以下格式返回五项内容，每项一行：\n"
    "[长相：...]\n"
    "[头发颜色：...]\n"
    "[特征：...]\n"
    "[衣着：...]\n"
    "[风格：...]\n"
    "[人数：...]\n"
    "[动作：...]\n"
    "不要输出其他内容。"
)

# ✅ 测试一张图片
image_path = "../Draw&Guess/2d1e84732e04fbd0f4e89a929735462.jpg"
result = analyzer.analyze_image(image_path, prompt=prompt)
print("\n🧠 模型返回内容：\n", result)
