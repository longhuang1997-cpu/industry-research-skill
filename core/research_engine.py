"""
Industry Research Skill - 统一研究引擎

架构决策（2026-09-12重构）：
- 用Prompt工程替代复杂脚本逻辑
- 合并分散模块，高内聚低耦合
- AI推理 > 硬编码规则

核心能力：
1. 意图理解（自然语言→结构化参数）
2. 动态工作流（按需生成研究流程）
3. 咨询级分析（PEST/Porter/四方决策链等框架）
4. 质量保证（自动评分+修复建议）
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path


class ResearchEngine:
    """统一研究引擎 - Skill的核心大脑"""

    # ==================== 分析维度定义 ====================
    DIMENSIONS = {
        # 通用维度（适用于多种研究类型）
        '行业画像': {
            'time': 2,  # 分钟
            'required': True,
            'prompt_template': 'profile'
        },
        '政策环境': {
            'time': 8,
            'dependencies': ['行业画像'],
            'prompt_template': 'policy'
        },
        '市场规模': {
            'time': 8,
            'dependencies': ['行业画像'],
            'prompt_template': 'market_size'
        },
        '商业模式': {
            'time': 10,
            'dependencies': ['行业画像', '市场规模'],
            'prompt_template': 'business_model'
        },
        '竞争格局': {
            'time': 10,
            'dependencies': ['行业画像', '市场规模'],
            'prompt_template': 'competition'
        },
        '进入壁垒': {
            'time': 8,
            'dependencies': ['竞争格局'],
            'prompt_template': 'entry_barriers'
        },
        '风险分析': {
            'time': 8,
            'dependencies': ['政策环境', '竞争格局'],
            'prompt_template': 'risk'
        },
        '战略建议': {
            'time': 10,
            'required': True,
            'dependencies': ['行业画像'],
            'prompt_template': 'strategy'
        },

        # 公司对标专用维度
        '核心能力': {
            'time': 10,
            'dependencies': ['行业画像'],
            'prompt_template': 'core_competency'
        },
        '壁垒迁移': {
            'time': 10,
            'dependencies': ['核心能力', '政策环境'],
            'prompt_template': 'barrier_migration'
        },
        '财务测算': {
            'time': 12,
            'dependencies': ['核心能力', '市场规模'],
            'prompt_template': 'financial_modeling'
        },

        # 投资尽调专用维度
        '竞争壁垒': {
            'time': 10,
            'dependencies': ['竞争格局'],
            'prompt_template': 'competitive_moat'
        },
        '估值测算': {
            'time': 12,
            'dependencies': ['商业模式', '市场规模'],
            'prompt_template': 'valuation'
        },

        # 战略指导专用维度
        '路径设计': {
            'time': 10,
            'dependencies': ['市场规模', '竞争格局'],
            'prompt_template': 'strategy_path'
        },
        '资源评估': {
            'time': 8,
            'dependencies': ['路径设计'],
            'prompt_template': 'resource_assessment'
        },

        # 市场进入可行性专用维度
        '单位经济': {
            'time': 10,
            'dependencies': ['市场规模'],
            'prompt_template': 'unit_economics'
        },

        # 合作评估专用维度
        '合作价值': {
            'time': 10,
            'dependencies': ['商业模式'],
            'prompt_template': 'partnership_value'
        },
        '风险识别': {
            'time': 8,
            'dependencies': ['合作价值'],
            'prompt_template': 'risk_identification'
        }
    }

    # ==================== 意图解析关键词 ====================
    INTENT_KEYWORDS = {
        '政策环境': ['政策', '监管', '支持', '补贴', '法规'],
        '市场规模': ['市场', '规模', '多大', '空间', '增长'],
        '商业模式': ['商业模式', '盈利', '模式', '怎么赚钱'],
        '竞争格局': ['竞争', '对手', '激烈', '玩家', 'CR'],
        '进入壁垒': ['壁垒', '门槛', '难度', '护城河'],
        '风险分析': ['风险', '问题', '挑战', '威胁'],
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """初始化研究引擎"""
        # 加载模型配置
        from execution.model_config import ModelConfigManager
        config_manager = ModelConfigManager()
        config = config_manager.load_config(api_key=api_key, base_url=base_url, model=model)

        self.api_key = config.api_key
        self.base_url = config.base_url
        self.model = config.model
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature

        # Phase 3: 反面证据引擎（延迟加载）
        self.counter_evidence_engine = None

        # Phase 3 任务2: 用户自定义模型（延迟加载）
        self.user_model_loader = None

    # ==================== 1. 意图理解 ====================

    def parse_intent(self, user_input: str) -> Dict:
        """
        解析用户意图（自然语言→结构化参数）

        输入: "帮我研究医疗陪护，重点看政策和竞争，快速版"
        输出: {'dimensions': ['政策环境', '竞争格局'], 'depth': '快速'}
        """
        dimensions = []
        depth = '标准'

        # 提取维度
        for dim, keywords in self.INTENT_KEYWORDS.items():
            if any(kw in user_input for kw in keywords):
                dimensions.append(dim)

        # 提取深度
        if any(w in user_input for w in ['快速', '快', '简单', '10分钟']):
            depth = '快速'
        elif any(w in user_input for w in ['深度', '详细', '完整', '60分钟']):
            depth = '深度'

        return {
            'dimensions': dimensions if dimensions else ['政策环境', '市场规模', '商业模式'],
            'depth': depth
        }

    # ==================== 2. 动态工作流 ====================

    def create_workflow(self, dimensions: List[str], research_type: str = "行业分析",
                       interaction_density: str = "guided") -> Dict:
        """
        生成动态工作流（自动解析依赖关系）+ 假设-证据-结论三段式

        Args:
            dimensions: 分析维度列表
            research_type: 研究类型（公司对标/行业分析/投资尽调/战略指导/市场进入可行性/合作评估）
            interaction_density: 交互密度（guided=新手模式，expert=专家模式）

        输入: ['政策环境', '竞争格局'], research_type="行业分析"
        输出: {
            'research_type': '行业分析',
            'interaction_density': 'guided',
            'workflow': [
                {
                    'name': '行业画像',
                    'time': 2,
                    'prompt_template': 'profile',
                    'hypothesis': '该行业处于快速增长期',
                    'evidence_needed': {
                        'required': ['市场规模数据', '年增长率'],
                        'supporting': ['行业生命周期指标'],
                        'counter': ['市场饱和迹象']
                    },
                    'conclusion_format': '必须回答：行业规模、增速、生命周期阶段'
                },
                ...
            ],
            'data_requirements': ['用户需提供的内部数据清单']
        }
        """
        workflow_steps = []
        needed = set(dimensions)

        # 1. 补充必需维度
        for dim, config in self.DIMENSIONS.items():
            if config.get('required'):
                needed.add(dim)

        # 2. 解析依赖关系
        while True:
            added = False
            for dim in list(needed):
                if dim in self.DIMENSIONS:
                    deps = self.DIMENSIONS[dim].get('dependencies', [])
                    for dep in deps:
                        if dep not in needed:
                            needed.add(dep)
                            added = True
            if not added:
                break

        # 3. 拓扑排序（确保依赖顺序）
        sorted_dims = self._topological_sort(needed)

        # 4. 生成workflow（增强版：含假设-证据-结论）
        data_requirements = []

        for dim in sorted_dims:
            if dim in self.DIMENSIONS:
                step = {
                    'name': dim,
                    'time': self.DIMENSIONS[dim]['time'],
                    'prompt_template': self.DIMENSIONS[dim].get('prompt_template')
                }

                # 根据研究类型和维度生成假设-证据-结论
                step_enhancement = self._generate_hypothesis_evidence_conclusion(
                    research_type, dim
                )

                # 识别是否需要内部数据（在update之前收集）
                if step_enhancement.get('needs_internal_data') and step_enhancement.get('internal_data_desc'):
                    data_requirements.append(step_enhancement['internal_data_desc'])

                # 更新step（包含假设-证据-结论字段）
                step.update(step_enhancement)

                workflow_steps.append(step)

        return {
            'research_type': research_type,
            'interaction_density': interaction_density,
            'workflow': workflow_steps,
            'data_requirements': data_requirements if data_requirements else
                ['本研究可完全基于公开数据完成']
        }

    def _generate_hypothesis_evidence_conclusion(self, research_type: str,
                                                dimension: str) -> Dict:
        """
        根据研究类型和维度生成假设-证据-结论三段式

        注意：这是数据生成函数，不是智能判断。智能由Agent根据SKILL.md完成。
        """
        # 默认模板（由Agent根据SKILL.md中的方法论工具箱自定义）
        templates = {
            "行业分析": {
                "行业画像": {
                    "hypothesis": "该行业处于特定生命周期阶段（成长/成熟/衰退）",
                    "evidence_needed": {
                        "required": ["市场规模数据", "年增长率", "主要玩家数量"],
                        "supporting": ["行业集中度CR4", "技术迭代周期"],
                        "counter": ["市场饱和迹象", "增速放缓数据"]
                    },
                    "conclusion_format": "必须回答：行业规模X亿元、年增速Y%、处于Z阶段",
                    "needs_internal_data": False
                },
                "政策环境": {
                    "hypothesis": "政策对行业发展起促进/抑制/中性作用",
                    "evidence_needed": {
                        "required": ["最新政策文件", "补贴/税收优惠细则"],
                        "supporting": ["政策执行案例", "地方落地情况"],
                        "counter": ["政策收紧信号", "补贴退坡时间表"]
                    },
                    "conclusion_format": "必须回答：主要政策、影响方向（促进/抑制）、持续性判断",
                    "needs_internal_data": False
                },
                "市场规模": {
                    "hypothesis": "市场空间足够大且增速可持续",
                    "evidence_needed": {
                        "required": ["TAM数据（自上而下+自下而上）", "历史增长率"],
                        "supporting": ["SAM/SOM测算", "渗透率数据"],
                        "counter": ["市场饱和迹象", "替代品威胁"]
                    },
                    "conclusion_format": "必须回答：TAM/SAM/SOM三层、当前渗透率、未来3年CAGR",
                    "needs_internal_data": False
                },
                "竞争格局": {
                    "hypothesis": "市场集中度处于X水平，竞争强度为Y",
                    "evidence_needed": {
                        "required": ["主要玩家市占率", "CR4/CR8指数"],
                        "supporting": ["Porter五力分析数据", "新进入者数量"],
                        "counter": ["市场整合迹象", "价格战信号"]
                    },
                    "conclusion_format": "必须回答：CR4=X%、竞争强度（激烈/中等/温和）、未来演化方向",
                    "needs_internal_data": False
                }
            },
            "公司对标": {
                "核心能力": {
                    "hypothesis": "标杆公司A的核心竞争力是X，对标公司B可以/不可以复制",
                    "evidence_needed": {
                        "required": ["A公司核心能力拆解（VRIO）", "B公司现有能力盘点"],
                        "supporting": ["A公司历史发展路径", "B公司资源禀赋"],
                        "counter": ["A公司的能力在B公司场景下失效的证据"]
                    },
                    "conclusion_format": "必须回答：A公司核心能力是什么？B公司哪些能复制/哪些不能？",
                    "needs_internal_data": True,
                    "internal_data_desc": "B公司内部：组织架构、技术栈、核心团队背景"
                },
                "壁垒迁移": {
                    "hypothesis": "A公司的壁垒在B公司所在市场X%有效",
                    "evidence_needed": {
                        "required": ["两个市场的PEST对比", "壁垒来源分析"],
                        "supporting": ["可迁移能力清单", "需要重建的能力清单"],
                        "counter": ["壁垒完全失效的证据（如政策/技术环境根本不同）"]
                    },
                    "conclusion_format": "必须回答：哪些壁垒可迁移？哪些失效？需要哪些替代方案？",
                    "needs_internal_data": False
                },
                "财务测算": {
                    "hypothesis": "学标杆的ROI为X%，回收期Y年，财务可行",
                    "evidence_needed": {
                        "required": ["获客成本", "客单价", "留存率", "运营成本结构"],
                        "supporting": ["A公司的单位经济数据", "B公司现有成本数据"],
                        "counter": ["悲观情景下的亏损测算"]
                    },
                    "conclusion_format": "必须回答：三情景（乐观/基准/悲观）NPV、IRR、回收期，最敏感变量是什么",
                    "needs_internal_data": True,
                    "internal_data_desc": "B公司内部：历史财务数据、成本结构、定价策略"
                }
            },
            "投资尽调": {
                "商业模式": {
                    "hypothesis": "标的商业模式可持续，四方价值分配平衡",
                    "evidence_needed": {
                        "required": ["客户/供应商/公司/投资人各方价值量化"],
                        "supporting": ["商业模式演化路径", "关键转换点"],
                        "counter": ["某一方价值为负的证据（如持续烧钱无盈利路径）"]
                    },
                    "conclusion_format": "必须回答：四方各得到什么？模式可持续吗？最大风险点是哪一方可能退出？",
                    "needs_internal_data": True,
                    "internal_data_desc": "标的公司：详细财务模型、客户留存数据、供应商合同条款"
                },
                "竞争壁垒": {
                    "hypothesis": "标的护城河深度为X（宽/中/窄），核心壁垒是Y",
                    "evidence_needed": {
                        "required": ["五大壁垒评分（网络效应/转换成本/成本优势/品牌/监管）"],
                        "supporting": ["用户留存曲线", "NPS数据", "成本结构对比"],
                        "counter": ["竞争对手的破局路径分析"]
                    },
                    "conclusion_format": "必须回答：总分多少？核心壁垒是什么？最容易被攻破的是什么？",
                    "needs_internal_data": True,
                    "internal_data_desc": "标的公司：用户留存数据、成本结构、专利清单"
                },
                "估值测算": {
                    "hypothesis": "合理估值区间为X-Y亿，当前估值合理/高估/低估",
                    "evidence_needed": {
                        "required": ["未来5年现金流预测", "WACC参数", "可比公司倍数"],
                        "supporting": ["DCF敏感性分析", "可比公司选择逻辑"],
                        "counter": ["悲观情景下的估值下限"]
                    },
                    "conclusion_format": "必须回答：DCF估值、可比公司法估值、两种方法的差异reconcile、最终建议区间",
                    "needs_internal_data": True,
                    "internal_data_desc": "标的公司：历史财务数据、未来业务计划、股权结构"
                }
            },
            "战略指导": {
                "路径设计": {
                    "hypothesis": "推荐战略方向X，备选Y，理由是吸引力+可行性双高",
                    "evidence_needed": {
                        "required": ["至少3个战略选项", "吸引力×可行性矩阵评分"],
                        "supporting": ["各选项的资源需求", "时间窗口分析"],
                        "counter": ["推荐选项的最大风险"]
                    },
                    "conclusion_format": "必须回答：推荐哪个？为什么？备选是什么？执行优先级？",
                    "needs_internal_data": True,
                    "internal_data_desc": "公司内部：战略目标、资源预算、管理层偏好"
                },
                "资源评估": {
                    "hypothesis": "关键资源缺口是X，获取方式Y，成本Z",
                    "evidence_needed": {
                        "required": ["需要的资源清单", "现有资源盘点"],
                        "supporting": ["缺口获取方案（自建/合作/收购）", "成本与时间估算"],
                        "counter": ["资源无法获取的情况下的替代方案"]
                    },
                    "conclusion_format": "必须回答：关键缺口是什么？如何获取？成本多少？时间多久？",
                    "needs_internal_data": True,
                    "internal_data_desc": "公司内部：人力/资金/技术/渠道现状盘点"
                }
            },
            "市场进入可行性": {
                "进入壁垒": {
                    "hypothesis": "进入壁垒总分X（低/中/高），最难跨越的是Y",
                    "evidence_needed": {
                        "required": ["五维壁垒评分（政策/资金/技术/渠道/品牌）"],
                        "supporting": ["各维度跨越方案", "时间窗口分析"],
                        "counter": ["壁垒降低的可能性（政策开放/技术突破）"]
                    },
                    "conclusion_format": "必须回答：总分多少？最难跨越的是什么？建议破局路径？",
                    "needs_internal_data": False
                },
                "单位经济": {
                    "hypothesis": "LTV/CAC比率X，单位经济可行/不可行",
                    "evidence_needed": {
                        "required": ["CAC", "LTV", "留存曲线", "毛利率"],
                        "supporting": ["回收期测算", "三情景敏感性分析"],
                        "counter": ["关键变量恶化情景（如留存率低于预期）"]
                    },
                    "conclusion_format": "必须回答：LTV/CAC比率？回收期？关键风险变量是什么？",
                    "needs_internal_data": True,
                    "internal_data_desc": "公司内部：现有获客成本、运营成本结构"
                }
            },
            "合作评估": {
                "合作价值": {
                    "hypothesis": "合作带来增量价值X亿，主要来自Y协同",
                    "evidence_needed": {
                        "required": ["资源互补清单", "协同效应量化（收入/成本/能力）"],
                        "supporting": ["类似合作案例", "协同实现路径"],
                        "counter": ["协同无法实现的风险（如文化冲突）"]
                    },
                    "conclusion_format": "必须回答：增量价值多少？主要来自哪种协同？实现概率多大？",
                    "needs_internal_data": True,
                    "internal_data_desc": "双方公司：详细业务数据、客户重叠分析、成本结构"
                },
                "风险识别": {
                    "hypothesis": "最大风险点是X，建议对冲方案Y",
                    "evidence_needed": {
                        "required": ["利益冲突点清单", "各冲突点严重性评估"],
                        "supporting": ["对冲方案设计（对赌/清算权/一票否决）"],
                        "counter": ["风险可接受的情况"]
                    },
                    "conclusion_format": "必须回答：最大风险点是什么？建议哪些对冲条款？",
                    "needs_internal_data": True,
                    "internal_data_desc": "双方公司：股权结构、治理架构、历史合作案例"
                }
            }
        }

        # 返回对应模板，如果没有则返回通用模板
        if research_type in templates and dimension in templates[research_type]:
            return templates[research_type][dimension]
        else:
            # 通用模板
            return {
                "hypothesis": f"关于{dimension}的初始假设（由Agent根据SKILL.md生成）",
                "evidence_needed": {
                    "required": ["关键证据1", "关键证据2"],
                    "supporting": ["支撑证据"],
                    "counter": ["反驳证据"]
                },
                "conclusion_format": f"必须回答：{dimension}的核心问题",
                "needs_internal_data": False
            }

    def _topological_sort(self, dimensions: set) -> List[str]:
        """拓扑排序（确保依赖关系正确）"""
        from collections import deque, defaultdict

        # 构建邻接表和入度
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        for dim in dimensions:
            if dim not in in_degree:
                in_degree[dim] = 0
            if dim in self.DIMENSIONS:
                for dep in self.DIMENSIONS[dim].get('dependencies', []):
                    if dep in dimensions:
                        graph[dep].append(dim)
                        in_degree[dim] += 1

        # Kahn算法
        queue = deque([dim for dim in dimensions if in_degree[dim] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    # ==================== 3. 咨询级分析（Prompt工程）====================

    def analyze(self, industry: str, dimension: str, context: Dict = None) -> Dict:
        """
        执行单个维度的分析

        Args:
            industry: 行业名称
            dimension: 分析维度
            context: 上下文信息（前序分析结果）

        Returns:
            {'content': '分析内容', 'quality_score': 0.85}
        """
        if dimension not in self.DIMENSIONS:
            raise ValueError(f"未知维度: {dimension}")

        template_name = self.DIMENSIONS[dimension].get('prompt_template')
        if not template_name:
            return {'content': f'{dimension}分析模板缺失', 'quality_score': 0.0}

        # 根据模板生成prompt
        prompt = self._get_prompt(template_name, industry, context or {})

        # 调用Claude API
        try:
            content = self._call_claude(prompt)
            quality_score = self._assess_quality(content)

            return {
                'content': content,
                'quality_score': quality_score,
                'dimension': dimension
            }
        except Exception as e:
            print(f"[WARN]  分析失败: {dimension} - {e}")
            return {
                'content': f'{dimension}分析失败，请重试',
                'quality_score': 0.0,
                'error': str(e)
            }

    def _get_prompt(self, template_name: str, industry: str, context: Dict) -> str:
        """获取Prompt模板（核心：用Prompt替代脚本）"""

        # 行业画像模板
        if template_name == 'profile':
            return f"""你是波士顿咨询（BCG）的行业专家。请用3句话精准描述【{industry}】行业的核心特征。

