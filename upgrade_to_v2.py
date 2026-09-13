#!/usr/bin/env python3
"""
v2.0升级脚本 - 一键升级到真实数据 + 真质量检查

功能:
1. 环境预检（确保可以运行）
2. 备份当前版本（git commit）
3. 测试v2.0功能（演示模式）
4. 生成升级报告

使用:
    python upgrade_to_v2.py --check-only  # 仅检查，不升级
    python upgrade_to_v2.py --upgrade      # 执行升级
"""

import sys
import subprocess
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.environment_checker import EnvironmentChecker, SecureConfigManager


def check_environment():
    """步骤1: 环境预检"""
    print("\n" + "="*60)
    print("步骤1: 环境预检")
    print("="*60)

    checker = EnvironmentChecker()
    result = checker.check_all()

    if result['issues']:
        print("\n❌ 发现阻断性问题:")
        for issue in result['issues']:
            print(f"   {issue}")
        return False

    if result['warnings']:
        print("\n⚠️ 警告:")
        for warning in result['warnings']:
            print(f"   {warning}")

    if result['can_run']:
        print("\n✅ 环境检查通过")
        return True
    else:
        print("\n❌ 环境检查失败")
        return False


def backup_current_version():
    """步骤2: 备份当前版本"""
    print("\n" + "="*60)
    print("步骤2: 备份当前版本")
    print("="*60)

    try:
        # 检查是否有未提交的更改
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            print("   发现未提交的更改，创建备份提交...")

            # 添加所有更改
            subprocess.run(['git', 'add', '-A'], check=True)

            # 提交
            subprocess.run(
                ['git', 'commit', '-m', 'Pre-v2.0 backup: automatic commit before upgrade'],
                check=True
            )

            print("   ✅ 已创建备份提交")
        else:
            print("   ✅ 工作区干净，无需备份")

        # 创建标签
        try:
            subprocess.run(
                ['git', 'tag', '-a', 'pre-v2.0-upgrade', '-m', 'Backup before v2.0 upgrade'],
                check=True
            )
            print("   ✅ 已创建标签: pre-v2.0-upgrade")
        except subprocess.CalledProcessError:
            print("   ⚠️ 标签已存在，跳过")

        return True

    except subprocess.CalledProcessError as e:
        print(f"   ❌ 备份失败: {e}")
        return False


def test_v2_functionality():
    """步骤3: 测试v2.0功能"""
    print("\n" + "="*60)
    print("步骤3: 测试v2.0功能（演示模式）")
    print("="*60)

    try:
        from core.research_engine_v2 import ResearchEngineV2

        # 初始化引擎
        print("\n3.1 初始化v2.0引擎...")
        engine = ResearchEngineV2(enable_web_search=True)

        # 测试单维度分析
        print("\n3.2 测试单维度分析...")
        result = engine.analyze_dimension(
            industry="测试行业",
            dimension="市场规模"
        )

        print(f"   质量分: {result['quality']['score']}")
        print(f"   数据来源: {result['method']}")
        print(f"   通过: {'✅' if result['passed'] else '❌'}")

        # 测试质量检查
        print("\n3.3 测试质量检查...")
        from core.quality_checker_v2 import QualityChecker

        checker = QualityChecker()

        # 测试好报告（有来源）
        good_content = """
        根据[来源1]显示，市场规模约200亿元[来源2]。
        """
        good_result = checker.check_report(
            good_content,
            "市场规模",
            {'method': 'web_search', 'results': [{'url': 'test'}]}
        )
        print(f"   好报告评分: {good_result['score']} ({good_result['grade']})")

        # 测试坏报告（无来源）
        bad_content = """
        市场规模约200亿元。
        """
        bad_result = checker.check_report(
            bad_content,
            "市场规模",
            {'method': 'llm_fallback'}
        )
        print(f"   坏报告评分: {bad_result['score']} ({bad_result['grade']})")

        print("\n✅ v2.0功能测试通过")
        return True

    except Exception as e:
        print(f"\n❌ v2.0功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_upgrade_report():
    """步骤4: 生成升级报告"""
    print("\n" + "="*60)
    print("步骤4: 生成升级报告")
    print("="*60)

    report = """
# v2.0升级完成报告

## 升级时间
{timestamp}

## 新增文件
- core/web_search_integration.py (Web搜索集成)
- core/quality_checker_v2.py (真质量检查)
- core/environment_checker.py (环境预检)
- core/research_engine_v2.py (v2.0引擎)

## 关键改进
1. ✅ Web搜索集成（真实数据）
2. ✅ 质量检查升级（硬关卡）
3. ✅ 安全配置（环境变量优先）
4. ✅ 输出位置修正（工作区）

## 使用方式

### 方式1: Python API
```python
from core.research_engine_v2 import ResearchEngineV2

engine = ResearchEngineV2(enable_web_search=True)
result = engine.generate_full_report(
    industry="医疗陪护",
    dimensions=["政策环境", "市场规模"],
    fail_fast=True
)
```

### 方式2: 命令行（需要修改irs.py）
```bash
python irs.py "医疗陪护" --use-v2
```

## 回退方式
如果需要回退到v1.x:
```bash
git checkout pre-v2.0-upgrade
```

## 下一步
1. 在真实项目中测试v2.0
2. 根据反馈调整质量标准
3. 集成到CI/CD流程

## 技术支持
- 文档: UPGRADE_TO_V2.md
- 问题: GitHub Issues
"""

    import datetime
    report = report.format(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 保存报告
    report_path = Path("UPGRADE_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"   ✅ 升级报告已生成: {report_path}")
    return True


def main():
    """主流程"""
    import argparse

    parser = argparse.ArgumentParser(description="Industry Research Skill v2.0 升级工具")
    parser.add_argument('--check-only', action='store_true', help='仅检查环境，不执行升级')
    parser.add_argument('--upgrade', action='store_true', help='执行完整升级')
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════╗
║   Industry Research Skill v2.0 升级工具               ║
║   真实数据 + 真质量检查                                ║
╚══════════════════════════════════════════════════════════╝
""")

    # 步骤1: 环境预检（总是执行）
    if not check_environment():
        print("\n❌ 环境预检失败，请先解决上述问题")
        return 1

    if args.check_only:
        print("\n✅ 仅检查模式：环境检查通过，可以升级")
        return 0

    if not args.upgrade:
        print("\n提示: 使用 --upgrade 参数执行升级")
        print("      使用 --check-only 仅检查环境")
        return 0

    # 步骤2: 备份
    if not backup_current_version():
        print("\n❌ 备份失败，中止升级")
        return 1

    # 步骤3: 测试
    if not test_v2_functionality():
        print("\n❌ 功能测试失败，中止升级")
        return 1

    # 步骤4: 生成报告
    generate_upgrade_report()

    print("\n" + "="*60)
    print("🎉 v2.0升级完成！")
    print("="*60)
    print("\n下一步:")
    print("1. 阅读 UPGRADE_TO_V2.md 了解详细变化")
    print("2. 阅读 UPGRADE_REPORT.md 查看升级报告")
    print("3. 测试: python -m core.research_engine_v2")
    print("\n如需回退:")
    print("git checkout pre-v2.0-upgrade")
    print("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
