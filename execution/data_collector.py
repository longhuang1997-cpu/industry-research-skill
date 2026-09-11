"""
数据收集器：自动化数据收集

功能:
1. 根据数据源选择器生成的关键词执行联网搜索
2. 批量收集数据
3. 数据去重和清洗
4. 数据来源分级（Tier 1/2/3）
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class DataCollector:
    """
    数据收集器

    自动化数据收集流程
    """

    def __init__(self):
        """初始化数据收集器"""
        self.collected_data = []
        self.sources = []

    def auto_collect(self,
                     industry: str,
                     year: int,
                     data_source_selector) -> Dict:
        """
        自动收集数据

        Args:
            industry: 行业名称
            year: 目标年份
            data_source_selector: 数据源选择器实例

        Returns:
            data: {
                'raw_data': [...],
                'sources': [...],
                'tier1_coverage': 0.0-1.0,
                'stats': {...}
            }
        """
        print(f"\n[DataCollector] Starting data collection for {industry} ({year})...")

        # Step 1: 生成搜索关键词
        keywords = data_source_selector.generate_search_keywords(industry)
        print(f"   生成了{len(keywords)}个搜索关键词")

        # Step 2: 获取Tier 1数据源
        tier1_sources = data_source_selector.get_tier1_sources(industry)
        print(f"   识别了{len(tier1_sources)}个Tier 1数据源")

        # Step 3: 批量搜索（当前版本为模拟）
        search_results = self._batch_search(keywords)

        # Step 4: 数据清洗和去重
        cleaned_data = self._clean_and_deduplicate(search_results)

        # Step 5: 计算Tier 1覆盖率
        tier1_coverage = self._calculate_tier1_coverage(
            cleaned_data,
            tier1_sources
        )

        print(f"   [OK] Collection complete, Tier 1 coverage: {tier1_coverage:.1%}")

        return {
            'raw_data': cleaned_data,
            'sources': self.sources,
            'tier1_coverage': tier1_coverage,
            'stats': {
                'total_keywords': len(keywords),
                'total_results': len(cleaned_data),
                'tier1_sources': len(tier1_sources)
            }
        }

    def _batch_search(self, keywords: List[Dict]) -> List[Dict]:
        """
        批量搜索

        使用WebSearchUtils执行真实搜索
        """
        # 导入web搜索工具
        try:
            from utils.web_search_utils import WebSearchUtils
            search_utils = WebSearchUtils()
        except ImportError:
            print("   [WARNING] WebSearchUtils not available, using mock data")
            return self._mock_batch_search(keywords)

        print(f"   [Search] Executing batch search...")

        # 执行批量搜索
        results = search_utils.batch_search(keywords, max_per_query=3, delay=0.3)

        # 清洗和去重
        cleaned_results = search_utils.clean_and_deduplicate(results)

        # 转换为标准格式
        formatted_results = []
        for result in cleaned_results:
            formatted_results.append({
                'keyword': result.get('query', ''),
                'tier': result.get('tier', 2),
                'data': result.get('snippet', ''),
                'source_url': result.get('url', ''),
                'source_name': result.get('source', ''),
                'timestamp': result.get('timestamp', ''),
                'title': result.get('title', '')
            })

            self.sources.append({
                'url': result.get('url', ''),
                'tier': result.get('tier', 2),
                'name': result.get('source', '')
            })

        return formatted_results

    def _mock_batch_search(self, keywords: List[Dict]) -> List[Dict]:
        """
        模拟批量搜索（降级方案）
        """
        results = []

        print(f"   [Mock Search] Using mock data...")

        for i, kw_info in enumerate(keywords[:5], 1):  # 搜索前5个
            result = {
                'keyword': kw_info['keyword'],
                'tier': kw_info['tier'],
                'data': f"Mock data for: {kw_info['keyword']}",
                'source_url': 'http://example.com',
                'source_name': 'example.com',
                'timestamp': '2026-09-11',
                'title': f'Result for {kw_info["keyword"]}'
            }
            results.append(result)
            self.sources.append({
                'url': result['source_url'],
                'tier': kw_info['tier'],
                'name': result['source_name']
            })

            print(f"      [{i}/{min(5, len(keywords))}] {kw_info['keyword'][:40]}...")

        if len(keywords) > 5:
            print(f"      ... {len(keywords)-5} more keywords pending")

        return results

    def _clean_and_deduplicate(self, results: List[Dict]) -> List[Dict]:
        """
        数据清洗和去重
        """
        # 简单去重（基于source_url）
        seen_urls = set()
        cleaned = []

        for result in results:
            url = result.get('source_url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                cleaned.append(result)

        return cleaned

    def _calculate_tier1_coverage(self,
                                   data: List[Dict],
                                   tier1_sources: List[Dict]) -> float:
        """
        计算Tier 1数据覆盖率
        """
        if not data:
            return 0.0

        tier1_count = sum(1 for d in data if d.get('tier') == 1)
        return tier1_count / len(data)


def main():
    """测试数据收集器"""
    from knowledge.data_sources.data_source_selector import DataSourceSelector

    print("="*60)
    print("测试: 数据收集器")
    print("="*60)

    # 初始化
    selector = DataSourceSelector()
    collector = DataCollector()

    # 测试自动收集
    result = collector.auto_collect(
        industry='医疗陪护',
        year=2024,
        data_source_selector=selector
    )

    print("\n收集结果:")
    print(f"  原始数据: {result['stats']['total_results']}条")
    print(f"  数据源数量: {len(result['sources'])}个")
    print(f"  Tier 1覆盖率: {result['tier1_coverage']:.1%}")


if __name__ == '__main__':
    main()
