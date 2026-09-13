"""
诚实质量关卡 - 可独立使用的质量检查模块

核心价值:
1. 区分"真实搜索数据"和"LLM记忆"
2. 对诚实标注的LLM记忆给予基础分（0.4）
3. 对假装有数据的内容给0分（惩罚欺骗）
4. 检查数字的来源标注覆盖率

设计原则:
- 零依赖（纯标准库）
- 可独立运行
- 输入输出明确
- 每个规则可验证

使用场景:
- 作为独立模块被任何研究工具调用
- 合并到cockpit的质量关卡
- 命令行直接测试
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class DataSource(Enum):
    """数据来源类型"""
    REAL_SEARCH = "real_search"      # 真实Web搜索
    LLM_MEMORY = "llm_memory"        # LLM训练记忆
    UNKNOWN = "unknown"              # 未知来源


@dataclass
class QualityResult:
    """质量检查结果"""
    score: float           # 0-1分数
    grade: str            # A/B/C/D/F等级
    passed: bool          # 是否通过
    issues: List[str]     # 具体问题清单
    source_type: str      # 数据来源类型
    honest: bool          # 是否诚实标注（仅LLM_MEMORY时有意义）

    def __repr__(self):
        return (f"QualityResult(score={self.score:.2f}, grade={self.grade}, "
                f"passed={self.passed}, source={self.source_type})")


class HonestQualityGate:
    """
    诚实质量关卡

    核心逻辑:
    1. 识别数据来源（真实搜索 vs LLM记忆）
    2. 提取数字和来源标注
    3. 计算来源覆盖率
    4. 判断是否诚实标注
    5. 综合评分
    """

    # 质量标准
    MIN_PASS_SCORE = 0.7              # 及格线
    MIN_SOURCE_COVERAGE = 0.8         # 最低来源覆盖率（80%）
    HONEST_FALLBACK_SCORE = 0.4       # 诚实标注LLM记忆的基础分
    DISHONEST_FALLBACK_SCORE = 0.0    # 假装有数据的分数

    # 权重分配
    WEIGHTS = {
        'source_coverage': 0.5,   # 来源覆盖率权重50%
        'content_quality': 0.3,   # 内容质量权重30%
        'structure': 0.2          # 结构完整性权重20%
    }

    def check(self, content: str, declared_source: str = None,
              urls: List[str] = None) -> QualityResult:
        """
        执行质量检查

        Args:
            content: 研究报告内容（Markdown）
            declared_source: 声明的数据来源（'real_search' | 'llm_memory' | None）
            urls: 如果是real_search，提供的来源URL列表

        Returns:
            QualityResult对象
        """
        # Step 1: 识别真实数据来源
        actual_source = self._identify_source(content, declared_source, urls)

        # Step 2: 提取数字和来源标注
        numbers = self._extract_numbers(content)
        source_tags = self._extract_source_tags(content)

        # Step 3: 检查诚实性（仅对LLM记忆）
        is_honest = self._check_honesty(content, actual_source)

        # Step 4: 计算各维度分数
        scores = {}

        # 4.1 来源覆盖率评分
        scores['source_coverage'] = self._score_source_coverage(
            numbers, source_tags, actual_source, is_honest
        )

        # 4.2 内容质量评分
        scores['content_quality'] = self._score_content_quality(content)

        # 4.3 结构完整性评分
        scores['structure'] = self._score_structure(content)

        # Step 5: 综合评分
        total_score = sum(
            scores[key] * self.WEIGHTS[key]
            for key in scores
        )

        # Step 6: 生成问题清单
        issues = self._generate_issues(
            scores, actual_source, is_honest, numbers, source_tags
        )

        # Step 7: 判定结果
        passed = total_score >= self.MIN_PASS_SCORE
        grade = self._score_to_grade(total_score)

        return QualityResult(
            score=total_score,
            grade=grade,
            passed=passed,
            issues=issues,
            source_type=actual_source.value,
            honest=is_honest
        )

    def _identify_source(self, content: str, declared: str,
                        urls: List[str]) -> DataSource:
        """识别真实数据来源"""
        # 如果有URL且内容中有[来源X]标注，认为是真实搜索
        if urls and len(urls) > 0:
            if re.search(r'\[来源\d+\]', content):
                return DataSource.REAL_SEARCH

        # 如果内容中明确标注了警告，认为是LLM记忆
        warning_patterns = [
            r'⚠️.*?LLM',
            r'⚠️.*?记忆',
            r'⚠️.*?训练数据',
            r'未使用实时数据',
            r'基于.*?记忆',
            r'需要验证'
        ]
        if any(re.search(p, content, re.IGNORECASE) for p in warning_patterns):
            return DataSource.LLM_MEMORY

        # 如果声明了来源，使用声明
        if declared == 'real_search':
            return DataSource.REAL_SEARCH
        elif declared == 'llm_memory':
            return DataSource.LLM_MEMORY

        # 否则根据内容推断
        has_source_tags = bool(re.search(r'\[来源\d+\]', content))
        if has_source_tags:
            return DataSource.REAL_SEARCH

        return DataSource.UNKNOWN

    def _extract_numbers(self, content: str) -> List[str]:
        """提取所有数字（带单位）"""
        patterns = [
            r'\d+(?:\.\d+)?(?:[亿万千百]+)',      # 200亿、5万
            r'\d+(?:\.\d+)?%',                     # 30%
            r'\d+(?:\.\d+)?(?:元|美元|英镑)',      # 100元
            r'\d+(?:\.\d+)?(?:户|个|人|家)',       # 5000户
            r'\d+(?:\.\d+)?(?:MW|MWh|kW)',         # 100MW
        ]

        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, content))

        return list(set(numbers))  # 去重

    def _extract_source_tags(self, content: str) -> List[str]:
        """提取所有来源标注"""
        return re.findall(r'\[来源\d+\]', content)

    def _check_honesty(self, content: str, source: DataSource) -> bool:
        """检查是否诚实标注（仅对LLM记忆有意义）"""
        if source != DataSource.LLM_MEMORY:
            return True  # 非LLM记忆，不适用

        # 检查是否有诚实标注
        warning_keywords = ['⚠️', '警告', '未使用实时数据', '基于LLM记忆',
                          '需要验证', '估算', '推测']
        return any(kw in content for kw in warning_keywords)

    def _score_source_coverage(self, numbers: List[str],
                               source_tags: List[str],
                               source: DataSource,
                               is_honest: bool) -> float:
        """来源覆盖率评分（权重50%）"""
        # 特殊情况1: 真实搜索但来源覆盖率低
        if source == DataSource.REAL_SEARCH:
            if not numbers:
                return 0.5  # 没有数字，中性分

            coverage = len(source_tags) / len(numbers)
            if coverage >= self.MIN_SOURCE_COVERAGE:
                return 1.0  # 完美
            elif coverage >= 0.5:
                return 0.7  # 还行
            else:
                return 0.3  # 不够

        # 特殊情况2: LLM记忆，检查诚实性
        elif source == DataSource.LLM_MEMORY:
            if is_honest:
                # 诚实标注给0.8分（因为权重是50%，最终得分0.4）
                return 0.8
            else:
                return 0.0  # 假装有数据，0分

        # 特殊情况3: 未知来源
        else:
            return 0.2  # 低分

    def _score_content_quality(self, content: str) -> float:
        """内容质量评分（权重30%）"""
        score = 0.0

        # 有因果分析
        if any(w in content for w in ['因为', '导致', '由于', '原因', '驱动']):
            score += 0.3

        # 有对比分析
        if any(w in content for w in ['相比', '对比', 'vs', '而', '但']):
            score += 0.3

        # 有趋势判断
        if any(w in content for w in ['未来', '预计', '趋势', '将']):
            score += 0.2

        # 有具体案例
        if re.search(r'[A-Z][a-z]+\s?(?:Energy|Tech|Group|Company)|[一-龥]{2,4}(?:公司|集团)', content):
            score += 0.2

        return min(score, 1.0)

    def _score_structure(self, content: str) -> float:
        """结构完整性评分（权重20%）"""
        score = 0.0

        # 有合理长度
        if len(content) >= 200:
            score += 0.4

        # 有标题层级
        if re.search(r'^#{1,3}\s', content, re.MULTILINE):
            score += 0.3

        # 有列表或表格
        if re.search(r'^\s*[-*+]\s', content, re.MULTILINE) or '|' in content:
            score += 0.3

        return min(score, 1.0)

    def _generate_issues(self, scores: Dict[float, float],
                        source: DataSource, is_honest: bool,
                        numbers: List[str], source_tags: List[str]) -> List[str]:
        """生成具体问题清单"""
        issues = []

        # 来源问题
        if scores['source_coverage'] < 0.5:
            if source == DataSource.LLM_MEMORY and not is_honest:
                issues.append(
                    "❌ 严重问题: 使用LLM记忆但未标注警告，假装有真实数据"
                )
            elif source == DataSource.REAL_SEARCH:
                coverage = len(source_tags) / len(numbers) if numbers else 0
                issues.append(
                    f"❌ 来源覆盖率不足: {len(source_tags)}/{len(numbers)} "
                    f"= {coverage:.0%} < {self.MIN_SOURCE_COVERAGE:.0%}"
                )

        # 内容质量问题
        if scores['content_quality'] < 0.5:
            issues.append("⚠️ 内容质量不足: 缺乏因果分析、对比或趋势判断")

        # 结构问题
        if scores['structure'] < 0.5:
            issues.append("⚠️ 结构不完整: 缺少标题层级或列表结构")

        # 如果没问题
        if not issues:
            if source == DataSource.REAL_SEARCH:
                issues.append("✅ 质量合格: 真实数据 + 充分溯源")
            elif source == DataSource.LLM_MEMORY and is_honest:
                issues.append("✅ 诚实标注: LLM记忆已明确警告")

        return issues

    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 0.9:
            return 'A+'
        elif score >= 0.85:
            return 'A'
        elif score >= 0.8:
            return 'A-'
        elif score >= 0.75:
            return 'B+'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.6:
            return 'C'
        elif score >= 0.5:
            return 'D'
        else:
            return 'F'


# ==================== 命令行测试 ====================

def run_tests():
    """完整测试套件 - 可独立验证"""
    import sys
    import io

    # 修复Windows编码问题
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    gate = HonestQualityGate()

    print("="*60)
    print("诚实质量关卡 - 测试套件")
    print("="*60)

    # 测试1: 真实搜索 + 充分溯源
    print("\n测试1: 真实搜索 + 充分溯源")
    content1 = """
