"""
测试报告导出器

用途: 验证Word/Markdown导出功能

作者: Claude Opus 5
日期: 2026-09-17
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from output.report_exporter import ReportExporter


def create_test_html():
    """创建测试HTML文件"""
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>医疗陪护行业研究报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #3498db; color: white; }
        .warning { background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <h1>医疗陪护行业研究报告</h1>

    <h2>第一章：行业概述</h2>

    <h3>1.1 市场规模</h3>
    <p>中国医疗陪护市场规模达到<strong>500亿元</strong>，预计未来5年CAGR为<em>25%</em>。</p>

    <ul>
        <li>市场需求持续增长</li>
        <li>老龄化加速</li>
        <li>政策支持力度加大</li>
    </ul>

    <h3>1.2 竞争格局</h3>
    <table>
        <tr>
            <th>公司名称</th>
            <th>市场份额</th>
            <th>核心优势</th>
        </tr>
        <tr>
            <td>陪护管家</td>
            <td>15%</td>
            <td>护理员数量多</td>
        </tr>
        <tr>
            <td>金牌护工</td>
            <td>12%</td>
            <td>服务质量高</td>
        </tr>
        <tr>
            <td>医护到家</td>
            <td>10%</td>
            <td>覆盖城市广</td>
        </tr>
    </table>

    <h2>第二章：关键发现</h2>

    <h3>2.1 核心洞察</h3>
    <ol>
        <li>市场处于快速增长期</li>
        <li>行业集中度较低（CR3=37%）</li>
        <li>服务标准化是痛点</li>
    </ol>

    <h3>2.2 反面证据</h3>
    <div class="warning">
        <strong>⚠️ 反面证据:</strong> 部分报告指出护理员流失率高达40%，服务质量难以保证。
    </div>

    <h2>第三章：投资建议</h2>
    <p>综合评估，建议<strong>谨慎看好</strong>该行业。关注头部企业的标准化能力和护理员留存率。</p>

    <blockquote>
        风险提示：行业监管政策可能趋严，护理员短缺问题短期难以解决。
    </blockquote>
</body>
</html>
    """

    test_file = project_root / "test_report.html"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(html_content.strip())

    return test_file


def main():
    print("=" * 70)
    print("报告导出器测试")
    print("=" * 70)

    # 1. 创建测试HTML
    print("\n[Step 1] 创建测试HTML...")
    test_file = create_test_html()
    print(f"   [OK] 测试文件: {test_file}")

    # 2. 初始化导出器
    print("\n[Step 2] 初始化导出器...")
    exporter = ReportExporter()
    print(f"   [OK] 支持的格式: {exporter.supported_formats}")

    # 3. 测试Word导出
    print("\n[Step 3] 测试Word导出...")
    if 'word' in exporter.supported_formats:
        try:
            word_path = exporter.export_report(str(test_file), 'word')
            print(f"   [OK] Word文件: {word_path}")
        except Exception as e:
            print(f"   [ERROR] Word导出失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   [SKIP] python-docx未安装，跳过Word导出")

    # 4. 测试Markdown导出
    print("\n[Step 4] 测试Markdown导出...")
    if 'markdown' in exporter.supported_formats:
        try:
            md_path = exporter.export_report(str(test_file), 'markdown')
            print(f"   [OK] Markdown文件: {md_path}")

            # 显示Markdown内容（前500字符）
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n   Markdown内容预览:")
                print("   " + "-" * 66)
                for line in content[:600].split('\n'):
                    print(f"   {line}")
                print("   " + "-" * 66)
        except Exception as e:
            print(f"   [ERROR] Markdown导出失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   [SKIP] markdownify未安装，跳过Markdown导出")

    # 5. 总结
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)

    print("\n生成的文件:")
    print(f"  - {test_file}")
    if 'word' in exporter.supported_formats:
        print(f"  - {test_file.with_suffix('.docx')}")
    if 'markdown' in exporter.supported_formats:
        print(f"  - {test_file.with_suffix('.md')}")

    print("\n请手动打开文件验证格式是否正确。")
    print("\n提示: 如需删除测试文件，请运行:")
    print(f"  rm {test_file}")
    print(f"  rm {test_file.with_suffix('.docx')}")
    print(f"  rm {test_file.with_suffix('.md')}")


if __name__ == '__main__':
    main()
