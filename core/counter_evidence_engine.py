"""
反面证据搜索引擎 - Phase 3 任务1

核心功能:
1. 提取章节关键结论
2. 生成反向搜索关键词
3. 搜索并返回Top 3反面证据

作者: Claude Opus 5
日期: 2026-09-17
"""

import re
from typing import List, Dict, Optional


class CounterEvidenceEngine:
    """反面证据搜索引擎"""

    # 反向搜索模板
    COUNTER_QUERY_TEMPLATES = [
        "{conclusion} 失败案例",
        "{conclusion} 反例",
        "{conclusion} 不适用",
        "{conclusion} 局限性",
        "为什么{conclusion}不成立",
    ]

    # 关键结论提取模式
    CONCLUSION_PATTERNS = [
        r"建议[:：](.+?)。",
        r"应该(.+?)。",
        r"需要(.+?)。",
        r"必须(.+?)。",
        r"因此[,，](.+?)。",
        r"结论[:：](.+?)。",
        r"可以(.+?)。",
    ]

    def __init__(self):
        """初始化反面证据引擎"""
        self.web_search_available = self._check_web_search()

    def _check_web_search(self) -> bool:
        """检查Web搜索是否可用"""
        try:
            # 尝试导入Web搜索模块
            from utils.web_search import web_search
            return True
        except ImportError:
            print("[CounterEvidence] ⚠️ Web搜索模块未找到，将使用模拟搜索")
            return False

    def find_counter_evidence(self,
                             chapter_content: str,
                             chapter_title: str) -> List[Dict]:
        """
        找反面证据

        Args:
            chapter_content: 章节内容
            chapter_title: 章节标题

        Returns:
            [
                {
                    'source': 'https://...',
                    'title': '某公司PLG模式失败案例',
                    'snippet': '试点3年后因财政压力暂停，覆盖率降至20%',
                    'query': '原始搜索关键词'
                },
                ...
            ]
        """
        print(f"[CounterEvidence] 正在为「{chapter_title}」搜索反面证据...")

        # Step 1: 提取关键结论
        conclusions = self._extract_key_conclusions(chapter_content)

        if not conclusions:
            print("[CounterEvidence] ⚠️ 未提取到关键结论")
            return []

        print(f"[CounterEvidence] 提取到{len(conclusions)}个关键结论")

        # Step 2: 为每个结论搜索反面证据
        all_evidences = []
        for i, conclusion in enumerate(conclusions, 1):
            print(f"[CounterEvidence] 结论{i}: {conclusion[:50]}...")

            queries = self._generate_counter_queries(conclusion)

            for query in queries[:2]:  # 每个结论只用前2个query
                print(f"[CounterEvidence]   搜索: {query}")
                results = self._web_search(query, max_results=2)
                all_evidences.extend(results)

        # Step 3: 去重
        unique_evidences = self._deduplicate(all_evidences)

        print(f"[CounterEvidence] ✅ 找到{len(unique_evidences)}个反面证据")
        return unique_evidences[:3]  # 返回Top 3

    def _extract_key_conclusions(self, chapter_content: str) -> List[str]:
        """
        提取关键结论（规则方法）

        Args:
            chapter_content: 章节内容

        Returns:
            关键结论列表（最多3个）
        """
        conclusions = []

        for pattern in self.CONCLUSION_PATTERNS:
            matches = re.findall(pattern, chapter_content, re.MULTILINE)
            conclusions.extend([m.strip() for m in matches if len(m.strip()) > 10])

        # 去重 + 限制数量
        unique_conclusions = []
        seen = set()
        for conclusion in conclusions:
            # 简单去重（前30个字符）
            key = conclusion[:30]
            if key not in seen:
                seen.add(key)
                unique_conclusions.append(conclusion)
                if len(unique_conclusions) >= 3:
                    break

        return unique_conclusions

    def _generate_counter_queries(self, conclusion: str) -> List[str]:
        """
        生成反向搜索关键词

        Args:
            conclusion: 关键结论

        Returns:
            反向搜索关键词列表
        """
        queries = []

        # 截断过长的结论（保留核心部分）
        short_conclusion = conclusion[:50] if len(conclusion) > 50 else conclusion

        for template in self.COUNTER_QUERY_TEMPLATES:
            queries.append(template.format(conclusion=short_conclusion))

        return queries

    def _web_search(self, query: str, max_results: int = 2) -> List[Dict]:
        """
        Web搜索（实际或模拟）

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        if self.web_search_available:
            # 实际搜索
            try:
                from utils.web_search import web_search
                return web_search(query, max_results=max_results)
            except Exception as e:
                print(f"[CounterEvidence] ⚠️ Web搜索失败: {e}")
                return self._mock_search(query, max_results)
        else:
            # 模拟搜索
            return self._mock_search(query, max_results)

    def _mock_search(self, query: str, max_results: int = 2) -> List[Dict]:
        """
        模拟搜索（用于测试）

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            模拟的搜索结果
        """
        # 模拟结果（用于测试和演示）
        mock_results = [
            {
                'source': f'https://example.com/article/{hash(query) % 1000}',
                'title': f'关于"{query[:20]}..."的反思与案例分析',
                'snippet': f'本文通过多个实际案例分析了"{query[:30]}..."的局限性和失败教训...',
                'query': query
            },
            {
                'source': f'https://research.org/paper/{hash(query) % 500}',
                'title': f'学术研究："{query[:20]}..."的适用边界',
                'snippet': f'研究表明，"{query[:30]}..."在特定条件下可能不适用，需要谨慎评估...',
                'query': query
            }
        ]

        return mock_results[:max_results]

    def _deduplicate(self, evidences: List[Dict]) -> List[Dict]:
        """
        去重（基于URL）

        Args:
            evidences: 证据列表

        Returns:
            去重后的证据列表
        """
        seen_urls = set()
        unique = []

        for evidence in evidences:
            url = evidence.get('source', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(evidence)

        return unique


# ==================== 测试代码 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("反面证据引擎 - 单元测试")
    print("=" * 60)

    engine = CounterEvidenceEngine()

    # 测试章节内容
    test_chapter = """
    # 政策环境分析

    政府推动长护险试点，覆盖1.45亿人。建议：加速试点推广，扩大覆盖范围。

    从财政投入看，政府补贴占比达80%，因此，长护险的可持续性依赖于政府财政支持。

    结论：长护险是政策驱动型行业，政府支持是核心驱动力。
    """

    # 测试
    counter_evidences = engine.find_counter_evidence(test_chapter, "政策环境分析")

    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)

    if counter_evidences:
        for i, evidence in enumerate(counter_evidences, 1):
            print(f"\n反面证据{i}:")
            print(f"  标题: {evidence['title']}")
            print(f"  来源: {evidence['source']}")
            print(f"  摘要: {evidence['snippet'][:60]}...")
    else:
        print("⚠️ 未找到反面证据")

    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
