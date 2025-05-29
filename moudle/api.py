import requests
import base64
import os

class QwenImageAnalyzer:
    def __init__(self, api_key: str, model_name: str = "Qwen/Qwen2.5-VL-32B-Instruct"):
        self.api_key = api_key
        self.model_name = model_name
        self.url = "https://api.siliconflow.cn/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        base64_image = self.image_to_base64(image_path)

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt  # ✅ 接收外部传入的 prompt
                        }
                    ]
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "enable_thinking": False,
            "thinking_budget": 4096,
            "min_p": 0.05,
            "stop": None,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }

        response = requests.post(self.url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

