import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
import logging


class SecurityConfig:
    def __init__(self, env_path: Optional[str] = None):
        """
        初始化安全配置
        Args:
            env_path: .env 文件路径，默认为项目根目录的 .env 文件
        """
        if env_path:
            load_dotenv(env_path)
        else:
            # 寻找项目根目录的 .env 文件
            current_dir = Path(__file__).resolve().parent
            root_dir = current_dir.parent
            env_path = root_dir / '.env'

            if not env_path.exists():
                raise FileNotFoundError(f"Environment file not found at {env_path}")

            load_dotenv(env_path)

        # 验证必要的 AWS 凭证
        if not self._verify_aws_credentials():
            raise ValueError("Required AWS credentials are missing or invalid")

    def _verify_aws_credentials(self) -> bool:
        """
        验证 AWS 凭证
        Returns:
            bool: 凭证是否有效
        """
        access_key = self.aws_access_key_id
        secret_key = self.aws_secret_access_key

        # 检查凭证是否存在
        if not access_key or not secret_key:
            logging.error("AWS credentials are missing")
            return False

        # 验证凭证格式
        if not isinstance(access_key, str) or not isinstance(secret_key, str):
            logging.error("AWS credentials must be strings")
            return False

        # 验证凭证长度
        if len(access_key) < 16 or len(secret_key) < 16:
            logging.error("AWS credentials appear to be invalid (too short)")
            return False

        # 移除可能的空白字符
        self._aws_access_key_id = access_key.strip()
        self._aws_secret_access_key = secret_key.strip()
        self._aws_region = self.aws_region.strip()

        return True

    @property
    def aws_access_key_id(self) -> str:
        return getattr(self, '_aws_access_key_id', os.getenv('AWS_ACCESS_KEY_ID', ''))

    @property
    def aws_secret_access_key(self) -> str:
        return getattr(self, '_aws_secret_access_key', os.getenv('AWS_SECRET_ACCESS_KEY', ''))

    @property
    def aws_region(self) -> str:
        return getattr(self, '_aws_region', os.getenv('AWS_REGION', 'us-west-2'))

    @property
    def api_key(self) -> str:
        """API 访问密钥"""
        return os.getenv('API_KEY', '')

    def __str__(self) -> str:
        """安全地打印配置信息"""
        return (
            f"AWS Region: {self.aws_region}\n"
            f"AWS Access Key ID: {self.aws_access_key_id[:4]}..."
        )