要求：
1. 第一句：行业定位（政府主导/市场主导、高监管/低监管）
2. 第二句：核心痛点或机会（用数据支撑）
3. 第三句：竞争格局（集中度、头部玩家）

每句话必须包含具体数字或案例，不超过50字。

示例（医疗陪护）：
"政府主导+高监管行业，长护险试点49城覆盖1.45亿人。核心机会在于4500万失能老人的刚需市场，但面临65%人力成本占比的盈利压力。市场高度分散，CR5<10%，无绝对龙头。"
"""

        # 政策环境模板
        elif template_name == 'policy':
            return f"""你是BCG/麦肯锡的资深行业分析师，正在为客户撰写【{industry}】行业的政策环境分析章节。

# 分析框架（PEST-P深度拆解）

## 第一步：识别核心政策驱动因素
1. 哪些政策对行业影响最大？（列出Top 3）
2. 政策演进的时间线是什么？
3. 政策背后的政府意图是什么？

## 第二步：量化政策影响
1. 政策带来的市场规模变化（用数字）
2. 政策导致的成本结构变化（百分比）
3. 政策创造的新商业机会（具体场景）

## 第三步：预测政策趋势
1. 未来2-3年可能的政策变化
2. 对企业的影响（机会/威胁）
3. 应对策略

