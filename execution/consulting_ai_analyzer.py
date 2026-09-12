"""
咨询级AI分析引擎：生成咨询公司水准的行业洞察

核心理念：
1. 多轮深度推理，而非一次性生成
2. 结构化思考：问题分解 → 数据收集 → 逻辑推理 → 结论验证
3. 具体化：数字、案例、对比
4. 可执行：战略建议必须可落地
"""

import os
from typing import Dict, List, Optional
import json
from pathlib import Path
from execution.model_config import ModelConfigManager


class ConsultingAIAnalyzer:
    """
    咨询级AI分析引擎

    生成真正有深度、有数据支撑的行业研究洞察
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: Optional[str] = None):
        """
        初始化咨询级AI分析引擎

        Args:
            api_key: Anthropic API密钥（可选）
            base_url: API Base URL（可选，用于中转站）
            model: 模型ID（可选）
        """
        # 使用模型配置管理器加载配置
        config_manager = ModelConfigManager()
        config = config_manager.load_config(
            api_key=api_key,
            base_url=base_url,
            model=model
        )

        self.api_key = config.api_key
        self.base_url = config.base_url
        self.model = config.model
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature

    def deep_industry_analysis(self,
                               industry: str,
                               focus_areas: List[str],
                               context: Dict) -> Dict:
        """
        深度行业分析（多轮推理）

        Args:
            industry: 行业名称
            focus_areas: 关注领域列表
            context: 上下文信息

        Returns:
            analysis: 结构化的深度分析结果
        """
        results = {}

        # 第一轮：行业定位与特征识别
        industry_profile = self._analyze_industry_profile(industry)
        results['profile'] = industry_profile

        # 第二轮：针对每个关注领域进行深度分析
        for area in focus_areas:
            if area == '政策环境':
                results['policy'] = self._analyze_policy_environment(industry, context)
            elif area == '市场规模':
                results['market_size'] = self._analyze_market_size(industry, context)
            elif area == '商业模式':
                results['business_model'] = self._analyze_business_model(industry, context)
            elif area == '竞争格局':
                results['competition'] = self._analyze_competition(industry, context)
            elif area == '进入壁垒':
                results['entry_barriers'] = self._analyze_entry_barriers(industry, context)

        # 第三轮：综合战略建议
        results['strategic_recommendations'] = self._generate_strategic_recommendations(
            industry, results
        )

        return results

    def _analyze_policy_environment(self, industry: str, context: Dict) -> Dict:
        """分析政策环境（咨询公司标准）"""

        prompt = f"""你是BCG/麦肯锡的资深行业分析师，正在为客户撰写【{industry}】行业的政策环境分析章节。

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

示例参考格式（针对医疗陪护行业）：
"长护险试点是医疗陪护行业的核心政策红利。截至2023年，49个试点城市覆盖1.45亿参保人，年赔付额约300亿元。但试点呈现'碎片化'特征：上海按月支付600元，青岛达1200元，待遇差异显著。政府意图明确：应对老龄化压力，将护理需求从医保转向长护险。

未来趋势：2025年前后出台全国统一标准，覆盖人群扩至3亿+。市场机会：1）抢占二线城市试点先发优势；2）参与标准制定获取政策红利；3）布局'长护险+商业保险'组合支付。风险：地方财政压力可能导致报销额度低于预期。

建议：选择长护险试点力度大且财政实力强的城市（如苏州、杭州）作为进入市场，提前3-6个月布局以获取定点资质。"
"""

        try:
            conclusion = self._call_claude_api(prompt)
            return {
                'content': conclusion,
                'type': 'policy_environment',
                'quality_score': self._assess_quality(conclusion)
            }
        except Exception as e:
            # 打印详细错误信息用于调试
            print(f"\n⚠️ API调用失败: {type(e).__name__}: {str(e)}")
            # Fallback到高质量模板
            return self._policy_fallback(industry)

    def _analyze_market_size(self, industry: str, context: Dict) -> Dict:
        """分析市场规模（含测算逻辑）"""

        prompt = f"""你是贝恩咨询的市场规模测算专家，正在为【{industry}】行业进行市场规模分析。

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

示例参考格式（针对医疗陪护行业）：
"医疗陪护市场规模测算（2023年）：

Top-down：中国60岁以上老年人2.8亿，失能/半失能约4500万人。其中需要长期陪护约2000万人，渗透率10%（参考日本15%），客单价300元/天×30天=9000元/月。市场规模=2000万×10%×9000×12月=2160亿元/年。