## 市场规模分析

根据[来源1]显示，2025年市场规模约200亿元[来源2]，
年增长率达30%[来源3]。

主要玩家包括XXX公司（市占率15%[来源4]），因为政策支持导致市场快速增长。
相比2024年，增速提升了10个百分点。

未来预计将继续保持高增长。
    """
    result1 = gate.check(
        content1,
        declared_source='real_search',
        urls=['http://example.com/1', 'http://example.com/2']
    )
    print(f"   {result1}")
    print(f"   问题: {result1.issues}")
    assert result1.passed, f"测试1应通过，实际分数={result1.score}"
    assert result1.score >= 0.7, f"测试1分数应≥0.7，实际={result1.score}"

    # 测试2: LLM记忆 + 诚实标注
    print("\n测试2: LLM记忆 + 诚实标注")
    content2 = """
    ⚠️ 警告: 以下内容基于LLM训练记忆，非实时数据

    估计市场规模约200亿元，年增长率约30%（需验证）。
    """
    result2 = gate.check(content2, declared_source='llm_memory')
    print(f"   {result2}")
    print(f"   问题: {result2.issues}")
    assert not result2.passed, "测试2应不通过（分数<0.7）"
    assert result2.honest, "测试2应标记为诚实"
    assert result2.score >= 0.3, "测试2分数应≥0.3（诚实基础分）"

    # 测试3: LLM记忆 + 不诚实（最差）
    print("\n测试3: LLM记忆 + 假装有数据（最差）")
    content3 = """
    根据权威数据显示，市场规模约200亿元，年增长率30%。
    """
    result3 = gate.check(content3, declared_source='llm_memory')
    print(f"   {result3}")
    print(f"   问题: {result3.issues}")
    assert not result3.passed, "测试3应不通过"
    assert not result3.honest, "测试3应标记为不诚实"
    assert result3.score <= 0.1, "测试3分数应≤0.1（惩罚欺骗）"

    # 测试4: 真实搜索 + 来源覆盖率不足
    print("\n测试4: 真实搜索 + 来源覆盖率不足")
    content4 = """
    根据[来源1]显示，市场规模约200亿元，年增长率30%，
    市占率15%，用户5000万。  # 4个数字，只有1个来源标注
    """
    result4 = gate.check(
        content4,
        declared_source='real_search',
        urls=['http://example.com']
    )
    print(f"   {result4}")
    print(f"   问题: {result4.issues}")
    assert not result4.passed, "测试4应不通过（来源覆盖率<80%）"

    print("\n" + "="*60)
    print("✅ 所有测试通过！质量关卡运行正常")
    print("="*60)


if __name__ == "__main__":
    run_tests()
