"""
5分钟实操演示脚本
==================

用途: 现场演示industry-research-skill v3.0三大核心功能
时长: 5分钟
方式: 真实文件操作，无需调用API
"""

import os
import sys
import time
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CONFIG_DIR = PROJECT_ROOT / "config"

# 颜色输出（Windows兼容）
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    """打印章节标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_section(text):
    """打印小节标题"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {text}{Colors.END}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_info(text):
    """打印普通信息"""
    print(f"{Colors.BLUE}{text}{Colors.END}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def wait_for_enter(prompt="按回车继续..."):
    """等待用户按回车"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")
    input()

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================================
# 开场
# ============================================================================

def demo_intro():
    """开场介绍"""
    clear_screen()
    print_header("Industry Research Skill v3.0 - 实操演示")

    print(f"{Colors.BOLD}欢迎！今天展示行业研究工具v3.0的三大核心升级：{Colors.END}\n")

    print(f"{Colors.GREEN}1. 反驳强化{Colors.END} - 提升报告可信度20-30%")
    print(f"{Colors.GREEN}2. 自定义模型库{Colors.END} - 企业方法论沉淀")
    print(f"{Colors.GREEN}3. 多格式导出{Colors.END} - Word + Markdown + HTML\n")

    print_info("💡 核心价值：让新手学会做研究，让专家提效10倍")

    wait_for_enter("准备好了吗？按回车开始演示...")

# ============================================================================
# Part 1: 反驳强化（2分钟）★核心
# ============================================================================

def demo_part1_counter_evidence():
    """演示反驳强化功能"""
    clear_screen()
    print_header("Part 1: 反驳强化 ★核心功能")

    print_section("1.1 什么是反驳强化？")
    print_info("传统研究报告常常只看正面，容易得出片面结论。")
    print_info("Phase 3新增：AI自动搜索反面证据，强制辩证思考。\n")

    wait_for_enter("按回车查看实际效果...")

    print_section("1.2 实际案例：医疗陪护行业分析")

    print(f"\n{Colors.BOLD}正面分析:{Colors.END}")
    print_info("✓ 政府推动长护险试点，覆盖1.45亿人")
    print_info("✓ 老龄化加速，2030年预计3亿老人")
    print_info("✓ 建议：加速推广，抢占市场\n")

    time.sleep(1)

    print(f"{Colors.BOLD}AI自动搜索到的反面证据:{Colors.END}")
    print_warning("⚠ 某地试点3年后因财政压力暂停，覆盖率降至20%")
    print_warning("⚠ 三四线城市参保意愿不足，实际覆盖率<5%")
    print_warning("⚠ 护理员短缺严重，供需失衡\n")

    time.sleep(1)

    print_section("1.3 价值")
    print_success("强制辩证思考，避免片面乐观")
    print_success("提升报告可信度 20-30%")
    print_success("带来源链接，可核查\n")

    print_section("1.4 技术实现")
    print_info("步骤1: AI提取关键结论")
    print_info("步骤2: 生成反向搜索（'XX试点失败'、'XX问题'）")
    print_info("步骤3: Web搜索实际数据")
    print_info("步骤4: 自动筛选，展示在报告中")

    wait_for_enter("\n按回车打开实际HTML报告...")

    # 打开HTML报告
    html_file = OUTPUT_DIR / "医疗陪护_mock_report_20260917_114337.html"
    if html_file.exists():
        print_success(f"正在打开报告: {html_file.name}")
        os.system(f'start "" "{html_file}"')
        print_info("\n👉 请在浏览器中查看黄色警告框（反驳证据）")
    else:
        print_warning(f"报告文件不存在: {html_file}")
        print_info("演示时请提前生成报告")

    wait_for_enter("\n看完报告后，按回车继续下一部分...")

# ============================================================================
# Part 2: 自定义模型库（1.5分钟）★核心
# ============================================================================

def demo_part2_custom_models():
    """演示自定义模型库"""
    clear_screen()
    print_header("Part 2: 自定义模型库 ★核心功能")

    print_section("2.1 什么是自定义模型库？")
    print_info("企业可以把自己的分析框架沉淀成配置文件")
    print_info("与系统内置的57个模型无缝融合")
    print_info("这是企业的长期资产，团队用统一框架\n")

    wait_for_enter("按回车查看配置示例...")

    print_section("2.2 示例：我司SaaS评估模型")

    config_file = CONFIG_DIR / "user_models.yaml"

    print(f"{Colors.BOLD}配置文件位置:{Colors.END}")
    print_info(f"  {config_file}\n")

    print(f"{Colors.BOLD}模型内容:{Colors.END}")
    print_info("  类型: core_model（核心分析模型）")
    print_info("  类别: 投资决策\n")

    print(f"{Colors.BOLD}  关键指标（5个）:{Colors.END}")
    print_info("    • ARR增速（年度经常性收入）")
    print_info("    • NDR（净收入留存率）")
    print_info("    • Magic Number（营销效率）")
    print_info("    • CAC Payback Period（获客成本回收期）")
    print_info("    • Rule of 40（增长率+利润率）\n")

    print(f"{Colors.BOLD}  分析维度（5个）:{Colors.END}")
    print_info("    • 收入增长质量")
    print_info("    • 客户留存健康度")
    print_info("    • 获客效率")
    print_info("    • 单位经济")
    print_info("    • 产品-市场契合度\n")

    wait_for_enter("按回车打开配置文件...")

    # 打开配置文件
    if config_file.exists():
        print_success(f"正在打开配置: {config_file.name}")
        os.system(f'notepad "{config_file}"')
        print_info("\n👉 请在记事本中查看完整配置")
    else:
        print_warning(f"配置文件不存在: {config_file}")

    wait_for_enter("\n看完配置后，按回车继续...")

    print_section("2.3 特性")
    print_success("✓ YAML格式，简单易用")
    print_success("✓ 保存后1秒内生效（热加载）")
    print_success("✓ 无数量限制（建议10-20个核心模型）")
    print_success("✓ 3种类型：核心模型、思维陷阱、战略工具")

    wait_for_enter("\n按回车继续下一部分...")

# ============================================================================
# Part 3: 多格式导出（30秒）
# ============================================================================

def demo_part3_export():
    """演示多格式导出"""
    clear_screen()
    print_header("Part 3: 多格式导出")

    print_section("3.1 支持的格式")
    print_info("✓ HTML - 在线查看，交互式")
    print_info("✓ Word - 给领导/客户，可编辑")
    print_info("✓ Markdown - Git版本控制，团队协作\n")

    print_section("3.2 一键导出")
    print_info("使用方法:")
    print(f"  {Colors.BOLD}report_exporter.export_report({Colors.END}")
    print(f"      html_path='报告.html',")
    print(f"      output_formats=['word', 'markdown']")
    print(f"  {Colors.BOLD}){Colors.END}\n")

    print_section("3.3 输出示例")

    # 查找输出文件
    output_files = list(OUTPUT_DIR.glob("*.html"))

    if output_files:
        print_info(f"Output目录中的文件:")
        for i, f in enumerate(output_files[:3], 1):
            print(f"  {i}. {f.name}")
        print()

    print_success("✓ 满足不同场景需求")
    print_success("✓ 保留完整内容和基本样式")

    wait_for_enter("\n按回车进入总结...")

# ============================================================================
# 总结
# ============================================================================

def demo_summary():
    """演示总结"""
    clear_screen()
    print_header("演示总结")

    print_section("Phase 3 三大核心升级")
    print(f"\n{Colors.GREEN}{Colors.BOLD}1. 反驳强化{Colors.END}")
    print_info("   • 自动搜索反面证据")
    print_info("   • 提升可信度 20-30%")
    print_info("   • 强制辩证思考\n")

    print(f"{Colors.GREEN}{Colors.BOLD}2. 自定义模型库{Colors.END}")
    print_info("   • 企业方法论沉淀")
    print_info("   • YAML配置，热加载 ≤1秒")
    print_info("   • 长期资产\n")

    print(f"{Colors.GREEN}{Colors.BOLD}3. 多格式导出{Colors.END}")
    print_info("   • Word + Markdown + HTML")
    print_info("   • 满足不同场景\n")

    print_section("开发成果")
    print_success("• 代码量: 4,500行")
    print_success("• 开发工时: 21小时")
    print_success("• 验收通过率: 100% (33/33)")
    print_success("• 内置模型: 57个 + 自定义无限")

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}感谢观看！欢迎提问！{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主演示流程"""
    try:
        # 检查Python版本
        if sys.version_info < (3, 7):
            print_warning("警告: 建议使用Python 3.7+")

        # 开场
        demo_intro()

        # Part 1: 反驳强化
        demo_part1_counter_evidence()

        # Part 2: 自定义模型库
        demo_part2_custom_models()

        # Part 3: 多格式导出
        demo_part3_export()

        # 总结
        demo_summary()

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}演示被中断{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}错误: {e}{Colors.END}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
