"""
数据源选择器：根据行业自动选择数据源并生成搜索清单

根据行业大类自动推荐:
- Tier 1数据源（政府官网、统计年鉴）
- Tier 2数据源（券商研报、行业协会）
- 政策数据源（新增）
- 流媒体数据源（新增）
- 搜索关键词清单
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class DataSourceSelector:
    """
    数据源选择器（增强版）

    根据行业自动生成搜索关键词和数据源清单

    新功能:
    - 集成政策数据源聚合器
    - 集成流媒体数据源聚合器
    - 提供统一的数据源推荐接口
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化数据源选择器

        Args:
            config_path: 数据源配置文件路径（可选）
        """
        if config_path is None:
            config_path = Path(__file__).parent / 'data_source_tree.yaml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.tree = yaml.safe_load(f)

        # 加载新的数据源聚合器
        from knowledge.data_sources.policy_sources import PolicySourceAggregator
        from knowledge.data_sources.social_media_sources import SocialMediaSourceAggregator

        self.policy_aggregator = PolicySourceAggregator()
        self.social_media_aggregator = SocialMediaSourceAggregator()

    def classify_industry_category(self, industry_name: str) -> str:
        """
        将具体行业归类到大类

        Args:
            industry_name: 如"医疗陪护"

        Returns:
            category: 如"医疗健康"
        """
        mapping = {
            '医疗陪护': '医疗健康',
            '居家养老': '养老服务',
            '养老院': '养老服务',
            '在线教育': '教育培训',
            '企业SaaS': '企业服务',
        }

        return mapping.get(industry_name, '其他')

    def generate_search_keywords(self, industry_name: str) -> List[Dict]:
        """
        自动生成搜索关键词清单

        Args:
            industry_name: 行业名称

        Returns:
            keywords: [{'keyword': '...', 'tier': 1, ...}, ...]
        """
        category = self.classify_industry_category(industry_name)

        if category == '其他':
            print(f"[WARNING] Unknown industry category, using generic search template")
            return self._generate_generic_keywords(industry_name)

        category_data = self.tree['data_source_tree']['by_industry_category'][category]

        keywords = []

        # 标准搜索关键词
        for pattern in category_data['standard_search_keywords']:
            keyword = pattern.replace('{行业}', industry_name)
            keywords.append({
                'keyword': keyword,
                'tier': 1,
                'expected_data': '市场规模/政策文件'
            })

        # 子行业特定关键词
        if 'sub_industries' in category_data:
            sub_data = category_data['sub_industries'].get(industry_name, {})
            if 'specific_keywords' in sub_data:
                for kw in sub_data['specific_keywords']:
                    keywords.append({
                        'keyword': kw,
                        'tier': 1,
                        'expected_data': '细分数据'
                    })

        print(f"\n[DataSourceSelector] Generated {len(keywords)} search keywords for {industry_name}")
        return keywords

    def get_tier1_sources(self, industry_name: str) -> List[Dict]:
        """
        获取Tier 1数据源清单

        Args:
            industry_name: 行业名称

        Returns:
            sources: Tier 1数据源列表
        """
        category = self.classify_industry_category(industry_name)

        if category == '其他':
            return []

        category_data = self.tree['data_source_tree']['by_industry_category'][category]
        return category_data.get('tier1_sources', [])

    def get_all_sources(self,
                       industry_name: str,
                       include_policy: bool = True,
                       include_social_media: bool = True,
                       region: Optional[str] = None) -> Dict:
        """
        获取所有类型的数据源（统一接口）

        Args:
            industry_name: 行业名称
            include_policy: 是否包含政策数据源
            include_social_media: 是否包含流媒体数据源
            region: 地区（可选，用于政策数据源）

        Returns:
            all_sources: {
                'traditional': [...],  # 传统数据源（券商研报等）
                'policy': [...],       # 政策数据源
                'social_media': [...], # 流媒体数据源
                'tier1_coverage': 0.8  # Tier 1覆盖率
            }
        """
        result = {
            'traditional': self.get_tier1_sources(industry_name),
            'policy': [],
            'social_media': [],
            'tier1_coverage': 0.0
        }

        # 添加政策数据源
        if include_policy:
            policy_sources = self.policy_aggregator.recommend_sources(
                industry=industry_name,
                region=region,
                include_subscription=False
            )
            result['policy'] = policy_sources[:10]  # 限制数量

        # 添加流媒体数据源
        if include_social_media:
            # 根据行业类型推荐不同的流媒体源
            category = self.classify_industry_category(industry_name)

            if category in ['医疗健康', '养老服务']:
                # B端+政策导向行业：优先专业内容
                social_sources = []
                social_sources.extend(
                    self.social_media_aggregator.recommend_sources('政策解读', False)
                )
                social_sources.extend(
                    self.social_media_aggregator.recommend_sources('行业趋势', False)
                )
            else:
                # 市场导向行业：优先用户反馈
                social_sources = []
                social_sources.extend(
                    self.social_media_aggregator.recommend_sources('用户需求', False)
                )
                social_sources.extend(
                    self.social_media_aggregator.recommend_sources('竞品分析', False)
                )

            # 去重
            seen = set()
            unique_sources = []
            for source in social_sources:
                if source['id'] not in seen:
                    seen.add(source['id'])
                    unique_sources.append(source)

            result['social_media'] = unique_sources[:8]  # 限制数量

        # 计算Tier 1覆盖率
        total_sources = len(result['traditional']) + len(result['policy'])
        tier1_count = len([s for s in result['policy'] if s.get('tier') == 1])
        tier1_count += len(result['traditional'])

        if total_sources > 0:
            result['tier1_coverage'] = tier1_count / total_sources

        return result

    def get_social_media_queries(self, industry_name: str) -> Dict:
        """
        生成流媒体平台的搜索关键词

        Args:
            industry_name: 行业名称

        Returns:
            queries: {'wechat': [...], 'zhihu': [...], ...}
        """
        platforms = ['wechat', 'zhihu', 'xiaohongshu', 'bilibili', 'weibo']
        queries = {}

        for platform in platforms:
            queries[platform] = self.social_media_aggregator.generate_search_queries(
                industry_name,
                platform
            )

        return queries

    def _generate_generic_keywords(self, industry_name: str) -> List[Dict]:
        """
        通用行业的默认搜索关键词

        Args:
            industry_name: 行业名称

        Returns:
            keywords: 通用关键词列表
        """
        return [
            {'keyword': f'{industry_name}市场规模 site:stats.gov.cn', 'tier': 1},
            {'keyword': f'{industry_name}行业政策 site:gov.cn', 'tier': 1},
            {'keyword': f'{industry_name}行业研究 filetype:pdf', 'tier': 2},
        ]


def main():
    """测试数据源选择器"""
    selector = DataSourceSelector()

    # 测试: 医疗陪护
    print("="*60)
    print("测试1: 医疗陪护 - 传统数据源")
    print("="*60)

    keywords = selector.generate_search_keywords('医疗陪护')
    print("\n搜索关键词清单:")
    for i, kw in enumerate(keywords[:5], 1):
        print(f"  {i}. [Tier {kw['tier']}] {kw['keyword']}")

    print("\nTier 1数据源:")
    sources = selector.get_tier1_sources('医疗陪护')
    for source in sources[:3]:
        print(f"  - {source['name']}: {source['url']}")

    print("\n" + "="*60)
    print("测试2: 医疗陪护 - 所有数据源")
    print("="*60)

    all_sources = selector.get_all_sources(
        industry_name='医疗陪护',
        include_policy=True,
        include_social_media=True,
        region='beijing'
    )

    print(f"\n传统数据源: {len(all_sources['traditional'])}个")
    print(f"政策数据源: {len(all_sources['policy'])}个")
    for source in all_sources['policy'][:3]:
        print(f"  - {source['name']} (Tier {source['tier']})")

    print(f"\n流媒体数据源: {len(all_sources['social_media'])}个")
    for source in all_sources['social_media'][:3]:
        print(f"  - {source['name']} ({source['platform_type']})")

    print(f"\nTier 1覆盖率: {all_sources['tier1_coverage']:.1%}")

    print("\n" + "="*60)
    print("测试3: 生成流媒体搜索关键词")
    print("="*60)

    social_queries = selector.get_social_media_queries('医疗陪护')
    for platform, queries in list(social_queries.items())[:2]:
        print(f"\n{platform}:")
        for q in queries[:2]:
            print(f"  - {q}")


if __name__ == '__main__':
    main()

