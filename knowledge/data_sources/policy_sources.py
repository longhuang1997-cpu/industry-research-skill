"""
政策数据源汇总

集成第三方政策网站，提供更全面的政策信息
"""

from typing import List, Dict, Optional
from datetime import datetime


class PolicySourceAggregator:
    """
    政策数据源聚合器

    集成多个第三方政策网站：
    1. 国务院政策文件库
    2. 各部委官网
    3. 地方政府政策平台
    4. 行业协会政策库
    5. 专业政策数据库
    """

    def __init__(self):
        """初始化政策数据源"""
        self.sources = self._init_sources()

    def _init_sources(self) -> List[Dict]:
        """
        初始化政策数据源列表

        Returns:
            sources: 数据源配置列表
        """
        sources = [
            # Tier 1: 官方权威源
            {
                'id': 'gov_cn',
                'name': '中国政府网',
                'url': 'http://www.gov.cn/zhengce/',
                'tier': 1,
                'coverage': ['国家政策', '部委文件', '地方政策'],
                'update_frequency': 'daily',
                'api_available': False,
                'scraping_method': 'html',
                'selectors': {
                    'list': '.listBox .listTxt ul li',
                    'title': 'a',
                    'date': '.date',
                    'url': 'a[href]'
                },
                'description': '国务院及各部委政策文件的官方发布平台'
            },
            {
                'id': 'ndrc',
                'name': '国家发改委',
                'url': 'https://www.ndrc.gov.cn/fggz/flfg/',
                'tier': 1,
                'coverage': ['产业政策', '发展规划', '价格政策'],
                'update_frequency': 'daily',
                'api_available': False,
                'scraping_method': 'html',
                'description': '产业发展、投资、价格等领域政策'
            },
            {
                'id': 'miit',
                'name': '工业和信息化部',
                'url': 'https://www.miit.gov.cn/zwgk/zcwj/',
                'tier': 1,
                'coverage': ['工业政策', '信息化政策', '中小企业政策'],
                'update_frequency': 'daily',
                'api_available': False,
                'scraping_method': 'html',
                'description': '工业、通信、中小企业相关政策'
            },
            {
                'id': 'nhc',
                'name': '国家卫健委',
                'url': 'http://www.nhc.gov.cn/wjw/gfxwj/list.shtml',
                'tier': 1,
                'coverage': ['医疗卫生政策', '人口政策', '健康中国'],
                'update_frequency': 'daily',
                'api_available': False,
                'scraping_method': 'html',
                'description': '医疗卫生、健康、人口政策'
            },
            {
                'id': 'mca',
                'name': '民政部',
                'url': 'http://www.mca.gov.cn/article/zwgk/fvfg/',
                'tier': 1,
                'coverage': ['养老政策', '社会组织', '社会救助'],
                'update_frequency': 'weekly',
                'api_available': False,
                'scraping_method': 'html',
                'description': '养老、社会福利、社会组织政策'
            },

            # Tier 2: 政策汇总平台
            {
                'id': 'pkulaw',
                'name': '北大法宝',
                'url': 'https://www.pkulaw.com/',
                'tier': 2,
                'coverage': ['全领域法律法规', '政策文件', '案例'],
                'update_frequency': 'daily',
                'api_available': True,
                'requires_subscription': True,
                'description': '最全面的法律法规数据库（需订阅）'
            },
            {
                'id': 'lawinfochina',
                'name': '法律信息资源系统',
                'url': 'https://www.lawinfochina.com/',
                'tier': 2,
                'coverage': ['法律法规', '部门规章', '地方性法规'],
                'update_frequency': 'daily',
                'api_available': True,
                'requires_subscription': True,
                'description': '专业法律法规检索平台（需订阅）'
            },
            {
                'id': 'zhengce_cloud',
                'name': '政策云',
                'url': 'https://www.zhengce.cn/',
                'tier': 2,
                'coverage': ['政府政策', '招商政策', '产业政策'],
                'update_frequency': 'daily',
                'api_available': False,
                'scraping_method': 'html',
                'description': '地方政府政策汇总平台'
            },

            # Tier 3: 行业协会政策库
            {
                'id': 'caict',
                'name': '中国信通院',
                'url': 'http://www.caict.ac.cn/kxyj/qwfb/zcfg/',
                'tier': 3,
                'coverage': ['信息通信政策', 'ICT政策解读'],
                'update_frequency': 'weekly',
                'api_available': False,
                'scraping_method': 'html',
                'description': '信息通信领域政策及解读'
            },
            {
                'id': 'caam',
                'name': '中国汽车工业协会',
                'url': 'http://www.caam.org.cn/chn/21/cate_478/list_1.html',
                'tier': 3,
                'coverage': ['汽车产业政策', '新能源汽车政策'],
                'update_frequency': 'weekly',
                'api_available': False,
                'scraping_method': 'html',
                'description': '汽车产业相关政策'
            },

            # Tier 4: 地方政策平台（示例）
            {
                'id': 'beijing_gov',
                'name': '首都之窗',
                'url': 'https://www.beijing.gov.cn/zhengce/',
                'tier': 4,
                'coverage': ['北京市政策', '区级政策'],
                'update_frequency': 'daily',
                'region': 'beijing',
                'api_available': False,
                'scraping_method': 'html',
                'description': '北京市政府政策发布平台'
            },
            {
                'id': 'shanghai_gov',
                'name': '上海市人民政府',
                'url': 'https://www.shanghai.gov.cn/nw12344/',
                'tier': 4,
                'coverage': ['上海市政策', '区级政策'],
                'update_frequency': 'daily',
                'region': 'shanghai',
                'api_available': False,
                'scraping_method': 'html',
                'description': '上海市政府政策发布平台'
            },
            {
                'id': 'guangdong_gov',
                'name': '广东省人民政府',
                'url': 'http://www.gd.gov.cn/zwgk/wjk/',
                'tier': 4,
                'coverage': ['广东省政策', '粤港澳大湾区政策'],
                'update_frequency': 'daily',
                'region': 'guangdong',
                'api_available': False,
                'scraping_method': 'html',
                'description': '广东省政府政策发布平台'
            },

            # Tier 5: 开放数据平台
            {
                'id': 'data_gov_cn',
                'name': '国家数据开放平台',
                'url': 'http://www.data.gov.cn/',
                'tier': 3,
                'coverage': ['开放数据', '政策数据集'],
                'update_frequency': 'monthly',
                'api_available': True,
                'description': '国家级开放数据平台'
            }
        ]

        return sources

    def get_sources_by_tier(self, tier: int) -> List[Dict]:
        """
        按Tier筛选数据源

        Args:
            tier: Tier等级 (1-5)

        Returns:
            sources: 符合条件的数据源列表
        """
        return [s for s in self.sources if s.get('tier') == tier]

    def get_sources_by_coverage(self, keyword: str) -> List[Dict]:
        """
        按覆盖领域筛选数据源

        Args:
            keyword: 关键词（如"医疗"、"养老"）

        Returns:
            sources: 符合条件的数据源列表
        """
        matching_sources = []

        for source in self.sources:
            coverage = source.get('coverage', [])
            if any(keyword in c for c in coverage):
                matching_sources.append(source)

        return matching_sources

    def get_sources_by_region(self, region: str) -> List[Dict]:
        """
        按地区筛选数据源

        Args:
            region: 地区代码（如"beijing", "shanghai"）

        Returns:
            sources: 符合条件的地方政策源
        """
        return [s for s in self.sources if s.get('region') == region]

    def get_all_sources(self, include_subscription: bool = False) -> List[Dict]:
        """
        获取所有数据源

        Args:
            include_subscription: 是否包含需要订阅的源

        Returns:
            sources: 数据源列表
        """
        if include_subscription:
            return self.sources
        else:
            return [s for s in self.sources if not s.get('requires_subscription', False)]

    def recommend_sources(self,
                         industry: str,
                         region: Optional[str] = None,
                         include_subscription: bool = False) -> List[Dict]:
        """
        根据行业和地区推荐数据源

        Args:
            industry: 行业名称
            region: 地区（可选）
            include_subscription: 是否包含需要订阅的源

        Returns:
            recommended: 推荐的数据源列表（按优先级排序）
        """
        recommended = []

        # 1. 添加关键词匹配的源
        matching = self.get_sources_by_coverage(industry)
        recommended.extend(matching)

        # 2. 添加地区相关的源
        if region:
            regional = self.get_sources_by_region(region)
            recommended.extend(regional)

        # 3. 添加Tier 1通用源
        tier1 = self.get_sources_by_tier(1)
        for source in tier1:
            if source not in recommended:
                recommended.append(source)

        # 4. 过滤订阅源
        if not include_subscription:
            recommended = [s for s in recommended if not s.get('requires_subscription', False)]

        # 5. 按Tier排序
        recommended.sort(key=lambda x: x.get('tier', 99))

        return recommended

    def get_source_info(self, source_id: str) -> Optional[Dict]:
        """
        获取数据源详细信息

        Args:
            source_id: 数据源ID

        Returns:
            source: 数据源信息，如果不存在返回None
        """
        for source in self.sources:
            if source['id'] == source_id:
                return source

        return None


def main():
    """测试政策数据源聚合器"""
    aggregator = PolicySourceAggregator()

    print("="*60)
    print("测试1: 列出所有Tier 1数据源")
    print("="*60)
    tier1 = aggregator.get_sources_by_tier(1)
    for source in tier1:
        print(f"  - {source['name']}")
        print(f"    覆盖: {', '.join(source['coverage'])}")
        print(f"    URL: {source['url']}\n")

    print("="*60)
    print("测试2: 医疗陪护行业推荐数据源")
    print("="*60)
    recommended = aggregator.recommend_sources(
        industry='医疗',
        region='beijing',
        include_subscription=False
    )
    for i, source in enumerate(recommended, 1):
        print(f"  {i}. {source['name']} (Tier {source['tier']})")
        print(f"     {source['description']}")

    print("\n" + "="*60)
    print("测试3: 按关键词查找数据源")
    print("="*60)
    养老_sources = aggregator.get_sources_by_coverage('养老')
    for source in 养老_sources:
        print(f"  - {source['name']}: {source['url']}")


if __name__ == '__main__':
    main()
