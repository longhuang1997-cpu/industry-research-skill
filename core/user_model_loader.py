"""
用户自定义模型加载器 - Phase 3 任务2

功能:
1. 加载 config/user_models.yaml
2. 验证模型配置
3. 热加载支持（文件变化时自动重新加载）
4. 优雅降级（配置文件不存在或有错误时不阻塞系统）

作者: Claude Opus 5
日期: 2026-09-17
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from core.user_model_validator import UserModelValidator


class UserModelLoader:
    """用户模型加载器"""

    def __init__(self, config_path: str = "config/user_models.yaml"):
        """
        初始化加载器

        Args:
            config_path: 配置文件路径（相对于项目根目录）
        """
        self.config_path = SKILL_ROOT / config_path
        self.validator = UserModelValidator()
        self.models = {}

        # 首次加载
        self.load()

    def load(self) -> Dict:
        """
        加载用户模型

        Returns:
            {model_name: model_config}
        """
        if not self.config_path.exists():
            print(f"[UserModels] ℹ️  未找到 {self.config_path.name}，跳过加载（使用内置模型）")
            return {}

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            if not config:
                print(f"[UserModels] ⚠️  配置文件为空: {self.config_path.name}")
                return {}

            user_models_list = config.get('user_models', [])

            if not user_models_list:
                print(f"[UserModels] ℹ️  配置文件中无自定义模型")
                return {}

            # 验证并加载
            valid_models = {}
            invalid_count = 0

            for model in user_models_list:
                model_name = model.get('name', 'Unknown')

                # 验证
                is_valid, errors = self.validator.validate(model)

                if is_valid:
                    valid_models[model_name] = model
                    print(f"[UserModels] ✅ {model_name}")
                else:
                    invalid_count += 1
                    print(f"[UserModels] ❌ {model_name} - 验证失败")
                    for error in errors:
                        print(f"    • {error}")

            self.models = valid_models

            # 汇总
            total = len(user_models_list)
            valid = len(valid_models)
            print(f"[UserModels] 加载完成: {valid}/{total}个模型有效")

            if invalid_count > 0:
                print(f"[UserModels] ⚠️  跳过{invalid_count}个无效模型，请修复后重新加载")

            return self.models

        except yaml.YAMLError as e:
            print(f"[UserModels] ❌ YAML解析失败: {e}")
            print(f"[UserModels] 请检查配置文件格式: {self.config_path}")
            return {}

        except Exception as e:
            print(f"[UserModels] ❌ 加载失败: {e}")
            return {}

    def reload(self):
        """
        重新加载配置（热加载）

        Returns:
            是否成功重新加载
        """
        print(f"\n[UserModels] 🔄 检测到配置变化，重新加载...")

        old_count = len(self.models)
        new_models = self.load()
        new_count = len(new_models)

        if new_count > old_count:
            print(f"[UserModels] ➕ 新增 {new_count - old_count} 个模型")
        elif new_count < old_count:
            print(f"[UserModels] ➖ 减少 {old_count - new_count} 个模型")
        else:
            print(f"[UserModels] 🔄 模型数量不变（可能是更新）")

        return new_count > 0

    def get_model(self, name: str) -> Optional[Dict]:
        """
        获取指定模型

        Args:
            name: 模型名称

        Returns:
            模型配置字典，不存在则返回None
        """
        return self.models.get(name)

    def get_models_by_type(self, model_type: str) -> List[Dict]:
        """
        获取指定类型的所有模型

        Args:
            model_type: 'core_model', 'thinking_trap', 'strategy_tool'

        Returns:
            模型配置列表
        """
        return [
            model for model in self.models.values()
            if model.get('type') == model_type
        ]

    def get_models_by_category(self, category: str) -> List[Dict]:
        """
        获取指定类别的所有模型

        Args:
            category: 类别名称（如"投资决策"）

        Returns:
            模型配置列表
        """
        return [
            model for model in self.models.values()
            if model.get('category') == category
        ]

    def list_all_models(self) -> List[str]:
        """
        列出所有模型名称

        Returns:
            模型名称列表
        """
        return list(self.models.keys())


# ==================== 热加载支持（可选） ====================

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class UserModelsFileHandler(FileSystemEventHandler):
        """文件变化处理器"""

        def __init__(self, loader: UserModelLoader):
            self.loader = loader

        def on_modified(self, event):
            """文件修改时触发"""
            if event.src_path == str(self.loader.config_path):
                self.loader.reload()

    def start_hot_reload(loader: UserModelLoader):
        """
        启动热加载监听

        Args:
            loader: 用户模型加载器
        """
        if not loader.config_path.exists():
            print("[UserModels] ⚠️  配置文件不存在，跳过热加载启动")
            return

        event_handler = UserModelsFileHandler(loader)
        observer = Observer()
        observer.schedule(
            event_handler,
            str(loader.config_path.parent),
            recursive=False
        )
        observer.start()

        print(f"[UserModels] 🔥 热加载已启动: {loader.config_path.name}")
        print(f"[UserModels] 提示: 修改配置文件后将自动重新加载")

        return observer

except ImportError:
    print("[UserModels] ⚠️  未安装 watchdog，热加载功能不可用")
    print("[UserModels] 安装: pip install watchdog")

    def start_hot_reload(loader: UserModelLoader):
        """热加载不可用时的占位函数"""
        print("[UserModels] ⚠️  热加载功能需要 watchdog 库")
        return None


# ==================== 测试代码 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("用户模型加载器 - 测试")
    print("=" * 60)

    # 测试加载
    loader = UserModelLoader()

    print("\n" + "=" * 60)
    print("加载的模型清单:")
    print("=" * 60)

    if loader.models:
        for i, (name, model) in enumerate(loader.models.items(), 1):
            model_type = model.get('type', 'unknown')
            category = model.get('category', '未分类')
            print(f"{i}. {name}")
            print(f"   类型: {model_type}")
            print(f"   类别: {category}")
            print()
    else:
        print("（无自定义模型）")

    # 测试按类型获取
    print("\n" + "=" * 60)
    print("核心分析模型:")
    print("=" * 60)
    core_models = loader.get_models_by_type('core_model')
    for model in core_models:
        print(f"  - {model['name']}")

    # 测试按类别获取
    print("\n" + "=" * 60)
    print("投资决策类模型:")
    print("=" * 60)
    invest_models = loader.get_models_by_category('投资决策')
    for model in invest_models:
        print(f"  - {model['name']} ({model['type']})")

    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)

    # 热加载测试（如果可用）
    print("\n提示: 修改 config/user_models.yaml 测试热加载...")
    observer = start_hot_reload(loader)

    if observer:
        try:
            import time
            print("按 Ctrl+C 停止监听...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            print("\n[UserModels] 热加载监听已停止")
