"""
文件操作工具模块

提供统一的文件读写接口
"""

from pathlib import Path
from typing import Optional, Union


class FileUtils:
    """
    文件操作工具类
    """

    @staticmethod
    def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        读取文件内容

        Args:
            file_path: 文件路径
            encoding: 文件编码

        Returns:
            content: 文件内容
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write_file(file_path: Union[str, Path],
                   content: str,
                   encoding: str = 'utf-8',
                   create_dirs: bool = True) -> Path:
        """
        写入文件

        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码
            create_dirs: 是否自动创建目录

        Returns:
            path: 文件路径
        """
        path = Path(file_path)

        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding=encoding) as f:
            f.write(content)

        return path

    @staticmethod
    def ensure_dir(dir_path: Union[str, Path]) -> Path:
        """
        确保目录存在

        Args:
            dir_path: 目录路径

        Returns:
            path: 目录路径
        """
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