# 输出要求
- 使用具体数字和时间节点
- 引用具体政策文件名称
- 给出可执行的建议
- 长度：300-400字

请直接输出分析内容，不要输出"分析如下"等前缀。
"""

        # 市场规模模板
        elif template_name == 'market_size':
            return f"""你是贝恩咨询的市场规模测算专家，正在为【{industry}】行业进行市场规模分析。

# 测算框架（Top-down + Bottom-up双验证）

## Top-down测算
1. 目标用户群体规模（具体数字）
2. 渗透率假设（基于类似行业）
3. 客单价水平（价格区间）
4. 市场规模 = 用户数 × 渗透率 × 客单价

## Bottom-up验证
1. 典型企业营收（列举2-3家）
2. 市场份额估算
3. 推导总市场规模

## 增长驱动因素
1. 需求端驱动（人口、政策、消费升级）
2. 供给端驱动（技术、效率提升）
3. 2020-2030年CAGR预测（%）

# 输出要求
- 必须包含具体数字和计算逻辑
- 引用公开数据来源
- 给出保守/中性/乐观三种情景
- 长度：300-400字

直接输出分析内容。
"""

        # 商业模式模板
        elif template_name == 'business_model':
            return f"""你是麦肯锡的商业模式专家，正在为【{industry}】行业进行商业模式深度拆解。

