"""
Interactive Research Session - 交互式研究会话层

核心理念：
- 多轮对话，逐步澄清需求
- 需求明确后再生成任务清单
- 中途可调整、可回顾
- 支持两种后端：Orchestrator（有API）/ PromptOnlyOrchestrator（零API）

使用场景：
1. WorkBuddy在对话中进行研究（零API模式）
2. 命令行交互式研究（有API模式）
3. 企业内部AI能力沉淀

用法示例：
    from core.interactive_session import InteractiveResearchSession

    # 初始化（零API模式）
    session = InteractiveResearchSession(backend='prompt_only')

    # 第一轮对话
    response = session.chat("帮我研究医疗陪护行业")
    # Skill返回：你研究医疗陪护的目的是什么？[选项]

    # 第二轮对话
    response = session.chat("market_entry")
    # Skill返回：推荐分析5个维度，全部分析还是部分？

    # 第三轮对话
    response = session.chat("all")
    # Skill返回：任务清单（5个Prompt）

    # Agent执行并提交结果
    for task in response['tasks']:
        content = agent.analyze(task['prompt'])
        session.submit_result(task['dimension'], content)

    # 中期回顾（自动触发）
    # Skill返回：关键发现 + 建议调整

    # 生成报告
    response = session.chat("continue")
"""

import re
from typing import Dict, List, Optional
from pathlib import Path