Bottom-up验证：头部企业（小鸟慧医）年营收约8亿元，市占率估算0.5%，推导市场规模=1600亿元，与top-down接近。

增长驱动：1）老龄化加速（每年新增失能老人200万）；2）长护险扩面提升支付能力；3）专业化服务替代家庭护理。2023-2030年CAGR预测：保守15%、中性20%、乐观25%。2030年市场规模有望达5000-8000亿元。"
"""

        try:
            conclusion = self._call_claude_api(prompt)
            return {
                'content': conclusion,
                'type': 'market_size',
                'quality_score': self._assess_quality(conclusion)
            }
        except Exception as e:
            print(f"\n⚠️ API调用失败(市场规模): {type(e).__name__}: {str(e)}")
            return self._market_size_fallback(industry)

    def _analyze_business_model(self, industry: str, context: Dict) -> Dict:
        """分析商业模式（四方决策链+单位经济）"""

        prompt = f"""你是麦肯锡的商业模式专家，正在为【{industry}】行业进行商业模式深度拆解。

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

示例参考格式（针对医疗陪护行业）：
"医疗陪护商业模式呈现'四方分离'特征：需求方（失能老人）需要专业护理，支付方（子女40%、长护险30%、自费30%）关注性价比，决策方（子女70%、医生建议20%）权重最大，使用方（老人）体验决定续费。

单位经济（以居家陪护为例）：客单价300元/天，月均消费9000元，年复购率60%，LTV约6.5万元。获客成本1200元（医生推荐+线上投放），人力成本占比65%（护理员工资200元/天），平台抽佣15%，毛利率20%。LTV/CAC=54倍，健康。但单月需30单才能覆盖运营成本，回本周期18个月，现金流压力大。

三种模式对比：1）平台撮合模式：轻资产，毛利低（10-15%），依赖规模效应；2）自营模式：重资产，毛利高（25-30%），但扩张慢；3）混合模式：核心城市自营+其他城市加盟，平衡规模与利润。建议采用混合模式，优先布局长护险覆盖城市以降低CAC。"
"""

        try:
            conclusion = self._call_claude_api(prompt)
            return {
                'content': conclusion,
                'type': 'business_model',
                'quality_score': self._assess_quality(conclusion)
            }
        except Exception as e:
            print(f"\n⚠️ API调用失败(商业模式): {type(e).__name__}: {str(e)}")
            return self._business_model_fallback(industry)

    def _analyze_industry_profile(self, industry: str) -> Dict:
        """行业画像（3个关键特征）"""
        prompt = f"""你是波士顿咨询（BCG）的行业专家。请用3句话精准描述【{industry}】行业的核心特征。

要求：
1. 第一句：行业定位（政府主导/市场主导、高监管/低监管）
2. 第二句：核心痛点或机会（用数据支撑）
3. 第三句：竞争格局（集中度、头部玩家）

每句话必须包含具体数字或案例，不超过50字。

示例（医疗陪护）：
"政府主导+高监管行业，长护险试点49城覆盖1.45亿人。核心机会在于4500万失能老人的刚需市场，但面临65%人力成本占比的盈利压力。市场高度分散，CR5<10%，无绝对龙头。"
"""

        try:
            conclusion = self._call_claude_api(prompt)
            return {
                'summary': conclusion,
                'type': 'industry_profile'
            }
        except:
            return {
                'summary': f'{industry}行业呈现独特的发展特征，市场空间巨大但竞争激烈，需要精准定位和差异化策略。',
                'type': 'industry_profile'
            }

    def _generate_strategic_recommendations(self, industry: str, analysis_results: Dict) -> Dict:
        """生成战略建议（可执行）"""

        # 整合之前的分析结果
        context_summary = json.dumps(analysis_results, ensure_ascii=False, indent=2)[:1000]

        prompt = f"""你是贝恩咨询的战略合伙人，基于前期分析，为客户提供【{industry}】行业的市场进入战略建议。

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

示例参考格式：
"医疗陪护市场进入战略：

目标市场：优先进入长三角+珠三角长护险试点城市（苏州、杭州、广州），理由：1）政策落地快，报销额度高（苏州1500元/月）；2）支付能力强，商业保险渗透率高；3）护理人才供给充足。避开北京、上海等头部竞争激烈市场。

