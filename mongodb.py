from pymongo import MongoClient
import json

# 连接数据库
client = MongoClient("mongodb://localhost:27017/")
db = client["ceramic_db"]
collection = db["multimodal_samples"]

# 加载你之前保存的 result.json
with open("output/result.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 加入 image_path 字段
for item in raw_data:
    item["image_path"] = f"Draw&Guess/{item['filename']}"
    item["created_at"] = "2025-05-29"  # 可用 datetime.now() 替代
    # item["image_vector"] = [...]     # 如果已提取可加入

# 批量插入
collection.insert_many(raw_data)
print(f"✅ 已导入 {len(raw_data)} 条数据到 MongoDB。")
