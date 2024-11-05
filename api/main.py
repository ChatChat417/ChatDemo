# api/main.py

from fastapi import FastAPI, HTTPException
from .models import Character, Scene, ChatRequest
from service.ai_service import AIService
from config.security import SecurityConfig
from typing import List
from prompts.chat.dialogue_control import DialogueControl
import logging
from datetime import datetime

app = FastAPI(
    title="AI RolePlay API",
    description="A simple AI roleplay service using Claude",
    version="1.0.0"
)

# 初始化服务
security_config = SecurityConfig()
ai_service = AIService()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        prompt_data = DialogueControl.build_prompt(
            character=request.character,
            scene=request.scene,
            message_history=request.message_history
        )

        # 简化的prompt，更口语化和调情风格
        system_prompt = f"""{prompt_data['character_info']}

    {prompt_data['context']}

    回复1条简短的约会应用信息（每条最多4个字），开玩笑调情。每条消息包含一个表情符号。保持它轻松愉快和有品位-没有角色扮演或动作描述。专注于巧妙的文字游戏和友好的玩笑，就像在Tinder或类似的应用程序上发信息一样。回答要简短、随意、吸引人.经常使用英文缩写。
    用英文回复
    """

        # 调用 AI 服务
        response = await ai_service.chat(
            user_message=request.message,
            system_prompt=system_prompt,
            messages=prompt_data['messages']
        )

        return {"response": response}

    except KeyError as e:
        logging.error(f"KeyError in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}