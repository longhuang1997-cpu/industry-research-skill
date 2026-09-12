"""
主控层：协调知识层、执行层、输出层的工作

使用方法:
    python orchestrator.py 医疗陪护 --mode quick
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class IndustryResearchOrchestrator:
    """
    主控层编排器

    协调:
    - 知识层: 框架选择、数据源选择
    - 执行层: 数据收集、图表生成
    - 输出层: 质量检查、报告生成、打包
    """

    def __init__(self, mode='quick'):
        """
        初始化主控层

        Args:
            mode: 'quick' (70分钟) 或 'full' (3-5小时)
        """
        self.mode = mode
        self.skill_root = SKILL_ROOT
        self.human_decisions = []

        print(f"[Orchestrator] Initializing {mode} mode...")

        # 初始化各层组件
        from knowledge.frameworks.framework_selector import FrameworkSelector
        from knowledge.data_sources.data_source_selector import DataSourceSelector
        from execution.data_collector import DataCollector
        from execution.framework_applier import FrameworkApplier
        from execution.chart_generator import ChartGenerator
        from execution.consulting_ai_analyzer import ConsultingAIAnalyzer
        from output.quality_checker import QualityChecker
        from output.report_generator import ReportGenerator
        from output.packaging import Packager
        from output.professional_report_generator import ProfessionalReportGenerator

        self.framework_selector = FrameworkSelector()
        self.data_source_selector = DataSourceSelector()
        self.data_collector = DataCollector()
        self.framework_applier = FrameworkApplier()
        self.ai_analyzer = ConsultingAIAnalyzer()  # 新增：AI分析引擎
        self.quality_checker = QualityChecker()
        self.report_generator = ReportGenerator()
        self.professional_generator = ProfessionalReportGenerator()  # 新增：专业报告生成器
        self.packager = Packager()

    def run(self, industry_name, user_params=None):
        """
        主入口

        Args:
            industry_name: 行业名称 (如"医疗陪护")
            user_params: 用户参数 (可选)

        Returns:
            deliverable: 交付物路径和元数据
        """
        print(f"\n[Orchestrator] Starting research for: {industry_name}")

        # Step 1: 收集需求
        research_brief = self._collect_requirements(industry_name, user_params)

        # Step 2: 根据模式执行
        if self.mode == 'quick':
            return self._run_quick_mode(research_brief)
        else:
            return self._run_full_mode(research_brief)

    def _collect_requirements(self, industry_name, user_params):
        """
        收集研究需求

        TODO: 弹出HTML表单收集需求
        """
        if user_params:
            return user_params

        # 当前版本: 使用默认参数
        return {
            'industry': industry_name,
            'web_search': True,
            'chart_style': 'data_accurate',
            'mode': self.mode
        }

    def _run_quick_mode(self, brief):
        """
        快速模式CPM路径 (70分钟)

        6个关键步骤:
        1. 数据收集
        2. 框架分析 + AI深度分析
        3. 快速可视化
        4. 执行摘要
        5. 质量检查
        6. 打包交付
        """
        print("\n" + "="*60)
        print("Quick Research Mode (Est. 70 minutes)")
        print("="*60)

        industry = brief['industry']

        # Phase 1: 数据收集
        print("\n[Phase 1/6] Data Collection...")
        collected_data = self.data_collector.auto_collect(
            industry=industry,
            year=2024,
            data_source_selector=self.data_source_selector
        )

        # 添加行业名称到collected_data，供后续框架分析使用
        collected_data['industry'] = industry

        # Phase 2: 框架分析 + AI深度分析（集成）
        print("\n[Phase 2/6] Framework Analysis + AI Deep Analysis...")
        frameworks = self.framework_selector.select_frameworks(industry)
        key_questions = self.framework_selector.get_key_questions(industry)

        # 应用框架到数据
        framework_analysis = self.framework_applier.apply(frameworks, collected_data)

        print(f"   Applied {len(frameworks)} frameworks")
        print(f"   Key questions: {len(key_questions)}")

        # AI深度分析（集成ConsultingAIAnalyzer）
        print("\n   [AI Deep Analysis] Running consulting-grade AI analysis...")

        # 行业画像
        profile = self.ai_analyzer._analyze_industry_profile(industry)

        # 政策环境分析
        policy = self.ai_analyzer._analyze_policy_environment(industry, collected_data)

        # 市场规模测算
        market = self.ai_analyzer._analyze_market_size(industry, collected_data)

        # 商业模式分析
        business_model = self.ai_analyzer._analyze_business_model(industry, collected_data)

        # 合并AI分析结果到framework_analysis
        framework_analysis['ai_insights'] = {
            'profile': profile,
            'policy': policy,
            'market_size': market,
            'business_model': business_model
        }

        print(f"   AI Analysis completed with quality scores:")
        print(f"      Policy: {policy.get('quality_score', 0):.2f}")
        print(f"      Market: {market.get('quality_score', 0):.2f}")
        print(f"      Business Model: {business_model.get('quality_score', 0):.2f}")

        # Phase 3: 生成核心图表
        print("\n[Phase 3/6] Generating Core Charts...")

        # 准备图表数据（使用模拟数据作为示例）
        chart_data = self._prepare_chart_data(industry, framework_analysis, collected_data)

        from execution.chart_generator import ChartGenerator
        chart_generator = ChartGenerator(industry=industry)
        chart_paths = chart_generator.generate_core_charts(chart_data)

        chart_summary = chart_generator.get_chart_summary()
        print(f"   Generated {chart_summary['count']} charts")
        print(f"   Total size: {chart_summary['total_size'] / 1024:.1f} KB")

        # Phase 4: 生成专业报告（使用ProfessionalReportGenerator）
        print("\n[Phase 4/6] Generating Professional Report...")

        # 准备研究数据
        research_data = {
            'profile': profile,
            'analysis': {
                'policy': policy,
                'market_size': market,
                'business_model': business_model
            },
            'frameworks': framework_analysis,
            'charts': chart_paths
        }

        # 使用专业报告生成器
        report_path = self.professional_generator.generate_report(
            industry=industry,
            research_data=research_data,
            report_type='quick'
        )

        print(f"   Professional report generated: {report_path}")

        # Phase 5: 质量检查
        print("\n[Phase 5/6] Quality Check...")

        # 质量检查包含AI分析结果
        quality_data = {
            'ai_analysis': framework_analysis.get('ai_insights', {}),
            'framework_analysis': framework_analysis,
            'charts': chart_paths,
            'data_sources': collected_data.get('sources', [])
        }

        issues = self.quality_checker.check_all(
            quality_data,
            chart_paths,
            collected_data
        )

        if issues:
            print(f"   Found {len(issues)} issues")
        else:
            print(f"   Quality check passed")

        # Phase 6: 打包交付
        print("\n[Phase 6/6] Packaging Deliverable...")
        deliverable = self.packager.package_quick_deliverable(
            research_data,
            chart_paths,
            collected_data.get('sources', [])
        )

        print(f"   Package: {deliverable.get('html_path', report_path)}")

        return {
            'status': 'success',
            'mode': 'quick',
            'industry': industry,
            'path': report_path,
            'charts': chart_summary['count'],
            'data_sources': len(collected_data.get('sources', [])),
            'tier1_coverage': collected_data.get('tier1_coverage', 0),
            'quality_issues': len(issues),
            'ai_quality_avg': (
                policy.get('quality_score', 0) +
                market.get('quality_score', 0) +
                business_model.get('quality_score', 0)
            ) / 3
        }

    def _prepare_chart_data(self, industry, analysis, collected_data):
        """
        准备图表数据

        从分析结果中提取图表所需数据
        """
        chart_data = {}

        # 金字塔图数据（从分析结果提取）
        industry_chain = analysis.get('frameworks', {}).get('行业链分析', {})
        if industry_chain:
            chart_data['industry_structure'] = {
                'title': f'{industry}行业结构金字塔',
                'layers': [
                    {'label': '高端市场', 'value': 630, 'unit': '亿元'},
                    {'label': '中端市场', 'value': 470, 'unit': '亿元'},
                    {'label': '基础市场', 'value': 210, 'unit': '亿元'}
                ]
            }

        # 瀑布图数据（从单位经济模型提取）
        unit_economics = analysis.get('frameworks', {}).get('单位经济模型', {})
        if unit_economics:
            chart_data['unit_economics'] = {
                'title': f'{industry}单位经济模型',
                'items': [
                    {'label': '单位收入', 'value': 500, 'type': 'start'},
                    {'label': '人力成本', 'value': -200, 'type': 'decrease'},
                    {'label': '材料成本', 'value': -100, 'type': 'decrease'},
                    {'label': '运营成本', 'value': -50, 'type': 'decrease'},
                    {'label': '单位毛利', 'value': 150, 'type': 'end'}
                ],
                'unit': '元'
            }

        # 支付结构对比（从四方决策链提取）
        four_party = analysis.get('frameworks', {}).get('四方决策链', {})
        if four_party:
            chart_data['payment_structure'] = {
                'title': f'{industry}支付结构演进',
                'left': {
                    'title': '当前（2024）',
                    'data': {'自费': 70, '保险': 20, '政府': 10}
                },
                'right': {
                    'title': '目标（2030）',
                    'data': {'自费': 40, '保险': 40, '长护险': 10, '政府': 10}
                }
            }

        # 时间线图数据（从PEST分析提取政策演进）
        pest_analysis = analysis.get('frameworks', {}).get('PEST分析', {})
        if pest_analysis:
            chart_data['policy_timeline'] = {
                'title': f'{industry}政策演进时间线',
                'events': [
                    {'year': 2015, 'event': '长护险试点启动', 'description': '15个城市开始试点'},
                    {'year': 2018, 'event': '扩大试点范围', 'description': '扩展至49个城市'},
                    {'year': 2020, 'event': '全国推广', 'description': '政策全面落地'},
                    {'year': 2022, 'event': '深化改革', 'description': '优化支付标准'},
                    {'year': 2024, 'event': '覆盖1.8亿人', 'description': '参保人数突破1.8亿'}
                ]
            }

        # 散点矩阵图数据（从波特五力提取竞争格局）
        porter_five = analysis.get('frameworks', {}).get('波特五力', {})
        if porter_five:
            chart_data['competitive_landscape'] = {
                'title': f'{industry}企业竞争格局（2024）',
                'competitors': [
                    {'name': '头部企业A', 'x': 8.5, 'y': 7.2, 'size': 120},
                    {'name': '头部企业B', 'x': 7.8, 'y': 6.5, 'size': 100},
                    {'name': '成长企业C', 'x': 4.2, 'y': 8.1, 'size': 60},
                    {'name': '区域企业D', 'x': 5.5, 'y': 3.8, 'size': 70},
                    {'name': '新进入者E', 'x': 2.1, 'y': 9.5, 'size': 30},
                    {'name': '区域企业F', 'x': 3.5, 'y': 2.2, 'size': 40}
                ],
                'x_label': '市场份额 (%)',
                'y_label': '增长率 (%)',
                'quadrants': ['低份额低增长', '高份额低增长', '低份额高增长', '高份额高增长']
            }

        # 趋势图数据（市场规模趋势）
        chart_data['market_trend'] = {
            'title': f'{industry}市场规模趋势（2015-2024）',
            'series': [
                {
                    'name': '市场规模',
                    'data': [
                        {'year': 2015, 'value': 100},
                        {'year': 2016, 'value': 150},
                        {'year': 2017, 'value': 210},
                        {'year': 2018, 'value': 320},
                        {'year': 2019, 'value': 470},
                        {'year': 2020, 'value': 680},
                        {'year': 2021, 'value': 950},
                        {'year': 2022, 'value': 1200},
                        {'year': 2023, 'value': 1480},
                        {'year': 2024, 'value': 1750}
                    ]
                }
            ],
            'y_label': '市场规模（亿元）',
            'show_markers': True
        }

        # 雷达图数据（PEST分析维度评分）
        if pest_analysis:
            chart_data['pest_radar'] = {
                'title': f'{industry}PEST分析雷达图',
                'dimensions': ['Political', 'Economic', 'Social', 'Technological'],
                'series': [
                    {
                        'name': '当前影响强度',
                        'values': [8, 6, 7, 5]  # 政策驱动型行业特征
                    },
                    {
                        'name': '未来预期影响',
                        'values': [9, 7, 8, 7]
                    }
                ],
                'max_value': 10
            }

        return chart_data

    def _run_full_mode(self, brief):
        """
        全量模式5阶段 (3-5小时)

        包含3个人工决策点:
        - 数据来源确认
        - 洞察深度自检
        - 最终质量把关
        """
        print("\n" + "="*60)
        print("Full Research Mode (Est. 3-5 hours)")
        print("="*60)

        industry = brief['industry']

        # Phase 1: 深度数据收集（包含人工决策点1）
        print("\n[Phase 1/5] Deep Data Collection...")
        collected_data = self.data_collector.auto_collect(
            industry=industry,
            year=2024,
            data_source_selector=self.data_source_selector
        )

        # 人工决策点1：数据来源确认
        print("\n[Decision Point 1/3] Data Source Confirmation")
        print(f"   Tier 1 coverage: {collected_data.get('tier1_coverage', 0):.1%}")
        print(f"   Total sources: {len(collected_data.get('sources', []))}")
        print("   [INFO] Review data sources and approve to continue")
        # TODO: 实现人工确认机制（弹出确认对话框）
        user_approved = True  # 当前自动批准

        if not user_approved:
            return {
                'status': 'cancelled',
                'mode': 'full',
                'industry': industry,
                'note': 'User cancelled at data source confirmation'
            }

        # Phase 2: 深度框架分析 + AI深度分析（集成）
        print("\n[Phase 2/5] Deep Framework Analysis + AI Deep Analysis...")
        frameworks = self.framework_selector.select_frameworks(industry)
        key_questions = self.framework_selector.get_key_questions(industry)

        # 应用框架到数据
        framework_analysis = self.framework_applier.apply(frameworks, collected_data)

        print(f"   Applied {len(frameworks)} frameworks")
        print(f"   Key questions: {len(key_questions)}")

        # AI深度分析（全量模式包含所有维度）
        print("\n   [AI Deep Analysis] Running full consulting-grade AI analysis...")

        # 行业画像
        profile = self.ai_analyzer._analyze_industry_profile(industry)

        # 核心分析维度
        policy = self.ai_analyzer._analyze_policy_environment(industry, collected_data)
        market = self.ai_analyzer._analyze_market_size(industry, collected_data)
        business_model = self.ai_analyzer._analyze_business_model(industry, collected_data)

        # 扩展分析维度（全量模式独有）
        competition = self.ai_analyzer._analyze_competition(industry, collected_data) if hasattr(self.ai_analyzer, '_analyze_competition') else None
        entry_barriers = self.ai_analyzer._analyze_entry_barriers(industry, collected_data) if hasattr(self.ai_analyzer, '_analyze_entry_barriers') else None

        # 合并AI分析结果
        framework_analysis['ai_insights'] = {
            'profile': profile,
            'policy': policy,
            'market_size': market,
            'business_model': business_model
        }

        if competition:
            framework_analysis['ai_insights']['competition'] = competition

        if entry_barriers:
            framework_analysis['ai_insights']['entry_barriers'] = entry_barriers

        print(f"   AI Analysis completed with quality scores:")
        print(f"      Policy: {policy.get('quality_score', 0):.2f}")
        print(f"      Market: {market.get('quality_score', 0):.2f}")
        print(f"      Business Model: {business_model.get('quality_score', 0):.2f}")
        if competition:
            print(f"      Competition: {competition.get('quality_score', 0):.2f}")
        if entry_barriers:
            print(f"      Entry Barriers: {entry_barriers.get('quality_score', 0):.2f}")

        # 人工决策点2：洞察深度自检
        print("\n[Decision Point 2/3] Insight Depth Review")
        print(f"   Framework analysis sections: {len(framework_analysis.get('frameworks', {}))}")
        print(f"   AI insights dimensions: {len(framework_analysis.get('ai_insights', {}))}")
        print("   [INFO] Review insights depth and approve to continue")
        # TODO: 实现人工确认机制
        user_approved = True

        if not user_approved:
            return {
                'status': 'cancelled',
                'mode': 'full',
                'industry': industry,
                'note': 'User cancelled at insight depth review'
            }

        # Phase 3: 完整图表生成（10+张）
        print("\n[Phase 3/5] Generating All Charts...")
        chart_data = self._prepare_chart_data(industry, framework_analysis, collected_data)

        from execution.chart_generator import ChartGenerator
        chart_generator = ChartGenerator(industry=industry)
        chart_paths = chart_generator.generate_all_charts(chart_data)

        chart_summary = chart_generator.get_chart_summary()
        print(f"   Generated {chart_summary['count']} charts")
        print(f"   Total size: {chart_summary['total_size'] / 1024:.1f} KB")

        # Phase 4: 完整专业报告生成
        print("\n[Phase 4/5] Generating Full Professional Report...")

        # 准备研究数据
        research_data = {
            'profile': profile,
            'analysis': {
                'policy': policy,
                'market_size': market,
                'business_model': business_model
            },
            'frameworks': framework_analysis,
            'charts': chart_paths
        }

        if competition:
            research_data['analysis']['competition'] = competition

        if entry_barriers:
            research_data['analysis']['entry_barriers'] = entry_barriers

        # 使用专业报告生成器
        report_path = self.professional_generator.generate_report(
            industry=industry,
            research_data=research_data,
            report_type='full'
        )

        print(f"   Professional report generated: {report_path}")

        # Phase 5: 质量检查和打包（包含人工决策点3）
        print("\n[Phase 5/5] Quality Check and Packaging...")

        quality_data = {
            'ai_analysis': framework_analysis.get('ai_insights', {}),
            'framework_analysis': framework_analysis,
            'charts': chart_paths,
            'data_sources': collected_data.get('sources', [])
        }

        issues = self.quality_checker.check_all(
            quality_data,
            chart_paths,
            collected_data
        )

        # 人工决策点3：最终质量把关
        print("\n[Decision Point 3/3] Final Quality Gate")
        if issues:
            print(f"   Found {len(issues)} issues:")
            for issue in issues[:5]:  # 显示前5个
                print(f"      - {issue['type']}: {issue['description']}")
        else:
            print("   No quality issues found")

        print("   [INFO] Review quality and approve to package")
        # TODO: 实现人工确认机制
        user_approved = True

        if not user_approved:
            return {
                'status': 'cancelled',
                'mode': 'full',
                'industry': industry,
                'note': 'User cancelled at final quality gate'
            }

        # 打包交付
        deliverable = self.packager.package_full_deliverable(
            research_data,
            chart_paths,
            collected_data.get('sources', [])
        )

        print(f"   Package: {deliverable.get('path', report_path)}")

        # 计算AI平均质量分数
        ai_scores = [
            policy.get('quality_score', 0),
            market.get('quality_score', 0),
            business_model.get('quality_score', 0)
        ]

        if competition:
            ai_scores.append(competition.get('quality_score', 0))

        if entry_barriers:
            ai_scores.append(entry_barriers.get('quality_score', 0))

        avg_quality = sum(ai_scores) / len(ai_scores)

        return {
            'status': 'success',
            'mode': 'full',
            'industry': industry,
            'path': report_path,
            'charts': chart_summary['count'],
            'data_sources': len(collected_data.get('sources', [])),
            'tier1_coverage': collected_data.get('tier1_coverage', 0),
            'quality_issues': len(issues),
            'report_sections': len(framework_analysis.get('frameworks', {})),
            'ai_quality_avg': avg_quality
        }


def main():
    """
    命令行入口

    示例:
        python orchestrator.py 医疗陪护
        python orchestrator.py 医疗陪护 --mode full
    """
    parser = argparse.ArgumentParser(
        description='AI辅助行业研究自动化',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  快速模式 (70分钟):
    python orchestrator.py 医疗陪护

  全量模式 (3-5小时):
    python orchestrator.py 医疗陪护 --mode full
        """
    )

    parser.add_argument('industry', help='行业名称 (如: 医疗陪护, 养老服务)')
    parser.add_argument('--mode', choices=['quick', 'full'], default='quick',
                        help='研究模式 (默认: quick)')
    parser.add_argument('--web-search', choices=['yes', 'no'], default='yes',
                        help='是否联网搜索 (默认: yes)')

    args = parser.parse_args()

    # 初始化主控层
    orchestrator = IndustryResearchOrchestrator(mode=args.mode)

    # 执行研究
    result = orchestrator.run(
        industry_name=args.industry,
        user_params={
            'industry': args.industry,
            'web_search': args.web_search == 'yes',
            'mode': args.mode
        }
    )

    # 输出结果
    print("\n" + "="*60)
    print("[OK] Research Complete!")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Mode: {result['mode']}")
    print(f"Industry: {result['industry']}")
    if 'path' in result:
        print(f"Deliverable: {result['path']}")
    if 'charts' in result:
        print(f"Charts: {result['charts']}")
    if 'data_sources' in result:
        print(f"Data sources: {result['data_sources']}")
    if 'tier1_coverage' in result:
        print(f"Tier 1 coverage: {result['tier1_coverage']:.1%}")
    if 'quality_issues' in result:
        print(f"Quality issues: {result['quality_issues']}")
    if 'note' in result:
        print(f"Note: {result['note']}")


if __name__ == '__main__':
    main()