# 分析框架

## 四方决策链拆解
1. 需求方是谁？关注什么？（具体描述）
2. 支付方是谁？支付意愿如何？（百分比+金额）
3. 决策方是谁？决策权重多大？（%）
4. 使用方（服务接收者）体验如何？

## 单位经济模型
收入端：
- 客单价：XX元/单
- 复购率：XX%
- LTV（客户终身价值）：XX元

成本端：
- 获客成本（CAC）：XX元
- 人力成本：XX%
- 平台成本：XX%
- 毛利率：XX%

盈利性：
- LTV/CAC比值（健康值>3）
- 盈亏平衡点：XX单/月
- 回本周期：XX个月

## 典型模式对比
列举2-3种主流商业模式，对比优劣势

# 输出要求
- 必须包含具体数字（不能写"较高"、"较低"）
- 给出盈利性判断和改进建议
- 长度：400-500字

直接输出分析内容。
"""

        # 竞争格局模板
        elif template_name == 'competition':
            return f"""你是波士顿咨询（BCG）的竞争战略专家，正在分析【{industry}】行业的竞争格局。

# 分析框架（Porter五力模型）

## 1. 行业内竞争强度
- 市场集中度（CR4、HHI指数）
- 头部玩家（列举Top 3-5，含市占率）
- 主要竞争维度（价格/服务/技术/品牌）
- 差异化程度（高/中/低）