差异化定位：聚焦'术后康复陪护'细分场景，客单价高（500元/天 vs 市场均价300元），医生推荐转化率高。建立壁垒：与三甲医院合作获取独家患者资源，培训体系打造专业护理员壁垒。

资源配置：首轮投入300-500万元（3城试点），团队15人（城市经理3人+运营5人+护理员7人），6个月达盈亏平衡，18个月回本。

风险应对：1）政策风险-签约多元支付方分散依赖；2）人力成本上涨-建立护理员培训学校降低招聘成本；3）医疗事故-购买责任险+SOP严格执行。"
"""

        try:
            conclusion = self._call_claude_api(prompt)
            return {
                'content': conclusion,
                'type': 'strategic_recommendations',
                'quality_score': self._assess_quality(conclusion)
            }
        except:
            return self._strategic_recommendations_fallback(industry)

    def _call_claude_api(self, prompt: str) -> str:
        """调用Claude API"""
        if not self.api_key:
            raise ValueError("未设置ANTHROPIC_API_KEY")

        try:
            import anthropic

            # 构建client参数
            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url

            client = anthropic.Anthropic(**client_kwargs)

            # P1.2: 自动重试机制（最多3次）
            max_retries = 3
            last_error = None

            for attempt in range(max_retries):
                try:
                    message = client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[{"role": "user", "content": prompt}]
                    )

                    # 处理响应：找到TextBlock（跳过ThinkingBlock）
                    for block in message.content:
                        if hasattr(block, 'text'):
                            return block.text.strip()

                    # 如果没有找到文本块，返回空字符串
                    return ""

                except Exception as api_error:
                    last_error = api_error
                    if attempt < max_retries - 1:
                        print(f"   ⚠️  API调用失败，正在重试 ({attempt + 1}/{max_retries})...")
                        import time
                        time.sleep(2 ** attempt)  # 指数退避：2秒、4秒
                    else:
                        # 最后一次重试也失败，抛出错误
                        raise

            # 如果所有重试都失败，抛出最后一个错误
            if last_error:
                raise last_error

            return ""

        except ImportError:
            raise ImportError("需要安装anthropic包: pip install anthropic")
        except Exception as e:
            # 打印具体错误信息，方便调试
            print(f"API调用错误: {str(e)}")
            raise

    def _assess_quality(self, content: str) -> float:
        """
        评估内容质量

        Returns:
            quality_score: 0-1之间的质量分数
        """
        score = 0.0

        # 检查是否包含数字
        import re
        if re.search(r'\d+', content):
            score += 0.3

        # 检查长度（300字以上认为比较完整）
        if len(content) >= 300:
            score += 0.3

        # 检查是否包含具体建议
        if '建议' in content or '推荐' in content or '应' in content:
            score += 0.2

        # 检查是否有结构
        if '：' in content or '、' in content:
            score += 0.2

        return min(score, 1.0)

    # Fallback方法（当API不可用时）
    def _policy_fallback(self, industry: str) -> Dict:
        return {
            'content': f'{industry}行业政策环境分析（待完善：需要API密钥生成深度分析）',
            'type': 'policy_environment',
            'quality_score': 0.3
        }

    def _market_size_fallback(self, industry: str) -> Dict:
        return {
            'content': f'{industry}行业市场规模分析（待完善：需要API密钥生成深度分析）',
            'type': 'market_size',
            'quality_score': 0.3
        }

    def _business_model_fallback(self, industry: str) -> Dict:
        return {
            'content': f'{industry}行业商业模式分析（待完善：需要API密钥生成深度分析）',
            'type': 'business_model',
            'quality_score': 0.3
        }

    def _strategic_recommendations_fallback(self, industry: str) -> Dict:
        return {
            'content': f'{industry}行业战略建议（待完善：需要API密钥生成深度分析）',
            'type': 'strategic_recommendations',
            'quality_score': 0.3
        }


def main():
    """测试咨询级AI分析引擎"""
    print("="*60)
    print("测试: 咨询级AI分析引擎")
    print("="*60)

    analyzer = ConsultingAIAnalyzer()

    # 测试行业画像
    print("\n测试: 行业画像")
    profile = analyzer._analyze_industry_profile('医疗陪护')
    print(f"\n{profile['summary']}")

    # 测试政策环境分析
    print("\n测试: 政策环境分析")
    policy = analyzer._analyze_policy_environment('医疗陪护', {})
    print(f"\n{policy['content'][:200]}...")
    print(f"质量分数: {policy['quality_score']:.2f}")


if __name__ == '__main__':
    main()
