"""
模型配置管理器：支持多平台调用的模型配置

支持的配置方式（优先级从高到低）：
1. 代码传入参数
2. skill_config.yaml中的model配置
3. 环境变量
4. Claude Code settings.json
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional, Any


class ModelConfig:
    """模型配置类"""

    def __init__(self,
                 provider: str = "anthropic",
                 model: str = "claude-sonnet-5",
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 max_tokens: int = 2048,
                 temperature: float = 0.7):
        """
        初始化模型配置

        Args:
            provider: 模型提供商 (anthropic, openai, azure, custom)
            model: 模型ID
            api_key: API密钥
            base_url: API Base URL（用于中转站或自定义端点）
            max_tokens: 最大token数
            temperature: 温度参数
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature


class ModelConfigManager:
    """
    模型配置管理器

    负责从多个来源读取和管理模型配置
    """

    def __init__(self, skill_root: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            skill_root: skill根目录（用于读取skill_config.yaml）
        """
        self.skill_root = skill_root or Path(__file__).parent.parent
        self.config_file = self.skill_root / "skill_config.yaml"

    def load_config(self,
                   provider: Optional[str] = None,
                   model: Optional[str] = None,
                   api_key: Optional[str] = None,
                   base_url: Optional[str] = None) -> ModelConfig:
        """
        加载模型配置（按优先级）

        优先级：
        1. 代码传入参数（最高优先级）
        2. skill_config.yaml中的model配置
        3. 环境变量
        4. Claude Code settings.json（最低优先级）

        Args:
            provider: 模型提供商（代码传入）
            model: 模型ID（代码传入）
            api_key: API密钥（代码传入）
            base_url: API Base URL（代码传入）

        Returns:
            ModelConfig: 模型配置对象
        """
        # 优先级1: 代码传入参数
        config = {
            'provider': provider,
            'model': model,
            'api_key': api_key,
            'base_url': base_url
        }

        # 优先级2: 从skill_config.yaml读取
        yaml_config = self._load_from_yaml()

        # 优先级3: 从环境变量读取
        env_config = self._load_from_env()

        # 优先级4: 从Claude Code settings.json读取
        claude_config = self._load_from_claude_settings()

        # 合并配置（优先级从高到低）
        final_config = {}
        for key in ['provider', 'model', 'api_key', 'base_url', 'max_tokens', 'temperature']:
            final_config[key] = (
                config.get(key) or
                yaml_config.get(key) or
                env_config.get(key) or
                claude_config.get(key)
            )

        # 设置默认值
        if not final_config['provider']:
            final_config['provider'] = 'anthropic'
        if not final_config['model']:
            final_config['model'] = 'claude-sonnet-5'
        if not final_config['max_tokens']:
            final_config['max_tokens'] = 2048
        if not final_config['temperature']:
            final_config['temperature'] = 0.7

        return ModelConfig(**final_config)

    def _load_from_yaml(self) -> Dict[str, Any]:
        """从skill_config.yaml读取配置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'model' in data:
                        return data['model']
        except Exception:
            pass
        return {}

    def _load_from_env(self) -> Dict[str, Any]:
        """从环境变量读取配置"""
        return {
            'api_key': os.environ.get('ANTHROPIC_API_KEY'),
            'base_url': os.environ.get('ANTHROPIC_BASE_URL'),
            'model': os.environ.get('ANTHROPIC_MODEL')
        }

    def _load_from_claude_settings(self) -> Dict[str, Any]:
        """从Claude Code settings.json读取配置"""
        try:
            settings_path = Path.home() / '.claude' / 'settings.json'
            if settings_path.exists():
                import json
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    env = settings.get('env', {})
                    return {
                        'api_key': env.get('ANTHROPIC_AUTH_TOKEN'),
                        'base_url': env.get('ANTHROPIC_BASE_URL'),
                        'model': env.get('ANTHROPIC_MODEL')
                    }
        except Exception:
            pass
        return {}

    def save_config_template(self):
        """保存配置文件模板到skill_config.yaml"""
        template = {
            'skill': {
                'name': 'industry-research',
                'version': '0.3.0'
            },
            'model': {
                'provider': 'anthropic',
                'model': 'claude-sonnet-5',
                'api_key': 'your-api-key-here',  # 可选：留空则从环境变量读取
                'base_url': 'https://api.anthropic.com',  # 可选：中转站URL
                'max_tokens': 2048,
                'temperature': 0.7
            },
            'paths': {
                'skill_root': '.',
                'output': 'output'
            }
        }

        # 如果配置文件已存在，不覆盖
        if not self.config_file.exists():
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(template, f, allow_unicode=True, default_flow_style=False)
            print(f"✅ 配置文件模板已创建: {self.config_file}")
        else:
            print(f"ℹ️  配置文件已存在: {self.config_file}")


def main():
    """测试模型配置管理器"""
    print("="*60)
    print("测试: 模型配置管理器")
    print("="*60)

    manager = ModelConfigManager()

    # 测试1: 生成配置文件模板
    print("\n[测试1] 生成配置文件模板")
    manager.save_config_template()

    # 测试2: 加载配置（按优先级）
    print("\n[测试2] 加载配置")
    config = manager.load_config()

    print(f"\n加载的配置:")
    print(f"  Provider: {config.provider}")
    print(f"  Model: {config.model}")
    print(f"  API Key: {'已设置' if config.api_key else '未设置'}")
    print(f"  Base URL: {config.base_url if config.base_url else '默认'}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  Temperature: {config.temperature}")

    # 测试3: 代码传入参数（最高优先级）
    print("\n[测试3] 代码传入参数覆盖")
    config2 = manager.load_config(
        provider="openai",
        model="gpt-4",
        api_key="test-key"
    )
    print(f"  Provider: {config2.provider}")
    print(f"  Model: {config2.model}")
    print(f"  API Key: {'已设置' if config2.api_key else '未设置'}")


if __name__ == '__main__':
    main()
