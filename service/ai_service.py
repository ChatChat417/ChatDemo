# service/ai_service.py

from core.ai.claude_client import ClaudeClient
from typing import Optional, Dict, List
import logging


class AIService:
    def __init__(self):
        """初始化 AI 服务"""
        try:
            self.claude = ClaudeClient()
            self._chat_history: List[Dict[str, str]] = []
            logging.info("AI Service initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize AI Service: {str(e)}")
            raise

    async def chat(self,
                   user_message: str,
                   system_prompt: Optional[str] = None,
                   messages: Optional[List[Dict[str, str]]] = None,  # 新增参数
                   clear_history: bool = False) -> str:
        """
        处理聊天请求

        Args:
            user_message: 用户消息
            system_prompt: 系统提示词
            messages: 历史消息列表  # 新增参数说明
            clear_history: 是否清除对话历史

        Returns:
            str: AI 的回复
        """
        try:
            if clear_history:
                self._chat_history = []

            # 如果提供了历史消息,使用提供的历史
            if messages is not None:
                self._chat_history = messages.copy()

            # 调用 Claude
            response = await self.claude.chat(
                system_prompt=system_prompt,
                user_message=user_message,
                messages=self._chat_history  # 传递历史消息给 Claude
            )

            # 更新对话历史
            self._chat_history.append({"role": "user", "content": user_message})
            self._chat_history.append({"role": "assistant", "content": response})

            return response

        except Exception as e:
            logging.error(f"Error in chat: {str(e)}")
            raise Exception(f"Chat error: {str(e)}")