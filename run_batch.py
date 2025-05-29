from moudle.api import QwenImageAnalyzer
from moudle.batch_processor import process_images_in_folder

API_KEY = "sk-okeezynetvsoihinhuogqlkwftfmpepcwatpkvqurfwbexat"
analyzer = QwenImageAnalyzer(api_key=API_KEY)

prompt = (
    """
    请根据以下规则分析图像并返回格式化结果：
    【输出要求】：
    仅返回以下五项内容，每项一行，格式必须为：
    [长相：...]  
    [头发颜色：...]  
    [特征：...]  
    [衣着：...]  
    [风格：...]
    
    【注意事项】：
    严格执行返回[长相：...]  [头发颜色：...]  [特征：...]  [衣着：...]  [风格：...]这五项的内容
    1. 每一项必须填写，若图像中无法判断，请填写“无”
    2. 严禁省略任何一项
    3. 严禁输出除上述五行之外的任何其他内容
    4. 输出必须完全符合指定格式，包括方括号、冒号、顺序、换行

    【现在开始分析图像】
    """
)

results = process_images_in_folder(
    folder_path="Draw&Guess",
    analyzer=analyzer,
    prompt=prompt,
    save_path="output/result.json"
)