class InteractiveResearchSession:
    """
    交互式研究会话

    状态机：
    init → clarify_purpose → confirm_dimensions → execute → review → complete
    """

    def __init__(self, backend='prompt_only'):
        """
        初始化会话

        Args:
            backend: 'auto' / 'prompt_only'
                - 'auto': 使用Orchestrator（需要API密钥）
                - 'prompt_only': 使用PromptOnlyOrchestrator（零API）
        """
        self.backend = backend
        self.state = {
            'stage': 'init',  # 当前阶段
            'industry': None,  # 行业名称
            'research_purpose': None,  # 研究目的
            'research_type': None,  # 研究类型（6种之一）
            'selected_dimensions': [],  # 选定的维度
            'completed_dimensions': [],  # 已完成的维度
            'results': [],  # 分析结果
            'context': {},  # 上下文
            'reviewed': False,  # 是否已中期回顾
            'key_findings': []  # 关键发现
        }

        # 初始化后端执行器
        if backend == 'auto':
            from core.orchestrator import Orchestrator
            self.executor = Orchestrator()
        else:
            from core.prompt_only_orchestrator import PromptOnlyOrchestrator
            self.executor = PromptOnlyOrchestrator()

        print(f"[InteractiveSession] 初始化完成（backend={backend}）")

    def chat(self, user_input: str) -> Dict:
        """
        对话接口 - 核心方法

        Args:
            user_input: 用户输入（自然语言或选项值）

        Returns:
            {
                'type': 'question'/'tasks'/'progress'/'review'/'complete',
                'stage': 当前阶段,
                'message': 回复消息,
                'options': 可选项（如果type='question'）,
                'tasks': 任务清单（如果type='tasks'）,
                'result': 结果（如果type='complete'）
            }
        """
        stage = self.state['stage']

        # 路由到对应阶段的处理函数
        if stage == 'init':
            return self._handle_init(user_input)
        elif stage == 'clarify_purpose':
            return self._handle_clarify_purpose(user_input)
        elif stage == 'confirm_dimensions':
            return self._handle_confirm_dimensions(user_input)
        elif stage == 'execute':
            return self._handle_execute(user_input)
        elif stage == 'review':
            return self._handle_review(user_input)
        elif stage == 'complete':
            return {
                'type': 'complete',
                'stage': 'complete',
                'message': '✅ 研究已完成，会话结束'
            }
        else:
            return {
                'type': 'error',
                'message': f'未知阶段: {stage}'
            }

    def _handle_init(self, user_input: str) -> Dict:
        """
        阶段1: 初始化 - 提取行业名称
        """
        # 提取行业名称
        industry = self._extract_industry(user_input)

        if not industry:
            return {
                'type': 'question',
                'stage': 'init',
                'message': '你想研究哪个行业？',
                'suggestions': [
                    '医疗陪护',
                    '智能制造',
                    '新能源汽车',
                    '产业园区能源',
                    '企业服务SaaS'
                ]
            }

        # 提取成功，进入下一阶段
        self.state['industry'] = industry
        self.state['stage'] = 'clarify_purpose'

        return self._handle_clarify_purpose('')

    def _handle_clarify_purpose(self, user_input: str) -> Dict:
        """
        阶段2: 澄清目的 - 询问研究目的
        """
        industry = self.state['industry']

        # 如果还没有确定研究目的，询问
        if not self.state['research_purpose']:
            return {
                'type': 'question',
                'stage': 'clarify_purpose',
                'message': f'你研究【{industry}】的目的是什么？',
                'options': [
                    {
                        'value': 'market_entry',
                        'label': '市场进入可行性',
                        'desc': '评估进入该市场的机会、壁垒、风险',
                        'emoji': '🚀'
                    },
                    {
                        'value': 'investment',
                        'label': '投资尽调',
                        'desc': '评估标的公司价值、壁垒、估值',
                        'emoji': '💰'
                    },
                    {
                        'value': 'competition',
                        'label': '竞争分析',
                        'desc': '分析市场格局、对手策略、差异化机会',
                        'emoji': '⚔️'
                    },
                    {
                        'value': 'overview',
                        'label': '行业概览',
                        'desc': '全面了解行业政策、规模、趋势',
                        'emoji': '📊'
                    },
                    {
                        'value': 'custom',
                        'label': '自定义',
                        'desc': '我自己选择分析维度',
                        'emoji': '🎯'
                    }
                ]
            }

        # 解析用户选择
        purpose = self._parse_purpose(user_input)
        self.state['research_purpose'] = purpose

        # 映射到研究类型
        purpose_map = {
            'market_entry': '市场进入可行性',
            'investment': '投资尽调',
            'competition': '公司对标',
            'overview': '行业分析'
        }
        self.state['research_type'] = purpose_map.get(purpose, '行业分析')

        # 进入下一阶段：确认维度
        self.state['stage'] = 'confirm_dimensions'
        return self._handle_confirm_dimensions('')

    def _handle_confirm_dimensions(self, user_input: str) -> Dict:
        """
        阶段3: 确认维度 - 推荐维度并让用户确认
        """
        purpose = self.state['research_purpose']

        # 如果还没有选定维度，推荐维度
        if not self.state['selected_dimensions']:
            if purpose == 'custom':
                # 让用户自己选
                return {
                    'type': 'question',
                    'stage': 'confirm_dimensions',
                    'message': '请选择要分析的维度（可多选）：',
                    'options': self._get_available_dimensions(),
                    'multi_select': True
                }
            else:
                # 推荐维度
                recommended = self._get_recommended_dimensions(purpose)
                estimated_time = len(recommended) * 8  # 估算时间

                return {
                    'type': 'confirm',
                    'stage': 'confirm_dimensions',
                    'message': f'基于「{self._format_purpose(purpose)}」，我推荐分析以下维度：',
                    'dimensions': recommended,
                    'estimated_time': estimated_time,
                    'options': [
                        {
                            'value': 'all',
                            'label': f'全部分析（预计{estimated_time}分钟）',
                            'emoji': '✅'
                        },
                        {
                            'value': 'select',
                            'label': '我来选择部分',
                            'emoji': '🎯'
                        },
                        {
                            'value': 'quick',
                            'label': '快速版（3-4个核心维度）',
                            'emoji': '⚡'
                        }
                    ]
                }

        # 解析用户选择
        selection = self._parse_dimension_selection(user_input)
        self.state['selected_dimensions'] = selection

        # 进入执行阶段
        self.state['stage'] = 'execute'
        return self._handle_execute('')

    def _handle_execute(self, user_input: str) -> Dict:
        """
        阶段4: 执行分析

        - backend='auto': 自动执行，返回结果
        - backend='prompt_only': 返回任务清单
        """
        dimensions = self.state['selected_dimensions']
        industry = self.state['industry']
        research_type = self.state['research_type']

        if self.backend == 'auto':
            # 自动执行模式（有API）
            print(f"\n[InteractiveSession] 开始自动执行分析...")

            result = self.executor.run(
                industry=industry,
                user_params={
                    'dimensions': dimensions,
                    'research_type': research_type
                }
            )

            self.state['results'] = result.get('analysis_results', [])
            self.state['stage'] = 'complete'

            return {
                'type': 'complete',
                'stage': 'complete',
                'message': f'✅ 分析完成！共分析了{len(dimensions)}个维度',
                'report_path': result.get('path'),
                'quality': result.get('quality'),
                'dimensions': dimensions
            }
        else:
            # Prompt-Only模式（零API）
            print(f"\n[InteractiveSession] 生成任务清单...")

            tasks = self.executor.get_research_tasks(
                industry=industry,
                dimensions=dimensions,
                research_type=research_type
            )

            return {
                'type': 'tasks',
                'stage': 'execute',
                'message': f'已生成{len(tasks)}个分析任务，请Agent逐个执行：',
                'tasks': tasks,
                'total': len(tasks),
                'industry': industry
            }

    def submit_result(self, dimension: str, content: str, quality_score: float = None):
        """
        提交单个维度的分析结果（Prompt-Only模式使用）

        Args:
            dimension: 维度名称
            content: 分析内容
            quality_score: 质量分数（可选，自动计算）

        Returns:
            {
                'type': 'progress'/'review'/'complete',
                'message': 进度消息,
                ...
            }
        """
        # 评估质量（如果没有提供）
        if quality_score is None:
            quality_score = self.executor.engine.assess_content_quality(content)

        # 存储结果
        result = {
            'dimension': dimension,
            'content': content,
            'quality_score': quality_score
        }
        self.state['results'].append(result)
        self.state['completed_dimensions'].append(dimension)
        self.state['context'][dimension] = content

        # 计算进度
        total = len(self.state['selected_dimensions'])
        completed = len(self.state['completed_dimensions'])

        # 检查是否需要中期回顾（完成一半时）
        if completed >= total // 2 and not self.state['reviewed'] and total > 3:
            self.state['stage'] = 'review'
            return self._mid_point_review()

        # 检查是否全部完成
        if completed >= total:
            self.state['stage'] = 'complete'
            return self._generate_final_report()

        # 返回进度
        next_dimension = self.state['selected_dimensions'][completed]

        return {
            'type': 'progress',
            'stage': 'execute',
            'message': f'✅ {dimension} 分析完成',
            'quality_score': quality_score,
            'completed': completed,
            'total': total,
            'progress': f'{completed}/{total}',
            'next_dimension': next_dimension
        }

    def _handle_review(self, user_input: str) -> Dict:
        """
        阶段5: 中期回顾 - 用户决定是否继续/调整
        """
        choice = user_input.strip().lower()

        if choice == 'continue' or choice == '1':
            # 继续按计划
            self.state['stage'] = 'execute'
            remaining = [d for d in self.state['selected_dimensions']
                        if d not in self.state['completed_dimensions']]

            return {
                'type': 'continue',
                'stage': 'execute',
                'message': f'继续分析剩余{len(remaining)}个维度',
                'remaining_dimensions': remaining
            }

        elif choice == 'finish' or choice == '3':
            # 提前生成报告
            self.state['stage'] = 'complete'
            return self._generate_final_report()

        elif choice == 'adjust' or choice == '2':
            # 调整维度（暂不实现，返回继续）
            self.state['stage'] = 'execute'
            return {
                'type': 'adjust',
                'stage': 'execute',
                'message': '维度调整功能开发中，继续按原计划执行'
            }

        else:
            # 未识别，重新询问
            return self._mid_point_review()

    def _mid_point_review(self) -> Dict:
        """
        中期回顾：提取关键发现，询问是否调整
        """
        self.state['reviewed'] = True

        # 提取关键发现
        key_findings = self._extract_key_findings(self.state['results'])
        self.state['key_findings'] = key_findings

        # 推荐后续维度（基于已有发现）
        suggested = self._suggest_next_dimensions(key_findings)

        completed = len(self.state['completed_dimensions'])
        total = len(self.state['selected_dimensions'])

        return {
            'type': 'review',
            'stage': 'review',
            'message': f'📊 已完成{completed}/{total}个维度，中期回顾：',
            'key_findings': key_findings,
            'suggested_next': suggested,
            'options': [
                {'value': 'continue', 'label': '继续按计划', 'emoji': '✅'},
                {'value': 'adjust', 'label': '调整维度', 'emoji': '🔧'},
                {'value': 'finish', 'label': '够了，生成报告', 'emoji': '📄'}
            ]
        }

    def _generate_final_report(self) -> Dict:
        """
        生成最终报告
        """
        print(f"\n[InteractiveSession] 生成最终报告...")

        report = self.executor.generate_report(
            industry=self.state['industry'],
            analysis_results=self.state['results'],
            export_formats=[]  # 可选：['word', 'markdown']
        )

        return {
            'type': 'complete',
            'stage': 'complete',
            'message': '✅ 研究完成！',
            'report_path': report.get('path'),
            'quality': report.get('quality'),
            'dimensions_analyzed': self.state['completed_dimensions'],
            'total_dimensions': len(self.state['completed_dimensions'])
        }

    # ==================== 辅助方法 ====================

    def _extract_industry(self, text: str) -> Optional[str]:
        """从文本中提取行业名称"""
        # 简单模式匹配
        patterns = [
            r'研究(.{2,10}?)行业',
            r'分析(.{2,10}?)行业',
            r'(.{2,10}?)行业研究',
            r'(.{2,10}?)行业分析',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # 如果没有匹配，返回None
        return None

    def _parse_purpose(self, text: str) -> str:
        """解析研究目的"""
        text_lower = text.lower().strip()

        if text_lower in ['market_entry', '1', '市场进入', '进入']:
            return 'market_entry'
        elif text_lower in ['investment', '2', '投资', '尽调']:
            return 'investment'
        elif text_lower in ['competition', '3', '竞争', '对手']:
            return 'competition'
        elif text_lower in ['overview', '4', '概览', '了解']:
            return 'overview'
        elif text_lower in ['custom', '5', '自定义']:
            return 'custom'
        else:
            # 默认
            return 'overview'

    def _parse_dimension_selection(self, text: str) -> List[str]:
        """解析维度选择"""
        text_lower = text.lower().strip()
        purpose = self.state['research_purpose']

        if text_lower in ['all', '1', '全部', '全部分析']:
            # 全部分析
            return self._get_recommended_dimensions(purpose)
        elif text_lower in ['quick', '3', '快速', '快速版']:
            # 快速版（前3-4个核心维度）
            recommended = self._get_recommended_dimensions(purpose)
            return recommended[:min(4, len(recommended))]
        else:
            # 默认全部
            return self._get_recommended_dimensions(purpose)

    def _get_recommended_dimensions(self, purpose: str) -> List[str]:
        """根据研究目的推荐维度"""
        dimension_map = {
            'market_entry': ['市场规模', '进入壁垒', '竞争格局', '单位经济', '风险分析'],
            'investment': ['行业画像', '商业模式', '竞争壁垒', '市场规模', '估值测算'],
            'competition': ['竞争格局', '商业模式', '核心能力', '进入壁垒'],
            'overview': ['行业画像', '政策环境', '市场规模', '竞争格局', '商业模式', '风险分析', '战略建议']
        }
        return dimension_map.get(purpose, dimension_map['overview'])

    def _get_available_dimensions(self) -> List[Dict]:
        """获取所有可用维度（供用户自定义选择）"""
        dimensions = [
            {'value': '行业画像', 'label': '行业画像', 'desc': '行业规模、增速、生命周期'},
            {'value': '政策环境', 'label': '政策环境', 'desc': 'PEST分析、政策影响'},
            {'value': '市场规模', 'label': '市场规模', 'desc': 'TAM/SAM/SOM、增长驱动'},
            {'value': '商业模式', 'label': '商业模式', 'desc': '四方决策链、单位经济'},
            {'value': '竞争格局', 'label': '竞争格局', 'desc': 'Porter五力、CR4'},
            {'value': '进入壁垒', 'label': '进入壁垒', 'desc': '五大壁垒、突破路径'},
            {'value': '风险分析', 'label': '风险分析', 'desc': 'PESTEL风险、应对措施'},
            {'value': '战略建议', 'label': '战略建议', 'desc': '市场进入策略、行动计划'}
        ]
        return dimensions

    def _format_purpose(self, purpose: str) -> str:
        """格式化研究目的为中文"""
        purpose_names = {
            'market_entry': '市场进入可行性',
            'investment': '投资尽调',
            'competition': '竞争分析',
            'overview': '行业概览',
            'custom': '自定义'
        }
        return purpose_names.get(purpose, purpose)

    def _extract_key_findings(self, results: List[Dict]) -> List[Dict]:
        """从已完成的结果中提取关键发现"""
        findings = []

        for result in results:
            dimension = result['dimension']
            content = result['content']

            # 简单提取：取前200字作为摘要
            summary = content[:200] + '...' if len(content) > 200 else content

            findings.append({
                'dimension': dimension,
                'summary': summary,
                'quality_score': result.get('quality_score', 0)
            })

        return findings

    def _suggest_next_dimensions(self, key_findings: List[Dict]) -> List[str]:
        """基于关键发现，推荐后续维度"""
        # 简化版：根据已完成的维度推荐
        completed = set(self.state['completed_dimensions'])
        all_dimensions = set(self.state['selected_dimensions'])
        remaining = list(all_dimensions - completed)

        # 返回剩余维度（可以根据findings智能排序）
        return remaining[:3]  # 最多推荐3个
