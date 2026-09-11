"""
Web搜索工具模块

提供联网搜索能力，支持批量搜索和结果解析
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import time

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class WebSearchUtils:
    """
    Web搜索工具类

    封装联网搜索功能
    """

    def __init__(self):
        """初始化搜索工具"""
        self.search_results = []

    def web_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        执行单次Web搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            results: 搜索结果列表
                [
                    {
                        'title': '标题',
                        'url': 'URL',
                        'snippet': '摘要',
                        'source': '来源'
                    },
                    ...
                ]
        """
        # TODO: 集成Claude的web_search工具
        # 当前返回模拟数据
        print(f"  [Search] Query: {query[:50]}...")

        mock_results = [
            {
                'title': f'搜索结果 - {query}',
                'url': 'https://example.com/page1',
                'snippet': f'这是关于{query}的搜索结果摘要...',
                'source': 'example.com',
                'tier': self._detect_tier(query)
            }
        ]

        return mock_results[:max_results]

    def batch_search(self,
                    keywords: List[Dict],
                    max_per_query: int = 5,
                    delay: float = 0.5) -> List[Dict]:
        """
        批量搜索

        Args:
            keywords: 关键词列表
                [
                    {'keyword': '关键词', 'tier': 1/2/3, 'priority': 'high/normal'},
                    ...
                ]
            max_per_query: 每个查询的最大结果数
            delay: 查询间隔（秒）

        Returns:
            all_results: 所有搜索结果
        """
        print(f"\n[WebSearchUtils] Batch searching {len(keywords)} queries...")

        all_results = []

        for i, kw_info in enumerate(keywords, 1):
            query = kw_info['keyword']
            tier = kw_info.get('tier', 2)

            print(f"  [{i}/{len(keywords)}] Tier {tier}: {query[:40]}...")

            try:
                results = self.web_search(query, max_results=max_per_query)

                # 为每个结果添加元数据
                for result in results:
                    result['query'] = query
                    result['tier'] = tier
                    result['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

                all_results.extend(results)

                # 延迟避免过快请求
                if i < len(keywords):
                    time.sleep(delay)

            except Exception as e:
                print(f"    [ERROR] Search failed: {e}")
                continue

        print(f"\n[WebSearchUtils] Collected {len(all_results)} results")

        self.search_results = all_results
        return all_results

    def parse_search_results(self, raw_results: List[Dict]) -> Dict:
        """
        解析搜索结果

        提取结构化信息

        Args:
            raw_results: 原始搜索结果

        Returns:
            parsed: 解析后的结构化数据
                {
                    'total_count': int,
                    'tier1_count': int,
                    'tier2_count': int,
                    'tier3_count': int,
                    'sources': [...],
                    'data_points': [...]
                }
        """
        tier1_results = [r for r in raw_results if r.get('tier') == 1]
        tier2_results = [r for r in raw_results if r.get('tier') == 2]
        tier3_results = [r for r in raw_results if r.get('tier') == 3]

        # 提取数据源
        sources = list(set([r['source'] for r in raw_results if 'source' in r]))

        return {
            'total_count': len(raw_results),
            'tier1_count': len(tier1_results),
            'tier2_count': len(tier2_results),
            'tier3_count': len(tier3_results),
            'tier1_coverage': len(tier1_results) / len(raw_results) if raw_results else 0,
            'sources': sources,
            'results': raw_results
        }

    def clean_and_deduplicate(self, results: List[Dict]) -> List[Dict]:
        """
        清洗和去重

        Args:
            results: 搜索结果列表

        Returns:
            cleaned: 清洗后的结果
        """
        # 按URL去重
        seen_urls = set()
        cleaned = []

        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                cleaned.append(result)

        print(f"[WebSearchUtils] Deduplication: {len(results)} -> {len(cleaned)} results")

        return cleaned

    def _detect_tier(self, query: str) -> int:
        """
        检测查询的数据层级

        Args:
            query: 查询关键词

        Returns:
            tier: 1(政府官网) / 2(研报) / 3(媒体)
        """
        # Tier 1: 政府官网
        tier1_indicators = [
            'site:gov.cn',
            'site:stats.gov.cn',
            'site:nhc.gov.cn',
            'site:mca.gov.cn',
            'site:moe.gov.cn'
        ]

        for indicator in tier1_indicators:
            if indicator in query:
                return 1

        # Tier 2: 券商研报、年鉴
        tier2_indicators = ['研报', '年鉴', '统计公报', 'filetype:pdf']

        for indicator in tier2_indicators:
            if indicator in query:
                return 2

        # Tier 3: 其他
        return 3


def main():
    """测试Web搜索工具"""
    print("="*60)
    print("Test: Web Search Utils")
    print("="*60)

    # 初始化
    search_utils = WebSearchUtils()

    # 模拟关键词列表
    test_keywords = [
        {
            'keyword': '医疗陪护市场规模 site:stats.gov.cn',
            'tier': 1,
            'priority': 'high'
        },
        {
            'keyword': '长期护理保险基金支出 site:nhsa.gov.cn',
            'tier': 1,
            'priority': 'high'
        },
        {
            'keyword': '医疗陪护行业研究 filetype:pdf',
            'tier': 2,
            'priority': 'normal'
        }
    ]

    # 测试批量搜索
    results = search_utils.batch_search(test_keywords, max_per_query=3, delay=0.1)

    # 解析结果
    parsed = search_utils.parse_search_results(results)

    print("\n--- Search Summary ---")
    print(f"Total results: {parsed['total_count']}")
    print(f"Tier 1 results: {parsed['tier1_count']}")
    print(f"Tier 1 coverage: {parsed['tier1_coverage']:.1%}")
    print(f"Unique sources: {len(parsed['sources'])}")

    # 测试去重
    print("\n--- Deduplication Test ---")
    duplicate_results = results + results  # 制造重复
    cleaned = search_utils.clean_and_deduplicate(duplicate_results)


if __name__ == '__main__':
    main()