## 2. 供应商议价能力
- 供应商集中度
- 转换成本
- 上游对行业利润的影响

## 3. 购买者议价能力
- 客户集中度
- 价格敏感度
- 转换成本

## 4. 新进入者威胁
- 进入壁垒高度（资金/技术/牌照/网络效应）
- 新进入频率
- 潜在竞争者

## 5. 替代品威胁
- 替代品类型
- 替代风险程度

# 输出要求
- 必须包含具体数字（市占率、CR4等）
- 给出竞争强度评级（低/中/高）
- 识别竞争机会窗口
- 长度：400-500字

直接输出分析内容。
"""

        # 进入壁垒模板
        elif template_name == 'entry_barriers':
            return f"""你是麦肯锡的战略咨询师，正在评估【{industry}】行业的进入壁垒。

# 分析框架（五大壁垒类型）

## 1. 资金壁垒
- 初始投入规模（万元/百万元/亿元级别）
- 资金回报周期
- 现金流特征

## 2. 技术壁垒
- 核心技术难度
- 研发周期
- 专利保护

## 3. 政策壁垒
- 牌照/资质要求
- 审批周期
- 政策风险

## 4. 渠道壁垒
- 渠道建设时间
- 渠道独占性
- 转换成本

## 5. 品牌壁垒
- 品牌建设周期
- 用户忠诚度
- 口碑传播

