import gradio as gr
import requests
import json
from typing import List, Dict


class RolePlayChat:
    def __init__(self, api_url: str = "http://localhost:8000/api/v1/chat"):
        self.api_url = api_url
        self.message_history: List[Dict] = []

        # 预设角色列表
        self.preset_characters = {
            "Jake (Musician)": {
                "name": "Jake",
                "background": "Bass player in a local band, loves late night adventures",
                "personality": "Spontaneous, flirty, loves making people laugh",
                "greeting": "hey there 😉"
            },
            "Emma (Model)": {
                "name": "Emma",
                "background": "Part-time model and photography enthusiast",
                "personality": "Confident, playful, enjoys good banter",
                "greeting": "hi cutie ✨"
            },
            "Alex (Bartender)": {
                "name": "Alex",
                "background": "Mixologist at an upscale lounge, knows all the best spots",
                "personality": "Charming, smooth talker, good at reading people",
                "greeting": "what's up? 😏"
            },
            "Sophia (Dancer)": {
                "name": "Sophia",
                "background": "Professional dancer teaching at a studio",
                "personality": "Flirtatious, graceful, loves good vibes",
                "greeting": "heyyy 💋"
            }
        }

    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(theme=gr.themes.Soft()) as interface:
            with gr.Row():
                with gr.Column(scale=1):
                    # 角色设置区
                    with gr.Group():
                        gr.Markdown("### 角色设置")
                        char_preset = gr.Dropdown(
                            choices=list(self.preset_characters.keys()),
                            label="选择预设角色",
                            value=list(self.preset_characters.keys())[0]
                        )
                        char_name = gr.Textbox(label="角色名称")
                        char_background = gr.Textbox(label="角色背景", lines=3)
                        char_personality = gr.Textbox(label="角色性格", lines=2)
                        char_greeting = gr.Textbox(
                            label="打招呼用语",
                            lines=2,
                            placeholder="输入角色的打招呼用语..."
                        )

                    # 场景设置
                    with gr.Group():
                        gr.Markdown("### 场景设置")
                        scene_desc = gr.Textbox(
                            label="场景描述",
                            value="在一个安静的实验室里,四周是闪烁的量子计算机显示屏",
                            lines=2
                        )
                        scene_mood = gr.Textbox(
                            label="场景氛围",
                            value="专注而平静"
                        )

                    # 控制按钮区
                    with gr.Group():
                        gr.Markdown("### 控制")
                        with gr.Row():
                            start_chat_btn = gr.Button("开始对话", variant="primary")
                            clear_btn = gr.Button("清除对话")

                with gr.Column(scale=2):
                    # 聊天区域
                    chatbot = gr.Chatbot(label="对话历史")
                    msg = gr.Textbox(
                        label="发送消息",
                        placeholder="在这里输入你的消息...",
                        lines=2
                    )
                    with gr.Row():
                        send_btn = gr.Button("发送", variant="primary")

            # 事件处理
            char_preset.change(
                self.load_preset_character,
                inputs=[char_preset],
                outputs=[char_name, char_background, char_personality, char_greeting]
            )

            start_chat_btn.click(
                self.start_chat,
                inputs=[char_name, char_background, char_personality, char_greeting,
                        scene_desc, scene_mood, chatbot],
                outputs=[chatbot]
            )

            send_btn.click(
                self.send_message,
                inputs=[
                    msg, char_name, char_background, char_personality,
                    scene_desc, scene_mood, chatbot
                ],
                outputs=[msg, chatbot]
            )

            clear_btn.click(
                self.clear_history,
                outputs=[chatbot]
            )

            # 支持按回车发送
            msg.submit(
                self.send_message,
                inputs=[
                    msg, char_name, char_background, char_personality,
                    scene_desc, scene_mood, chatbot
                ],
                outputs=[msg, chatbot]
            )

        return interface

    def load_preset_character(self, preset_name: str):
        """加载预设角色信息"""
        if preset_name in self.preset_characters:
            char = self.preset_characters[preset_name]
            return [
                char["name"],
                char["background"],
                char["personality"],
                char["greeting"]
            ]
        return ["", "", "", ""]

    def start_chat(
            self, char_name: str, char_background: str,
            char_personality: str, char_greeting: str,
            scene_desc: str, scene_mood: str,
            chat_history: List
    ):
        """开始新对话"""
        self.clear_history()

        # 使用打招呼用语开始对话
        data = {
            "character": {
                "name": char_name,
                "background": char_background,
                "personality": char_personality
            },
            "scene": {
                "description": scene_desc,
                "mood": scene_mood
            },
            "message": "你好",
            "message_history": []
        }

        try:
            # 如果有自定义打招呼用语，直接使用
            if char_greeting.strip():
                chat_history.append((None, char_greeting))
                self.message_history.append({
                    "role": "assistant",
                    "content": char_greeting
                })
            else:
                # 否则调用 API 获取回复
                response = requests.post(self.api_url, json=data)
                response.raise_for_status()

                ai_message = response.json()["response"]
                chat_history.append((None, ai_message))
                self.message_history.append({
                    "role": "assistant",
                    "content": ai_message
                })

            return chat_history

        except Exception as e:
            print(f"Error: {e}")
            return chat_history + [(None, f"发生错误: {str(e)}")]

    def send_message(
            self, message: str, char_name: str, char_background: str,
            char_personality: str, scene_desc: str, scene_mood: str,
            chat_history: List
    ):
        """发送消息并获取回复"""
        if not message.strip():
            return "", chat_history

        # 准备请求数据
        data = {
            "character": {
                "name": char_name,
                "background": char_background,
                "personality": char_personality
            },
            "scene": {
                "description": scene_desc,
                "mood": scene_mood
            },
            "message": message,
            "message_history": self.message_history
        }

        try:
            # 调用 API
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()

            # 更新对话历史
            ai_message = response.json()["response"]
            self.message_history.append({"role": "user", "content": message})
            self.message_history.append({"role": "assistant", "content": ai_message})

            # 更新界面对话历史
            chat_history.append((message, ai_message))

            return "", chat_history

        except Exception as e:
            print(f"Error: {e}")
            return "", chat_history + [(message, f"发生错误: {str(e)}")]

    def clear_history(self):
        """清除对话历史"""
        self.message_history = []
        return None


# 启动应用
if __name__ == "__main__":
    chat_app = RolePlayChat()
    interface = chat_app.create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )