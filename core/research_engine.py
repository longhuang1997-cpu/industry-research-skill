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

    def create_workflow(self, dimensions: List[str]) -> List[Dict]:
        """
        生成动态工作流（自动解析依赖关系）

        输入: ['政策环境', '竞争格局']
        输出: [
            {'name': '行业画像', 'time': 2},  # 自动补充必需维度
            {'name': '市场规模', 'time': 8},  # 竞争格局依赖市场规模
            {'name': '政策环境', 'time': 8},
            {'name': '竞争格局', 'time': 10},
            {'name': '战略建议', 'time': 10}  # 自动补充必需维度
        ]
        """
        workflow = []
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

        # 4. 生成workflow
        for dim in sorted_dims:
            if dim in self.DIMENSIONS:
                workflow.append({
                    'name': dim,
                    'time': self.DIMENSIONS[dim]['time'],
                    'prompt_template': self.DIMENSIONS[dim].get('prompt_template')
                })

        return workflow

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
