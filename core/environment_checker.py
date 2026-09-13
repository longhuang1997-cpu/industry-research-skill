"""
工程问题修复清单 + 预检脚本

问题：
1. API密钥明文存储在skill_config.yaml（安全风险）
2. 输出位置在skill目录，用户找不到
3. 环境依赖没有预检，运行时才报错

解决方案：
- API密钥改为环境变量优先
- 输出改为工作区（用户可见）
- 启动时预检环境
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


class EnvironmentChecker:
    """环境预检 - 启动前检查所有依赖"""

    def __init__(self):
        self.issues = []
        self.warnings = []

    def check_all(self) -> Dict:
        """
        执行完整环境检查

        Returns:
            {
                'passed': True/False,
                'issues': [...],  # 阻断性问题
                'warnings': [...], # 警告
                'can_run': True/False
            }
        """
        # 1. Python版本检查
        self._check_python_version()

        # 2. 依赖包检查
        self._check_dependencies()

        # 3. API配置检查
        self._check_api_config()

        # 4. 文件权限检查
        self._check_file_permissions()

        # 5. 输出目录检查
        self._check_output_directory()

        can_run = len(self.issues) == 0

        return {
            'passed': can_run,
            'issues': self.issues,
            'warnings': self.warnings,
            'can_run': can_run
        }

    def _check_python_version(self):
        """Python版本检查"""
        version = sys.version_info
        if version < (3, 8):
            self.issues.append(
                f"❌ Python版本过低: {version.major}.{version.minor}，需要3.8+"
            )
        elif version < (3, 10):
            self.warnings.append(
                f"⚠️ Python版本: {version.major}.{version.minor}，建议升级到3.10+"
            )

    def _check_dependencies(self):
        """依赖包检查"""
        required_packages = {
            'anthropic': '必需（API调用）',
            'pyyaml': '必需（配置文件）',
        }

        for package, purpose in required_packages.items():
            try:
                __import__(package)
            except ImportError:
                self.issues.append(
                    f"❌ 缺少依赖包: {package} - {purpose}\n"
                    f"   安装: pip install {package}"
                )

    def _check_api_config(self):
        """API配置检查（安全优先）"""
        # 检查环境变量
        api_key_env = os.getenv('ANTHROPIC_API_KEY')

        # 检查配置文件（不推荐）
        config_file = Path(__file__).parent.parent / 'skill_config.yaml'
        api_key_in_config = self._check_config_file_for_key(config_file)

        if not api_key_env and not api_key_in_config:
            self.issues.append(
                "❌ API密钥未配置\n"
                "   推荐方式: export ANTHROPIC_API_KEY='your-key'\n"
                "   备选方式: 在skill_config.yaml中配置（不安全）"
            )

        if api_key_in_config:
            self.warnings.append(
                "⚠️ 安全警告: API密钥存储在skill_config.yaml（明文）\n"
                "   建议改为环境变量: export ANTHROPIC_API_KEY='your-key'\n"
                "   然后删除配置文件中的api_key字段"
            )

    def _check_config_file_for_key(self, config_file: Path) -> bool:
        """检查配置文件是否有API密钥"""
        if not config_file.exists():
            return False

        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                api_key = config.get('model', {}).get('api_key', '')
                return bool(api_key and api_key.strip())
        except Exception:
            return False

    def _check_file_permissions(self):
        """文件权限检查"""
        skill_root = Path(__file__).parent.parent

        # 检查是否可写
        test_file = skill_root / '.permission_test'
        try:
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            self.issues.append(
                f"❌ 技能目录不可写: {skill_root}\n"
                f"   错误: {str(e)}"
            )

    def _check_output_directory(self):
        """输出目录检查"""
        # 获取用户工作区（而非技能目录）
        workspace = self._get_workspace()

        if not workspace:
            self.warnings.append(
                "⚠️ 无法确定工作区位置，将使用当前目录作为输出路径"
            )
            return

        # 检查输出目录是否可创建
        output_dir = workspace / 'industry_research_output'
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.issues.append(
                f"❌ 无法创建输出目录: {output_dir}\n"
                f"   错误: {str(e)}"
            )

    def _get_workspace(self) -> Optional[Path]:
        """获取用户工作区（而非技能目录）"""
        # 方式1: 从环境变量读取（Claude Code会设置）
        workspace_env = os.getenv('CLAUDE_WORKSPACE_DIR')
        if workspace_env:
            return Path(workspace_env)

        # 方式2: 当前工作目录
        cwd = Path.cwd()
        skill_root = Path(__file__).parent.parent

        # 如果cwd不是技能目录，那就是工作区
        if cwd != skill_root and not str(cwd).startswith(str(skill_root)):
            return cwd

        # 方式3: 回退到用户主目录
        return Path.home()


class SecureConfigManager:
    """安全的配置管理（环境变量优先）"""

    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        获取API密钥（优先级: 环境变量 > 配置文件）

        Returns:
            API密钥，如果都没有则返回None
        """
        # 优先从环境变量读取
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key

        # 回退到配置文件（但会打印警告）
        config_file = Path(__file__).parent.parent / 'skill_config.yaml'
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    api_key = config.get('model', {}).get('api_key', '')
                    if api_key:
                        print("⚠️ 警告: API密钥从配置文件读取（不安全）")
                        print("   建议改为环境变量: export ANTHROPIC_API_KEY='your-key'")
                        return api_key
            except Exception as e:
                print(f"❌ 读取配置文件失败: {e}")

        return None

    @staticmethod
    def get_output_directory() -> Path:
        """
        获取输出目录（工作区，而非技能目录）

        Returns:
            输出目录路径
        """
        # 获取工作区
        workspace_env = os.getenv('CLAUDE_WORKSPACE_DIR')
        if workspace_env:
            workspace = Path(workspace_env)
        else:
            workspace = Path.cwd()

        # 创建输出目录
        output_dir = workspace / 'industry_research_output'
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir


def precheck_and_run():
    """启动前预检 + 报告"""
    print("=" * 60)
    print("Industry Research Skill - 环境预检")
    print("=" * 60)

    checker = EnvironmentChecker()
    result = checker.check_all()

    # 打印检查结果
    if result['issues']:
        print("\n❌ 发现阻断性问题:")
        for issue in result['issues']:
            print(f"\n{issue}")

    if result['warnings']:
        print("\n⚠️ 警告:")
        for warning in result['warnings']:
            print(f"\n{warning}")

    if result['can_run']:
        print("\n✅ 环境检查通过，可以运行")
        print(f"   API密钥: {'已配置' if SecureConfigManager.get_api_key() else '未配置'}")
        print(f"   输出目录: {SecureConfigManager.get_output_directory()}")
        return True
    else:
        print("\n❌ 环境检查失败，无法运行")
        print("   请先解决上述问题")
        return False


if __name__ == "__main__":
    # 测试预检
    success = precheck_and_run()
    sys.exit(0 if success else 1)
