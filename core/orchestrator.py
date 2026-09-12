"""
主控层 - 精简版

职责：
1. 接收用户请求
2. 调用ResearchEngine执行研究
3. 生成报告
4. 返回结果

不再负责：
- 意图解析（→ ResearchEngine）
- 工作流生成（→ ResearchEngine）
- AI分析（→ ResearchEngine）
- 质量检查（→ ResearchEngine）
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class Orchestrator:
    """主控层 - 精简版"""

    def __init__(self, mode='quick'):
        """
        初始化

        Args:
            mode: 'quick' (快速模式) 或 'full' (全量模式)
        """
        self.mode = mode
        self.skill_root = SKILL_ROOT

        print(f"[Orchestrator] 初始化 {mode} 模式...")

        # 初始化核心引擎
        from core.research_engine import ResearchEngine
        self.engine = ResearchEngine()

        # 初始化报告生成器
        from output.professional_report_generator import ProfessionalReportGenerator
        self.report_generator = ProfessionalReportGenerator()

    def run(self, industry: str, user_params: Optional[Dict] = None) -> Dict:
        """
        主入口

        Args:
            industry: 行业名称
            user_params: 用户参数
                - dimensions: List[str] - 指定维度
                - intent: str - 自然语言意图
                - depth: str - 研究深度

        Returns:
            result: {
                'status': 'success'/'error',
                'industry': str,
                'mode': str,
                'path': str,  # 报告路径
                'quality': Dict,
                'analysis_results': List[Dict]
            }
        """
        print(f"\n{'='*60}")
        print(f"开始研究: {industry}")
        print(f"{'='*60}\n")

        try:
            user_params = user_params or {}

            # Step 1: 解析意图（如果提供了自然语言）
            if 'intent' in user_params:
                print("[Step 1] 解析用户意图...")
                parsed = self.engine.parse_intent(user_params['intent'])
                dimensions = parsed['dimensions']
                print(f"   [OK] 识别维度: {', '.join(dimensions)}")
            else:
                dimensions = user_params.get('dimensions', ['政策环境', '市场规模', '商业模式'])
                print(f"[Step 1] 使用指定维度: {', '.join(dimensions)}")

            # Step 2: 生成工作流
            print("\n[Step 2] 生成研究工作流...")
            workflow = self.engine.create_workflow(dimensions)
            total_time = sum(step['time'] for step in workflow)
            print(f"   [OK] 工作流: {len(workflow)}个步骤, 预计 {total_time} 分钟")
            for step in workflow:
                print(f"      - {step['name']} ({step['time']}分钟)")

            # Step 3: 执行分析
            print(f"\n[Step 3] 执行AI分析...")
            results = []
            context = {}  # 累积上下文

            for i, step in enumerate(workflow, 1):
                dim = step['name']
                print(f"   [{i}/{len(workflow)}] 分析 {dim}...", end=' ')

                result = self.engine.analyze(industry, dim, context)
                results.append(result)

                # 更新上下文
                context[dim] = result.get('content', '')

                # 显示质量分数
                score = result.get('quality_score', 0)
                if score >= 0.7:
                    print(f"[OK] (质量: {score:.2f})")
                else:
                    print(f"[WARN] (质量: {score:.2f}, 偏低)")

            # Step 4: 质量检查
            print(f"\n[Step 4] 质量检查...")
            quality_check = self.engine.check_quality(results)
            print(f"   平均质量分: {quality_check['avg_quality']:.2f}")
            if quality_check['passed']:
                print(f"   [OK] 质量检查通过")
            else:
                print(f"   [WARN] 质量问题: {', '.join(quality_check['issues'])}")
                for suggestion in quality_check['suggestions']:
                    print(f"      建议: {suggestion}")

            # Step 5: 生成报告
            print(f"\n[Step 5] 生成专业报告...")
            report_data = {
                'industry': industry,
                'mode': self.mode,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_results': results,
                'quality_check': quality_check
            }

            report_path = self._generate_report(industry, report_data)
            print(f"   [OK] 报告已生成: {report_path}")

            # 返回结果
            print(f"\n{'='*60}")
            print(f"[SUCCESS] 研究完成!")
            print(f"{'='*60}\n")

            return {
                'status': 'success',
                'industry': industry,
                'mode': self.mode,
                'path': report_path,
                'quality': quality_check,
                'analysis_results': results,
                'total_time': total_time
            }

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"[ERROR] 研究失败")
            print(f"{'='*60}")
            print(f"错误: {type(e).__name__}: {str(e)}\n")

            return {
                'status': 'error',
                'industry': industry,
                'error': str(e),
                'error_type': type(e).__name__
            }

    def _generate_report(self, industry: str, data: Dict) -> str:
        """生成HTML报告"""
        output_dir = self.skill_root / 'output'
        output_dir.mkdir(exist_ok=True)

        # 生成报告文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{industry}_研究报告_{timestamp}.html"
        filepath = output_dir / filename

        # 调用报告生成器
        try:
            self.report_generator.generate_report(
                industry=industry,
                research_data=data,
                report_type='html'
            )
            # 假设报告生成器会保存到output目录
            return str(filepath)
        except Exception as e:
            # Fallback: 生成简单报告
            print(f"   ⚠️  专业报告生成失败，使用简单模板")
            return self._generate_simple_report(filepath, industry, data)

    def _generate_simple_report(self, filepath: Path, industry: str, data: Dict) -> str:
        """生成简单HTML报告（Fallback）"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{industry} - 行业研究报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .dimension-title {{
            color: #1e3c72;
            border-left: 4px solid #2a5298;
            padding-left: 15px;
            margin-bottom: 15px;
        }}
        .quality-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        }}
        .quality-good {{
            background: #d4edda;
            color: #155724;
        }}
        .quality-medium {{
            background: #fff3cd;
            color: #856404;
        }}
        .content {{
            color: #333;
            white-space: pre-wrap;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{industry} 行业研究报告</h1>
        <p>生成时间: {data.get('timestamp', '')}</p>
        <p>研究模式: {data.get('mode', '')} | 平均质量分: {data.get('quality', {}).get('avg_quality', 0):.2f}</p>
    </div>
"""

        # 添加分析内容
        for result in data.get('analysis_results', []):
            dimension = result.get('dimension', '未知')
            content = result.get('content', '无内容')
            quality = result.get('quality_score', 0)

            quality_class = 'quality-good' if quality >= 0.7 else 'quality-medium'
            quality_text = f"质量: {quality:.2f}"

            html += f"""
    <div class="section">
        <h2 class="dimension-title">{dimension} <span class="quality-badge {quality_class}">{quality_text}</span></h2>
        <div class="content">{content}</div>
    </div>
"""

        html += """
    <div class="footer">
        <p>本报告由 Industry Research Skill 自动生成</p>
        <p>Powered by Claude AI</p>
    </div>
</body>
</html>
"""

        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(filepath)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='Industry Research Skill')
    parser.add_argument('industry', help='行业名称')
    parser.add_argument('--mode', default='quick', choices=['quick', 'full'], help='研究模式')
    parser.add_argument('--dimensions', help='分析维度（逗号分隔）')
    parser.add_argument('--intent', help='自然语言意图')

    args = parser.parse_args()

    # 构建参数
    user_params = {}
    if args.dimensions:
        user_params['dimensions'] = args.dimensions.split(',')
    if args.intent:
        user_params['intent'] = args.intent

    # 执行研究
    orchestrator = Orchestrator(mode=args.mode)
    result = orchestrator.run(args.industry, user_params)

    # 输出结果
    if result['status'] == 'success':
        print(f"\n✅ 报告已生成: {result['path']}")
    else:
        print(f"\n❌ 研究失败: {result.get('error')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
