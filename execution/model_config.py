"""
模型配置管理器 - 零依赖版本

特点:
1. 不依赖环境变量
2. 不依赖外部配置文件
3. 自动适配 Claude Code 内部调用
4. 降级到 mock 模式（纯方法论脚手架）

优先级:
1. 传入参数（api_key, base_url, model）
2. 环境变量（ANTHROPIC_API_KEY）
3. skill_config.yaml
4. Mock模式（不调用API，返回方法论框架）
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """模型配置数据类"""
    api_key: Optional[str] = None
    base_url: str = "https://api.anthropic.com"
    model: str = "claude-opus-5"
    max_tokens: int = 8000
    temperature: float = 0.7
    mock_mode: bool = False  # 是否启用Mock模式


class ModelConfigManager:
    """模型配置管理器 - 零依赖版"""

    def __init__(self):
        self.skill_root = Path(__file__).parent.parent

    def load_config(self,
                   api_key: Optional[str] = None,
                   base_url: Optional[str] = None,
                   model: Optional[str] = None) -> ModelConfig:
        """
        加载模型配置（零依赖、自动降级）

        优先级:
        1. 传入参数
        2. 环境变量
        3. skill_config.yaml
        4. Mock模式
        """
        config = ModelConfig()

        # 优先级1: 传入参数
        if api_key:
            config.api_key = api_key
        if base_url:
            config.base_url = base_url
        if model:
            config.model = model

        # 优先级2: 环境变量
        if not config.api_key:
            config.api_key = os.getenv('ANTHROPIC_API_KEY')

        # 优先级3: skill_config.yaml（可选）
        if not config.api_key:
            try:
                import yaml
                config_file = self.skill_root / 'skill_config.yaml'
                if config_file.exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        yaml_config = yaml.safe_load(f)
                        api_config = yaml_config.get('api', {})
                        config.api_key = api_config.get('api_key') or config.api_key
                        config.base_url = api_config.get('base_url') or config.base_url
                        config.model = api_config.get('model') or config.model
            except Exception:
                # YAML加载失败，忽略
                pass

        # 优先级4: Mock模式（API密钥仍未设置）
        if not config.api_key:
            config.mock_mode = True
            print("[ModelConfig] WARNING: No API key detected, enabling Mock mode (methodology framework only)")
            print("[ModelConfig]    -> Will return research framework and Prompt templates, not calling Claude API")

        return config


# 便捷函数
def get_config(**kwargs) -> ModelConfig:
    """快速获取配置"""
    manager = ModelConfigManager()
    return manager.load_config(**kwargs)