# 综合评估
- 总体壁垒高度：高/中/低
- 新进入者的突破路径
- 现有玩家的防御策略

# 输出要求
- 量化各项壁垒（时间/金额）
- 给出新进入者建议
- 长度：300-400字

直接输出分析内容。
"""

        # 风险分析模板
        elif template_name == 'risk':
            return f"""你是贝恩咨询的风险管理专家，正在为【{industry}】行业进行风险分析。

# 分析框架（PESTEL风险）

## 1. 政策风险（Political）
- 政策变化可能性（高/中/低）
- 影响程度
- 应对措施

## 2. 经济风险（Economic）
- 宏观经济周期影响
- 支付能力波动
- 应对措施

## 3. 社会风险（Social）
- 需求变化趋势
- 舆论风险
- 应对措施

## 4. 技术风险（Technology）
- 技术替代风险
- 创新失败风险
- 应对措施

## 5. 法律风险（Legal）
- 合规风险
- 诉讼风险
- 应对措施

## 6. 环境风险（Environmental）
- ESG要求
- 环保压力
- 应对措施

# 风险矩阵
列出Top 3风险（按概率×影响排序）

# 输出要求
- 量化风险（概率%、影响规模）
- 给出可执行的应对措施
- 长度：300-400字

直接输出分析内容。
"""

        # 战略建议模板
        elif template_name == 'strategy':
            context_summary = json.dumps(context, ensure_ascii=False, indent=2)[:1000]
            return f"""你是贝恩咨询的战略合伙人，基于前期分析，为客户提供【{industry}】行业的市场进入战略建议。

