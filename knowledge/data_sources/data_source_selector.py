"""
数据源选择器：根据行业自动选择数据源并生成搜索清单

根据行业大类自动推荐:
- Tier 1数据源（政府官网、统计年鉴）
- Tier 2数据源（券商研报、行业协会）
- 搜索关键词清单
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class DataSourceSelector:
    """
    数据源选择器

    根据行业自动生成搜索关键词和数据源清单
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
    print("测试: 医疗陪护")
    print("="*60)

    keywords = selector.generate_search_keywords('医疗陪护')
    print("\n搜索关键词清单:")
    for i, kw in enumerate(keywords, 1):
        print(f"  {i}. [{kw['tier']}] {kw['keyword']}")

    print("\nTier 1数据源:")
    sources = selector.get_tier1_sources('医疗陪护')
    for source in sources:
        print(f"  - {source['name']}: {source['url']}")


if __name__ == '__main__':
    main()
