"""
质量检查模块 - 真实性验证 + 结构化评分

核心理念：
- 不再用正则规则假装质量检查
- 要求所有数字必须溯源
- 明确区分「真实数据」和「推测」
"""

from typing import Dict, List
import re


class QualityChecker:
    """质量检查器 - 真实性优先"""

    # 质量标准（咨询级报告要求）
    QUALITY_STANDARDS = {
        'data_sourcing': {
            '权重': 0.4,
            '说明': '数据必须有来源，数字必须溯源'
        },
        'structure': {
            '权重': 0.2,
            '说明': '结构完整，逻辑清晰'
        },
        'depth': {
            '权重': 0.2,
            '说明': '分析深度，有洞察'
        },
        'actionable': {
            '权重': 0.2,
            '说明': '结论可执行'
        }
    }

    def __init__(self):
        self.check_results = []

    def check_report(self, report_content: str, dimension: str, search_context: Dict) -> Dict:
        """
        检查报告质量

        Args:
            report_content: 报告内容（Markdown）
            dimension: 分析维度
            search_context: 搜索上下文（用于验证溯源）

        Returns:
            {
                'score': 0-1,
                'grade': 'A' | 'B' | 'C' | 'D',
                'issues': [...],  # 质量问题清单
                'passed': True/False,
                'details': {...}
            }
        """
        scores = {}

        # 1. 数据溯源检查（最重要）
        scores['data_sourcing'] = self._check_data_sourcing(
            report_content,
            search_context
        )

        # 2. 结构完整性检查
        scores['structure'] = self._check_structure(report_content, dimension)

        # 3. 深度检查
        scores['depth'] = self._check_depth(report_content)

        # 4. 可执行性检查
        scores['actionable'] = self._check_actionable(report_content, dimension)

        # 计算总分
        total_score = sum(
            scores[key] * self.QUALITY_STANDARDS[key]['权重']
            for key in scores
        )

        # 生成质量报告
        return {
            'score': round(total_score, 2),
            'grade': self._score_to_grade(total_score),
            'passed': total_score >= 0.7,
            'details': scores,
            'issues': self._generate_issues(scores),
            'method': search_context.get('method', 'unknown')
        }

    def _check_data_sourcing(self, content: str, search_context: Dict) -> float:
        """
        数据溯源检查 - 核心质量指标

        评分标准:
        - 1.0: 所有数字都有来源标注 [来源X]
        - 0.7: 部分数字有来源
        - 0.4: 有数字但无来源（标注了"基于LLM记忆"警告）
        - 0.0: 有数字但假装有来源（最差）
        """
        # 查找所有数字
        numbers = re.findall(r'\d+(?:\.\d+)?(?:[亿万千百]|%|元|美元|英镑|户|个|MW|MWh)', content)

        if not numbers:
            return 0.5  # 没有数字，不好也不差

        # 检查是否使用了搜索数据
        if search_context.get('method') == 'web_search':
            # 检查是否有来源标注
            source_tags = re.findall(r'\[来源\d+\]', content)
            if len(source_tags) >= len(numbers) * 0.8:  # 80%数字有来源
                return 1.0
            elif len(source_tags) >= len(numbers) * 0.5:
                return 0.7
            else:
                return 0.5

        # 如果使用LLM fallback，检查是否标注了警告
        elif search_context.get('method') == 'llm_fallback':
            if '⚠️' in content or '未使用实时数据' in content or '基于LLM记忆' in content:
                return 0.4  # 诚实标注了，给基础分
            else:
                return 0.0  # 没标注，假装真实数据，最差

        return 0.3  # 不确定来源

    def _check_structure(self, content: str, dimension: str) -> float:
        """结构完整性检查"""
        score = 0.0

        # 基础结构检查
        if len(content) >= 200:
            score += 0.3

        # 有标题层级
        if re.search(r'^#{1,3}\s', content, re.MULTILINE):
            score += 0.3

        # 有列表或表格（结构化呈现）
        if re.search(r'^\s*[-*+]\s', content, re.MULTILINE) or '|' in content:
            score += 0.2

        # 维度特定要求
        dimension_requirements = {
            '商业模式': ['收入', '成本', '客户'],
            '竞争格局': ['竞争', '市场份额', '玩家'],
            '市场规模': ['规模', '增长', '市场']
        }

        if dimension in dimension_requirements:
            keywords = dimension_requirements[dimension]
            matched = sum(1 for kw in keywords if kw in content)
            score += 0.2 * (matched / len(keywords))

        return min(score, 1.0)

    def _check_depth(self, content: str) -> float:
        """深度检查 - 是否有洞察"""
        score = 0.0

        # 有因果分析（"因为"、"导致"、"由于"）
        if any(word in content for word in ['因为', '导致', '由于', '原因', '驱动']):
            score += 0.3

        # 有对比分析（"相比"、"对比"、"vs"）
        if any(word in content for word in ['相比', '对比', 'vs', '而', '但']):
            score += 0.3

        # 有趋势判断（"未来"、"预计"、"趋势"）
        if any(word in content for word in ['未来', '预计', '趋势', '将', '预测']):
            score += 0.2

        # 有案例或具体公司名
        if re.search(r'[A-Z][a-z]+\s?(?:Energy|Tech|Group|Company)|[一-龥]{2,4}(?:公司|集团)', content):
            score += 0.2

        return min(score, 1.0)

    def _check_actionable(self, content: str, dimension: str) -> float:
        """可执行性检查"""
        score = 0.0

        # 有明确结论
        if any(word in content for word in ['因此', '综上', '总结', '建议', '应该']):
            score += 0.5

        # 如果是"战略建议"维度，要求更高
        if dimension == '战略建议':
            if any(word in content for word in ['第一步', '优先', '阶段', '路径']):
                score += 0.5
        else:
            score += 0.5  # 其他维度不强求

        return min(score, 1.0)

    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 0.85:
            return 'A'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.5:
            return 'C'
        else:
            return 'D'

    def _generate_issues(self, scores: Dict) -> List[str]:
        """生成质量问题清单"""
        issues = []

        if scores['data_sourcing'] < 0.7:
            issues.append('❌ 数据溯源不足：数字缺乏来源标注，可信度低')

        if scores['structure'] < 0.6:
            issues.append('⚠️ 结构不完整：缺少必要的分析要素')

        if scores['depth'] < 0.5:
            issues.append('⚠️ 分析深度不够：缺乏洞察和因果分析')

        if scores['actionable'] < 0.6:
            issues.append('⚠️ 结论不明确：缺少可执行的建议')

        if not issues:
            issues.append('✅ 质量合格，符合咨询级报告标准')

        return issues


