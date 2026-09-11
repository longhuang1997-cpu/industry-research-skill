"""
YAML加载工具模块

提供YAML配置文件加载功能
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Union


class YAMLLoader:
    """
    YAML加载器
    """

    @staticmethod
    def load(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        加载YAML文件

        Args:
            file_path: YAML文件路径

        Returns:
            data: 解析后的数据
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def save(data: Dict[str, Any],
             file_path: Union[str, Path],
             create_dirs: bool = True) -> Path:
        """
        保存数据为YAML文件

        Args:
            data: 要保存的数据
            file_path: 目标文件路径
            create_dirs: 是否自动创建目录

        Returns:
            path: 文件路径
        """
        path = Path(file_path)

        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)

        return path
