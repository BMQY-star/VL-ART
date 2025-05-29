from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ceramic_db"]
collection = db["multimodal_samples"]

# 检索条件（组合特征）
query = {
    "头发颜色": "",
    "风格": {"$regex": ""}  # 模糊匹配关键词
}

results = list(collection.find(query))
print(results)
# 打印结果
for doc in results:
    print(f"✅ 找到匹配图像：{doc['filename']}，风格：{doc['风格']}")