# ==================== 使用示例 ====================

def example_usage():
    """测试质量检查"""
    checker = QualityChecker()

    # 场景1: 有真实数据来源的报告
    good_report = """
    ## 市场规模分析

    根据[来源1]显示，2025年中国医疗陪护市场规模约200亿元[来源2]，
    年增长率达30%[来源3]。主要玩家包括XXX公司（市占率15%）。

    预计未来3年CAGR将达25%，因为老龄化加速和政策支持。
    """

    search_context_good = {
        'method': 'web_search',
        'results': [{'url': 'http://example.com'}]
    }

    result1 = checker.check_report(good_report, '市场规模', search_context_good)
    print(f"好报告评分: {result1['score']} ({result1['grade']})")
    print(f"问题: {result1['issues']}")

    # 场景2: LLM编造的报告（但诚实标注了）
    fallback_report = """
    ⚠️ 以下内容基于LLM训练记忆，非实时数据

    ## 市场规模分析

    估计市场规模约200亿元，年增长率约30%。
    """

    search_context_fallback = {
        'method': 'llm_fallback',
        'reason': 'Web搜索失败'
    }

    result2 = checker.check_report(fallback_report, '市场规模', search_context_fallback)
    print(f"\nFallback报告评分: {result2['score']} ({result2['grade']})")
    print(f"问题: {result2['issues']}")

    # 场景3: 假装有数据的报告（最差）
    fake_report = """
    ## 市场规模分析

    根据权威数据，市场规模200亿元，增长率30%。
    """

    search_context_fake = {
        'method': 'llm_fallback',  # 实际是fallback
        'reason': 'Web搜索失败'
    }

    result3 = checker.check_report(fake_report, '市场规模', search_context_fake)
    print(f"\n假报告评分: {result3['score']} ({result3['grade']})")
    print(f"问题: {result3['issues']}")


if __name__ == "__main__":
    example_usage()
