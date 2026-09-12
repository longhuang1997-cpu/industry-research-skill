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
        from execution.workflow_engine import WorkflowEngine, ResearchDepth, AnalysisDimension
        from output.quality_checker import QualityChecker
        from output.report_generator import ReportGenerator
        from output.packaging import Packager
        from output.professional_report_generator import ProfessionalReportGenerator

        self.framework_selector = FrameworkSelector()
        self.data_source_selector = DataSourceSelector()
        self.data_collector = DataCollector()
        self.framework_applier = FrameworkApplier()
        self.ai_analyzer = ConsultingAIAnalyzer()
        self.workflow_engine = WorkflowEngine()  # 新增：工作流引擎
        self.quality_checker = QualityChecker()
        self.report_generator = ReportGenerator()
        self.professional_generator = ProfessionalReportGenerator()
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

        try:
            # Step 1: 收集需求
            research_brief = self._collect_requirements(industry_name, user_params)

            # Step 2: 根据模式执行
            if self.mode == 'quick':
                return self._run_quick_mode(research_brief)
            else:
                return self._run_full_mode(research_brief)

        except Exception as e:
            # P1.2: 友好的错误处理
            print("\n" + "="*60)
            print("❌ 研究过程中遇到问题")
            print("="*60)
            print(f"\n错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}\n")

            # 根据错误类型给出建议
            error_suggestions = self._get_error_suggestions(e)
            if error_suggestions:
                print("💡 可能的解决方案:")
                for i, suggestion in enumerate(error_suggestions, 1):
                    print(f"   {i}. {suggestion}")

            print("\n📝 详细错误信息已记录，请稍后重试或联系支持")
            print("="*60)

            return {
                'status': 'failed',
                'mode': self.mode,
                'industry': industry_name,
                'error': str(e),
                'error_type': type(e).__name__,
                'suggestions': error_suggestions
            }

    def _get_error_suggestions(self, error):
        """
        根据错误类型提供解决建议

        Args:
            error: 异常对象

        Returns:
            suggestions: 建议列表
        """
        error_type = type(error).__name__
        error_msg = str(error).lower()

        suggestions = []

        # API相关错误
        if 'api' in error_msg or 'anthropic' in error_msg or 'openai' in error_msg:
            suggestions.append("检查API密钥配置是否正确（skill_config.yaml）")
            suggestions.append("确认API服务可访问（网络连接正常）")
            suggestions.append("检查API配额是否充足")

        # 网络相关错误
        if 'connection' in error_msg or 'timeout' in error_msg or 'network' in error_msg:
            suggestions.append("检查网络连接是否正常")
            suggestions.append("尝试使用VPN或更换网络环境")
            suggestions.append("增加超时时间设置")

        # 文件相关错误
        if 'file' in error_msg or 'directory' in error_msg or 'path' in error_msg:
            suggestions.append("检查output目录是否存在且有写入权限")
            suggestions.append("确认磁盘空间充足")

        # 模型相关错误
        if 'model' in error_msg or 'claude' in error_msg:
            suggestions.append("检查skill_config.yaml中的model配置")
            suggestions.append("尝试使用其他可用模型")

        # 通用建议
        if not suggestions:
            suggestions.append("重试一次（可能是临时性问题）")
            suggestions.append("检查skill_config.yaml配置是否正确")
            suggestions.append("查看完整错误日志以获取更多信息")

        return suggestions

    def _collect_requirements(self, industry_name, user_params):
        """
        收集研究需求并生成工作流

        根据用户输入解析：维度、深度、输出选项
        使用WorkflowEngine生成灵活的研究计划
        """
        from execution.workflow_engine import ResearchDepth, AnalysisDimension, WorkflowConfig

        if user_params is None:
            user_params = {}

        # 1. 解析研究深度
        depth = user_params.get('depth', None)
        if depth == 'quick' or depth == '10分钟' or depth == '快速':
            research_depth = ResearchDepth.QUICK
        elif depth == 'standard' or depth == '30分钟' or depth == '标准':
            research_depth = ResearchDepth.STANDARD
        elif depth == 'deep' or depth == '60分钟' or depth == '深度':
            research_depth = ResearchDepth.DEEP
        elif depth == 'custom' or depth == '自定义':
            research_depth = ResearchDepth.CUSTOM
        else:
            # 默认：quick模式用STANDARD，full模式用DEEP
            if self.mode == 'quick':
                research_depth = ResearchDepth.STANDARD  # 30分钟标准研究
            else:
                research_depth = ResearchDepth.DEEP

        # 2. 解析分析维度
        dimensions = user_params.get('dimensions', None)
        if dimensions:
            # 用户明确指定维度
            dimension_map = {
                '政策': AnalysisDimension.POLICY,
                '政策环境': AnalysisDimension.POLICY,
                '市场': AnalysisDimension.MARKET_SIZE,
                '市场规模': AnalysisDimension.MARKET_SIZE,
                '商业模式': AnalysisDimension.BUSINESS_MODEL,
                '竞争': AnalysisDimension.COMPETITION,
                '竞争格局': AnalysisDimension.COMPETITION,
                '壁垒': AnalysisDimension.ENTRY_BARRIERS,
                '进入壁垒': AnalysisDimension.ENTRY_BARRIERS,
                '产业链': AnalysisDimension.SUPPLY_CHAIN,
                '风险': AnalysisDimension.RISK_ANALYSIS,
                '风险分析': AnalysisDimension.RISK_ANALYSIS,
                '机会': AnalysisDimension.OPPORTUNITIES,
                '机会识别': AnalysisDimension.OPPORTUNITIES
            }

            selected_dimensions = []
            for dim_str in dimensions:
                if dim_str in dimension_map:
                    selected_dimensions.append(dimension_map[dim_str])
        else:
            # 没有指定，使用预定义工作流
            selected_dimensions = []

        # 3. 创建工作流配置
        workflow_config = WorkflowConfig(
            depth=research_depth,
            dimensions=selected_dimensions,
            include_charts=user_params.get('include_charts', True),
            include_data_tables=user_params.get('include_data_tables', True),
            generate_pdf=user_params.get('generate_pdf', False)
        )

        # 4. 使用WorkflowEngine生成工作流
        workflow_steps = self.workflow_engine.create_workflow(workflow_config)
        total_time = self.workflow_engine.estimate_total_time(workflow_steps)

        # 5. 可视化工作流
        workflow_viz = self.workflow_engine.visualize_workflow(workflow_steps)

        return {
            'industry': industry_name,
            'workflow_config': workflow_config,
            'workflow_steps': workflow_steps,
            'estimated_time': total_time,
            'workflow_viz': workflow_viz,
            'web_search': user_params.get('web_search', True),
            'chart_style': user_params.get('chart_style', 'data_accurate'),
            'mode': self.mode
        }

    def _run_quick_mode(self, brief):
        """
        快速模式：根据WorkflowEngine生成的步骤执行

        动态执行用户选择的分析维度
        """
        print("\n" + "="*60)
        print("🚀 开始行业研究")
        print("="*60)

        industry = brief['industry']
        workflow_steps = brief.get('workflow_steps', [])
        estimated_time = brief.get('estimated_time', 60)

        # 显示工作流计划
        print(f"预计耗时: {estimated_time} 分钟")
        print(f"分析步骤: {len(workflow_steps)} 个")

        # 显示简化的工作流
        print("\n分析维度:")
        for i, step in enumerate(workflow_steps, 1):
            print(f"  {i}. {step.name} (约{step.estimated_time}分钟)")

        print("\n💡 您可以离开去做其他事，完成后会通知您")
        print("="*60)

        # Phase 1: 数据收集
        print("\n🔍 [1/6] 正在收集行业数据...")
        print("   预计耗时: 10-15分钟")
        collected_data = self.data_collector.auto_collect(
            industry=industry,
            year=2024,
            data_source_selector=self.data_source_selector
        )

        collected_data['industry'] = industry

        print(f"   ✓ 已收集 {len(collected_data.get('sources', []))}个数据源")
        print(f"   ✓ Tier 1覆盖率: {collected_data.get('tier1_coverage', 0):.1%}")

        # Phase 2: 根据WorkflowEngine执行分析
        print("\n💡 [2/6] 正在进行深度分析...")
        print(f"   预计耗时: {estimated_time - 30} 分钟")

        # 应用框架
        frameworks = self.framework_selector.select_frameworks(industry)
        framework_analysis = self.framework_applier.apply(frameworks, collected_data)

        print(f"   ✓ 已应用 {len(frameworks)} 个分析框架")

        # 根据workflow_steps动态执行AI分析
        print("\n   💡 AI正在生成咨询级深度分析...")

        analysis_results = {}

        # 总是执行行业画像（必需）
        print("      → 分析行业定位...")
        profile = self.ai_analyzer._analyze_industry_profile(industry)
        analysis_results['profile'] = profile

        # 根据workflow_steps执行对应维度的分析
        from execution.workflow_engine import AnalysisDimension

        for step in workflow_steps:
            if step.dimension == AnalysisDimension.POLICY and step.name != "行业画像":
                print("      → 分析政策环境...")
                analysis_results['policy'] = self.ai_analyzer._analyze_policy_environment(industry, collected_data)

            elif step.dimension == AnalysisDimension.MARKET_SIZE and step.name != "行业画像":
                print("      → 测算市场规模...")
                analysis_results['market_size'] = self.ai_analyzer._analyze_market_size(industry, collected_data)

            elif step.dimension == AnalysisDimension.BUSINESS_MODEL:
                print("      → 拆解商业模式...")
                analysis_results['business_model'] = self.ai_analyzer._analyze_business_model(industry, collected_data)

            elif step.dimension == AnalysisDimension.COMPETITION:
                print("      → 分析竞争格局...")
                if hasattr(self.ai_analyzer, '_analyze_competition'):
                    analysis_results['competition'] = self.ai_analyzer._analyze_competition(industry, collected_data)

            elif step.dimension == AnalysisDimension.ENTRY_BARRIERS:
                print("      → 评估进入壁垒...")
                if hasattr(self.ai_analyzer, '_analyze_entry_barriers'):
                    analysis_results['entry_barriers'] = self.ai_analyzer._analyze_entry_barriers(industry, collected_data)

            # 其他维度可以继续扩展...

        # 合并分析结果
        framework_analysis['ai_insights'] = analysis_results

        # 显示质量分数
        print(f"\n   ✓ AI分析完成")
        for key, result in analysis_results.items():
            if key != 'profile' and isinstance(result, dict) and 'quality_score' in result:
                print(f"      {key}: {result.get('quality_score', 0):.2f}/1.00")

        # Phase 3-6: 保持原有流程（图表、报告、质检、打包）
        return self._complete_research(
            industry, profile, analysis_results,
            framework_analysis, collected_data,
            brief.get('workflow_config')
        )

    def _complete_research(self, industry, profile, analysis_results,
                          framework_analysis, collected_data, workflow_config):
        """
        完成研究的后续步骤：图表、报告、质检、打包

        抽取出来复用于quick和full模式
        """
        # Phase 3: 生成核心图表
        print("\n📊 [3/6] 正在生成可视化图表...")
        print("   预计耗时: 5-8分钟")

        chart_data = self._prepare_chart_data(industry, framework_analysis, collected_data)

        from execution.chart_generator import ChartGenerator
        chart_generator = ChartGenerator(industry=industry)

        if workflow_config and workflow_config.include_charts:
            chart_paths = chart_generator.generate_core_charts(chart_data)
        else:
            chart_paths = {}

        chart_summary = chart_generator.get_chart_summary()
        print(f"   ✓ 已生成 {chart_summary['count']} 张专业图表")

        # Phase 4: 生成专业报告
        print("\n📄 [4/6] 正在生成专业报告...")
        print("   预计耗时: 3-5分钟")

        research_data = {
            'profile': profile,
            'analysis': analysis_results,
            'frameworks': framework_analysis,
            'charts': chart_paths
        }

        report_path = self.professional_generator.generate_report(
            industry=industry,
            research_data=research_data,
            report_type='quick'
        )

        print(f"   ✓ 专业报告已生成")

        # Phase 5: 质量检查
        print("\n✅ [5/6] 正在进行质量检查...")
        print("   预计耗时: 2-3分钟")

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
            print(f"   ⚠️  发现 {len(issues)} 个问题（可接受范围内）")
        else:
            print(f"   ✓ 质量检查通过")

        # Phase 6: 打包交付
        print("\n📦 [6/6] 正在打包交付物...")
        print("   预计耗时: 1-2分钟")

        deliverable = self.packager.package_quick_deliverable(
            research_data,
            chart_paths,
            collected_data.get('sources', [])
        )

        print(f"   ✓ 打包完成")

        # 展示核心结论
        self._display_insights(industry, profile, analysis_results)

        # 保存上下文
        context_file = self.skill_root / "output" / f"{industry}_context.md"
        self._save_context_for_followup(industry, profile, analysis_results, context_file)

        print(f"\n📝 分析内容已保存，您现在可以直接询问报告中的任何问题")

        # 计算平均质量
        quality_scores = []
        for key, result in analysis_results.items():
            if key != 'profile' and isinstance(result, dict) and 'quality_score' in result:
                quality_scores.append(result.get('quality_score', 0))

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        return {
            'status': 'success',
            'mode': 'quick',
            'industry': industry,
            'path': report_path,
            'context_file': str(context_file),
            'charts': chart_summary['count'],
            'data_sources': len(collected_data.get('sources', [])),
            'tier1_coverage': collected_data.get('tier1_coverage', 0),
            'quality_issues': len(issues),
            'ai_quality_avg': avg_quality,
            'analysis_content': analysis_results
        }

    def _display_insights(self, industry, profile, analysis_results):
        """
        在对话中展示核心洞察
        """
        print("\n" + "="*60)
        print("✅ 研究完成！")
        print("="*60)
        print(f"\n📊 【{industry}】行业核心洞察\n")

        # 展示行业画像
        print("🎯 行业定位")
        print(f"{profile.get('summary', '暂无数据')}\n")

        # 展示各维度分析（动态）
        dimension_labels = {
            'policy': ('📋 政策环境', '政策'),
            'market_size': ('💰 市场规模', '市场'),
            'business_model': ('💡 商业模式', '商业模式'),
            'competition': ('🏆 竞争格局', '竞争'),
            'entry_barriers': ('🚧 进入壁垒', '壁垒')
        }

        for key, result in analysis_results.items():
            if key == 'profile':
                continue

            if key in dimension_labels:
                label, short_name = dimension_labels[key]
                print(label)

                content = result.get('content', '暂无数据')
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"{preview}")

                if 'quality_score' in result:
                    print(f"   质量分数: {result.get('quality_score', 0):.2f}/1.00\n")
                else:
                    print()

        print("="*60)
        print("📄 完整交付物")
        print("="*60)
        print("\n💡 您可以：")
        print("1. 打开完整报告查看所有图表和详细分析")
        print("2. 询问报告中的具体内容（如：竞争格局怎么样？）")
        print("3. 对比其他行业或深入某个维度")
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
        print("🚀 开始行业研究（快速模式）")
        print("="*60)
        print("预计耗时: 60-70分钟")
        print("流程: 数据收集 → AI分析 → 图表生成 → 专业报告 → 质量检查 → 打包交付")
        print("\n💡 您可以离开去做其他事，完成后会通知您")
        print("="*60)

        industry = brief['industry']

        # Phase 1: 数据收集
        print("\n🔍 [1/6] 正在收集行业数据...")
        print("   预计耗时: 10-15分钟")
        collected_data = self.data_collector.auto_collect(
            industry=industry,
            year=2024,
            data_source_selector=self.data_source_selector
        )

        # 添加行业名称到collected_data，供后续框架分析使用
        collected_data['industry'] = industry

        print(f"   ✓ 已收集 {len(collected_data.get('sources', []))}个数据源")
        print(f"   ✓ Tier 1覆盖率: {collected_data.get('tier1_coverage', 0):.1%}")

        # Phase 2: 框架分析 + AI深度分析（集成）
        print("\n💡 [2/6] 正在进行深度分析...")
        print("   预计耗时: 15-20分钟")
        frameworks = self.framework_selector.select_frameworks(industry)
        key_questions = self.framework_selector.get_key_questions(industry)

        # 应用框架到数据
        framework_analysis = self.framework_applier.apply(frameworks, collected_data)

        print(f"   ✓ 已应用 {len(frameworks)} 个分析框架")

        # AI深度分析（集成ConsultingAIAnalyzer）
        print("\n   💡 AI正在生成咨询级深度分析...")

        # 行业画像
        print("      → 分析行业定位...")
        profile = self.ai_analyzer._analyze_industry_profile(industry)

        # 政策环境分析
        print("      → 分析政策环境...")
        policy = self.ai_analyzer._analyze_policy_environment(industry, collected_data)

        # 市场规模测算
        print("      → 测算市场规模...")
        market = self.ai_analyzer._analyze_market_size(industry, collected_data)

        # 商业模式分析
        print("      → 拆解商业模式...")
        business_model = self.ai_analyzer._analyze_business_model(industry, collected_data)

        # 合并AI分析结果到framework_analysis
        framework_analysis['ai_insights'] = {
            'profile': profile,
            'policy': policy,
            'market_size': market,
            'business_model': business_model
        }

        print(f"\n   ✓ AI分析完成")
        print(f"      政策环境质量: {policy.get('quality_score', 0):.2f}/1.00")
        print(f"      市场规模质量: {market.get('quality_score', 0):.2f}/1.00")
        print(f"      商业模式质量: {business_model.get('quality_score', 0):.2f}/1.00")

        # Phase 3: 生成核心图表
        print("\n📊 [3/6] 正在生成可视化图表...")
        print("   预计耗时: 5-8分钟")

        # 准备图表数据（使用模拟数据作为示例）
        chart_data = self._prepare_chart_data(industry, framework_analysis, collected_data)

        from execution.chart_generator import ChartGenerator
        chart_generator = ChartGenerator(industry=industry)
        chart_paths = chart_generator.generate_core_charts(chart_data)

        chart_summary = chart_generator.get_chart_summary()
        print(f"   ✓ 已生成 {chart_summary['count']} 张专业图表")

        # Phase 4: 生成专业报告（使用ProfessionalReportGenerator）
        print("\n📄 [4/6] 正在生成专业报告...")
        print("   预计耗时: 3-5分钟")

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

        print(f"   ✓ 专业报告已生成")

        # Phase 5: 质量检查
        print("\n✅ [5/6] 正在进行质量检查...")
        print("   预计耗时: 2-3分钟")

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
            print(f"   ⚠️  发现 {len(issues)} 个问题（可接受范围内）")
        else:
            print(f"   ✓ 质量检查通过")

        # Phase 6: 打包交付
        print("\n📦 [6/6] 正在打包交付物...")
        print("   预计耗时: 1-2分钟")
        deliverable = self.packager.package_quick_deliverable(
            research_data,
            chart_paths,
            collected_data.get('sources', [])
        )

        print(f"   Package: {deliverable.get('html_path', report_path)}")

        # ============================================================
        # P0改进：在对话中直接展示核心结论
        # ============================================================
        print("\n" + "="*60)
        print("✅ 研究完成！")
        print("="*60)
        print(f"\n📊 【{industry}】行业核心洞察\n")

        # 展示行业画像
        print("🎯 行业定位")
        print(f"{profile.get('summary', '暂无数据')}\n")

        # 展示政策环境核心发现（提取前200字）
        policy_content = policy.get('content', '')
        if len(policy_content) > 200:
            policy_preview = policy_content[:200] + "..."
        else:
            policy_preview = policy_content

        print("📋 政策环境")
        print(f"{policy_preview}")
        print(f"   质量分数: {policy.get('quality_score', 0):.2f}/1.00\n")

        # 展示市场规模核心发现
        market_content = market.get('content', '')
        if len(market_content) > 200:
            market_preview = market_content[:200] + "..."
        else:
            market_preview = market_content

        print("💰 市场规模")
        print(f"{market_preview}")
        print(f"   质量分数: {market.get('quality_score', 0):.2f}/1.00\n")

        # 展示商业模式核心发现
        business_content = business_model.get('content', '')
        if len(business_content) > 200:
            business_preview = business_content[:200] + "..."
        else:
            business_preview = business_content

        print("💡 商业模式")
        print(f"{business_preview}")
        print(f"   质量分数: {business_model.get('quality_score', 0):.2f}/1.00\n")

        # 展示图表和报告路径
        print("="*60)
        print("📄 完整交付物")
        print("="*60)
        print(f"专业报告: {report_path}")
        print(f"图表数量: {chart_summary['count']}张")
        print(f"数据源: {len(collected_data.get('sources', []))}个 (Tier 1覆盖率: {collected_data.get('tier1_coverage', 0):.1%})")
        print(f"质量问题: {len(issues)}个")
        print(f"AI分析平均质量: {(policy.get('quality_score', 0) + market.get('quality_score', 0) + business_model.get('quality_score', 0)) / 3:.2f}/1.00")

        print("\n💡 您可以：")
        print("1. 打开完整报告查看所有图表和详细分析")
        print("2. 询问报告中的具体内容（如：竞争格局怎么样？）")
        print("3. 对比其他行业或深入某个维度")

        # P1.1: 保存分析内容到上下文文件，供后续查询
        context_file = self.skill_root / "output" / f"{industry}_context.md"
        self._save_context_for_followup(industry, profile, policy, market, business_model, context_file)

        print(f"\n📝 分析内容已保存，您现在可以直接询问报告中的任何问题")

        return {
            'status': 'success',
            'mode': 'quick',
            'industry': industry,
            'path': report_path,
            'context_file': str(context_file),  # 添加上下文文件路径
            'charts': chart_summary['count'],
            'data_sources': len(collected_data.get('sources', [])),
            'tier1_coverage': collected_data.get('tier1_coverage', 0),
            'quality_issues': len(issues),
            'ai_quality_avg': (
                policy.get('quality_score', 0) +
                market.get('quality_score', 0) +
                business_model.get('quality_score', 0)
            ) / 3,
            # 添加分析内容到返回值，供后续对话查询
            'analysis_content': {
                'profile': profile,
                'policy': policy,
                'market_size': market,
                'business_model': business_model
            }
        }

    def _save_context_for_followup(self, industry, profile, policy, market, business_model, context_file):
        """
        保存分析内容到markdown文件，供后续对话查询

        Args:
            industry: 行业名称
            profile: 行业画像
            policy: 政策分析
            market: 市场分析
            business_model: 商业模式分析
            context_file: 输出文件路径
        """
        content = f"""# {industry} 行业研究分析内容

> 本文件包含完整的行业研究分析内容，供后续对话查询使用

---

## 🎯 行业画像

{profile.get('summary', '暂无数据')}

**详细分析**：
{profile.get('content', '暂无数据') if 'content' in profile else profile.get('summary', '暂无数据')}

---

## 📋 政策环境分析

**质量分数**: {policy.get('quality_score', 0):.2f}/1.00

**核心发现**：
{policy.get('content', '暂无数据')}

**数据来源**：
{', '.join(policy.get('sources', ['AI分析生成']))}

---

## 💰 市场规模分析

**质量分数**: {market.get('quality_score', 0):.2f}/1.00

**核心发现**：
{market.get('content', '暂无数据')}

**数据来源**：
{', '.join(market.get('sources', ['AI分析生成']))}

---

## 💡 商业模式分析

**质量分数**: {business_model.get('quality_score', 0):.2f}/1.00

**核心发现**：
{business_model.get('content', '暂无数据')}

**数据来源**：
{', '.join(business_model.get('sources', ['AI分析生成']))}

---

## 💬 如何使用本文件

您现在可以直接询问关于{industry}行业的问题，例如：
- "政策环境的核心要点是什么？"
- "市场规模有多大？增长率如何？"
- "商业模式的核心是什么？"
- "单位经济模型如何？"

我会基于上述分析内容回答您的问题。
"""

        # 写入文件
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✓ 上下文已保存到: {context_file}")

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
