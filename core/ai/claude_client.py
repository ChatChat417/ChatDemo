# core/ai/claude_client.py

import boto3
import json
import logging
from typing import List, Dict, Optional
from config.security import SecurityConfig


class ClaudeClient:
    def __init__(self):
        """初始化 Claude 客户端"""
        try:
            self.security_config = SecurityConfig()

            # 初始化 AWS 客户端
            self.bedrock = boto3.client(
                service_name="bedrock-runtime",
                aws_access_key_id=self.security_config.aws_access_key_id,
                aws_secret_access_key=self.security_config.aws_secret_access_key,
                region_name=self.security_config.aws_region,
            )

            self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
            logging.info("Claude Client initialized successfully")

        except Exception as e:
            logging.error(f"Failed to initialize Claude Client: {str(e)}")
            raise

    async def chat(self,
                   system_prompt: Optional[str] = None,
                   user_message: str = "",
                   messages: Optional[List[Dict[str, str]]] = None) -> str:
        """
        与 Claude 进行对话

        Args:
            system_prompt: 系统提示词
            user_message: 用户消息
            messages: 历史消息列表

        Returns:
            str: Claude 的回复
        """
        try:
            # 准备消息列表
            formatted_messages = []

            # 处理历史消息
            if messages:
                for msg in messages:
                    # 只添加 user 和 assistant 角色的消息
                    if msg["role"] in ["user", "assistant"]:
                        formatted_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })

            # 如果有系统提示词，将其添加到用户消息中
            current_message = user_message
            if system_prompt:
                current_message = f"{system_prompt}\n\n{user_message}"

            # 添加当前用户消息
            formatted_messages.append({
                "role": "user",
                "content": current_message
            })

            # 调试日志
            logging.debug(f"Formatted messages: {formatted_messages}")

            # 准备请求体
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": formatted_messages,
                "max_tokens": 52,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop_sequences": ["[END]"]
            }

            # 调试信息
            logging.debug(f"Request body: {json.dumps(body, ensure_ascii=False)}")

            # 调用 API
            response = self.bedrock.invoke_model(
                body=json.dumps(body),
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )

            # 解析响应
            response_body = json.loads(response.get("body").read())
            logging.debug(f"Full response: {response_body}")

            # 提取回复内容
            content = response_body.get("content", [{}])[0].get("text", "")

            # 删除可能的停止序列
            if content.endswith("[END]"):
                content = content[:-5].strip()

            return content

        except Exception as e:
            logging.error(f"Error in Claude chat: {str(e)}")
            if hasattr(e, 'response'):
                logging.error(f"Response: {e.response}")
            raise Exception(f"Claude error: {str(e)}")