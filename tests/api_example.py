import requests
import json


def test_api():
    url = "http://0.0.0.0:8000/api/v1/chat"

    data = {
        "character": {
            "name": "艾莉",
            "background": "一位来自未来世界的AI研究员,在量子计算实验室工作",
            "personality": "聪明、专业、富有同理心,但有时会过于理性"
        },
        "scene": {
            "description": "在一个安静的实验室里,四周是闪烁的量子计算机显示屏",
            "mood": "专注而平静"
        },
        "message": "你好,艾莉,能告诉我你今天在研究什么项目吗?",
        "message_history": []
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Success:", response.json())
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    test_api()