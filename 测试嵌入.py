import requests
import numpy as np
API_KEY = "sk-okeezynetvsoihinhuogqlkwftfmpepcwatpkvqurfwbexat"
INPUT_JSON = "output/result.json"
IMAGE_DIR = "images/"

def encode_text_qwen(text, api_key, model="BAAI/bge-m3BAAI/bge-m3"):
    url = "https://api.siliconflow.cn/v1/embeddings"
    payload = {
        "input": text,
        "model": model
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    embedding = response.json()["data"][0]["embedding"]
    return np.array(embedding, dtype=np.float32)

from pymongo import MongoClient
import json


# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ceramic_db"]
collection = db["samples_with_vectors"]

# 加载原始结构化数据
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 遍历记录，生成文本向量
for item in raw_data:
    # 拼接五项特征为一段描述
    description = f"长相：{item.get('长相', '无')}；头发颜色：{item.get('头发颜色', '无')}；特征：{item.get('特征', '无')}；衣着：{item.get('衣着', '无')}；风格：{item.get('风格', '无')}"

    try:
        vector = encode_text_qwen(description, API_KEY)
        item["text_vector"] = vector.tolist()
        item["description"] = description
        item["image_path"] = IMAGE_DIR + item["filename"]

    except Exception as e:
        print(f"❌ 向量提取失败：{item['filename']}，原因：{e}")
        continue

# 批量写入 MongoDB
collection.insert_many(raw_data)
print(f"✅ 共存入 {len(raw_data)} 条记录（带向量）")