# 前期分析摘要
{context_summary}

# 战略建议框架

## 1. 目标市场选择
- 优先进入哪些城市/细分市场？（具体城市名）
- 为什么？（数据支撑）

## 2. 差异化定位
- 与竞争对手的差异点在哪里？
- 如何建立竞争壁垒？

## 3. 资源配置建议
- 需要投入多少资金？（金额区间）
- 团队配置（关键岗位+人数）
- 时间规划（分阶段里程碑）

## 4. 风险规避
- 3个最大风险是什么？
- 如何应对？（具体措施）

# 输出要求
- 建议必须可执行（有明确的数字、时间、责任人）
- 长度：300-400字

直接输出建议内容。
"""

        else:
            return f"请分析{industry}行业的{template_name}。"

    def _call_claude(self, prompt: str) -> str:
        """调用Claude API（带重试）"""
        if not self.api_key:
            raise ValueError("未设置ANTHROPIC_API_KEY")

        import anthropic

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        client = anthropic.Anthropic(**client_kwargs)

        # 自动重试（最多3次）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                message = client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )

                # 提取文本内容（跳过ThinkingBlock）
                for block in message.content:
                    if hasattr(block, 'text'):
                        return block.text.strip()

                return ""

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"   [WARN]  API调用失败，正在重试 ({attempt + 1}/{max_retries})...")
                    import time
                    time.sleep(2 ** attempt)
                else:
                    raise

        return ""

    def _assess_quality(self, content: str) -> float:
        """
        评估内容质量

        标准：
        - 包含数字 +0.3
        - 长度充足 +0.3
        - 有明确建议 +0.2
        - 结构清晰 +0.2
        """
        score = 0.0

        # 1. 是否包含数字
        import re
        if re.search(r'\d+', content):
            score += 0.3

        # 2. 长度是否充足（>200字）
        if len(content) > 200:
            score += 0.3

        # 3. 是否包含建议关键词
        if any(word in content for word in ['建议', '应该', '可以', '推荐', '优先']):
            score += 0.2

        # 4. 结构是否清晰（包含标点符号）
        if content.count('。') >= 3 or content.count('\n') >= 2:
            score += 0.2

        return min(score, 1.0)

    # ==================== 4. 质量检查 ====================

    def check_quality(self, results: List[Dict]) -> Dict:
        """
        质量检查

        返回: {
            'passed': True/False,
            'issues': [],
            'suggestions': []
        }
        """
        issues = []
        suggestions = []

        # 1. 检查所有分析的质量分数
        low_quality = [r for r in results if r.get('quality_score', 0) < 0.6]
        if low_quality:
            issues.append(f"有{len(low_quality)}个分析质量偏低")
            suggestions.append("建议重新生成低质量分析")

        # 2. 检查必需维度是否完整
        dimensions = [r.get('dimension') for r in results]
        if '行业画像' not in dimensions:
            issues.append("缺少行业画像")
        if '战略建议' not in dimensions:
            issues.append("缺少战略建议")

        # 3. 综合判断
        passed = len(issues) == 0 and len(low_quality) <= 1

        return {
            'passed': passed,
            'issues': issues,
            'suggestions': suggestions,
            'avg_quality': sum(r.get('quality_score', 0) for r in results) / max(len(results), 1)
        }

    # ==================== 5. Phase 3: 反面证据搜索 ====================

    def find_counter_evidence(self, chapter_content: str, chapter_title: str) -> List[Dict]:
        """
        搜索反面证据（Phase 3新增）

        Args:
            chapter_content: 章节内容
            chapter_title: 章节标题

        Returns:
            [
                {
                    'source': 'https://...',
                    'title': '...',
                    'snippet': '...',
                    'query': '...'
                },
                ...
            ]
        """
        # 延迟加载反面证据引擎
        if self.counter_evidence_engine is None:
            try:
                from core.counter_evidence_engine import CounterEvidenceEngine
                self.counter_evidence_engine = CounterEvidenceEngine()
                print("[Phase 3] ✅ 反面证据引擎已加载")
            except ImportError as e:
                print(f"[Phase 3] ⚠️ 反面证据引擎加载失败: {e}")
                return []

        try:
            return self.counter_evidence_engine.find_counter_evidence(
                chapter_content,
                chapter_title
            )
        except Exception as e:
            print(f"[Phase 3] ⚠️ 反面证据搜索失败: {e}")
            return []

    # ==================== 6. Phase 3 任务2: 用户自定义模型 ====================

    def get_user_models(self) -> Dict:
        """
        获取用户自定义模型（延迟加载）

        Returns:
            {model_name: model_config}
        """
        if self.user_model_loader is None:
            try:
                from core.user_model_loader import UserModelLoader
                self.user_model_loader = UserModelLoader()
                print(f"[Phase 3] ✅ 用户模型库已加载: {len(self.user_model_loader.models)}个自定义模型")
            except ImportError as e:
                print(f"[Phase 3] ⚠️ 用户模型库加载失败: {e}")
                return {}
            except Exception as e:
                print(f"[Phase 3] ⚠️ 用户模型库初始化失败: {e}")
                return {}

        return self.user_model_loader.models

    def get_user_model(self, name: str) -> Optional[Dict]:
        """
        获取指定的用户自定义模型

        Args:
            name: 模型名称

        Returns:
            模型配置字典，不存在则返回None
        """
        models = self.get_user_models()
        return models.get(name)
