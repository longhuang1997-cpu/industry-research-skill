"""
流媒体数据源（微信公众号、小红书、知乎等）

提供更及时的行业资讯和用户反馈
"""

from typing import List, Dict, Optional
from datetime import datetime


class SocialMediaSourceAggregator:
    """
    流媒体数据源聚合器

    集成主流社交媒体平台：
    1. 微信公众号
    2. 小红书
    3. 知乎
    4. 微博
    5. 抖音/快手
    6. B站
    """

    def __init__(self):
        """初始化流媒体数据源"""
        self.sources = self._init_sources()
        self.search_strategies = self._init_search_strategies()

    def _init_sources(self) -> List[Dict]:
        """
        初始化流媒体数据源列表

        Returns:
            sources: 数据源配置列表
        """
        sources = [
            # Tier 1: 文字内容平台
            {
                'id': 'wechat',
                'name': '微信公众号',
                'platform_type': 'article',
                'tier': 1,
                'content_types': ['深度文章', '行业报告', '案例分析'],
                'api_available': False,
                'scraping_difficulty': 'hard',
                'methods': [
                    {
                        'name': '搜狗微信搜索',
                        'url': 'https://weixin.sogou.com/',
                        'type': 'search_engine',
                        'selectors': {
                            'list': '.news-list li',
                            'title': 'h3 a',
                            'date': '.s-p',
                            'account': '.account'
                        }
                    },
                    {
                        'name': '微信读书',
                        'url': 'https://weread.qq.com/',
                        'type': 'aggregator',
                        'description': '精选公众号文章'
                    }
                ],
                'strengths': ['深度内容', '行业专家', '一手资讯'],
                'weaknesses': ['需要人工筛选', '信息密度不均'],
                'update_frequency': 'hourly',
                'recommended_for': ['政策解读', '行业趋势', '商业模式案例']
            },
            {
                'id': 'zhihu',
                'name': '知乎',
                'platform_type': 'qa',
                'tier': 1,
                'content_types': ['问答', '专栏文章', '圆桌讨论'],
                'api_available': False,
                'scraping_difficulty': 'medium',
                'methods': [
                    {
                        'name': '知乎搜索',
                        'url': 'https://www.zhihu.com/search',
                        'type': 'native_search',
                        'api_endpoint': None  # 需要逆向
                    },
                    {
                        'name': 'RSS订阅',
                        'url': 'https://rsshub.app/zhihu/',
                        'type': 'rss',
                        'description': '通过RSSHub获取'
                    }
                ],
                'strengths': ['专业讨论', '多视角', '深度回答'],
                'weaknesses': ['信息噪音', '需要筛选高质量回答'],
                'update_frequency': 'hourly',
                'recommended_for': ['行业痛点', '用户需求', '竞品对比']
            },
            {
                'id': 'xiaohongshu',
                'name': '小红书',
                'platform_type': 'ugc',
                'tier': 2,
                'content_types': ['用户笔记', '测评', '体验分享'],
                'api_available': False,
                'scraping_difficulty': 'hard',
                'methods': [
                    {
                        'name': '小红书搜索',
                        'url': 'https://www.xiaohongshu.com/search_result',
                        'type': 'native_search',
                        'requires_login': True
                    }
                ],
                'strengths': ['用户真实反馈', '消费趋势', '痛点挖掘'],
                'weaknesses': ['B端内容少', '偏C端消费'],
                'update_frequency': 'hourly',
                'recommended_for': ['C端需求', '用户体验', '消费趋势']
            },

            # Tier 2: 视频平台
            {
                'id': 'bilibili',
                'name': 'B站',
                'platform_type': 'video',
                'tier': 2,
                'content_types': ['科普视频', '测评', '行业分析'],
                'api_available': True,
                'api_endpoint': 'https://api.bilibili.com/x/web-interface/search/all/v2',
                'scraping_difficulty': 'easy',
                'methods': [
                    {
                        'name': 'B站搜索API',
                        'url': 'https://api.bilibili.com/x/web-interface/search/all/v2',
                        'type': 'api',
                        'requires_login': False,
                        'params': {
                            'keyword': '{query}',
                            'page': 1
                        }
                    }
                ],
                'strengths': ['年轻用户', '科技内容', '专业UP主'],
                'weaknesses': ['视频处理成本高', '需要字幕提取'],
                'update_frequency': 'hourly',
                'recommended_for': ['产品测评', '技术科普', '用户教育']
            },
            {
                'id': 'douyin',
                'name': '抖音',
                'platform_type': 'short_video',
                'tier': 3,
                'content_types': ['短视频', '直播', '种草'],
                'api_available': False,
                'scraping_difficulty': 'very_hard',
                'methods': [
                    {
                        'name': '抖音搜索',
                        'url': 'https://www.douyin.com/search/',
                        'type': 'native_search',
                        'requires_login': True,
                        'anti_scraping': 'strong'
                    }
                ],
                'strengths': ['流行趋势', '大众认知'],
                'weaknesses': ['内容碎片化', '深度不足'],
                'update_frequency': 'hourly',
                'recommended_for': ['品牌传播', '用户教育', '市场认知']
            },

            # Tier 3: 微博
            {
                'id': 'weibo',
                'name': '微博',
                'platform_type': 'microblog',
                'tier': 2,
                'content_types': ['热点话题', '行业动态', '官方公告'],
                'api_available': False,
                'scraping_difficulty': 'medium',
                'methods': [
                    {
                        'name': '微博搜索',
                        'url': 'https://s.weibo.com/weibo',
                        'type': 'native_search',
                        'selectors': {
                            'list': '.card-wrap',
                            'content': '.txt',
                            'user': '.name'
                        }
                    },
                    {
                        'name': 'RSS订阅',
                        'url': 'https://rsshub.app/weibo/',
                        'type': 'rss',
                        'description': '通过RSSHub获取特定用户'
                    }
                ],
                'strengths': ['实时性强', '舆情监测', '官方发声'],
                'weaknesses': ['信息噪音大', '深度不足'],
                'update_frequency': 'real_time',
                'recommended_for': ['舆情监测', '竞品动态', '行业热点']
            },

            # Tier 4: 专业平台
            {
                'id': '36kr',
                'name': '36氪',
                'platform_type': 'news',
                'tier': 1,
                'content_types': ['科技新闻', '融资报道', '深度分析'],
                'api_available': False,
                'scraping_difficulty': 'easy',
                'methods': [
                    {
                        'name': '36氪搜索',
                        'url': 'https://36kr.com/search/articles/',
                        'type': 'native_search'
                    },
                    {
                        'name': 'RSS订阅',
                        'url': 'https://rsshub.app/36kr/',
                        'type': 'rss'
                    }
                ],
                'strengths': ['科技前沿', '创投视角', '深度报道'],
                'weaknesses': ['偏向初创企业'],
                'update_frequency': 'hourly',
                'recommended_for': ['创投动态', '新兴赛道', '商业模式']
            },
            {
                'id': 'huxiu',
                'name': '虎嗅',
                'platform_type': 'news',
                'tier': 1,
                'content_types': ['商业分析', '行业报道', '观点评论'],
                'api_available': False,
                'scraping_difficulty': 'easy',
                'methods': [
                    {
                        'name': '虎嗅搜索',
                        'url': 'https://www.huxiu.com/search',
                        'type': 'native_search'
                    }
                ],
                'strengths': ['商业洞察', '行业深度', '观点独特'],
                'weaknesses': ['更新频率较低'],
                'update_frequency': 'daily',
                'recommended_for': ['商业模式', '行业趋势', '战略分析']
            },
            {
                'id': 'jiemian',
                'name': '界面新闻',
                'platform_type': 'news',
                'tier': 2,
                'content_types': ['财经新闻', '行业报道'],
                'api_available': False,
                'scraping_difficulty': 'easy',
                'methods': [
                    {
                        'name': '界面搜索',
                        'url': 'https://www.jiemian.com/search/',
                        'type': 'native_search'
                    }
                ],
                'strengths': ['财经视角', '行业覆盖广'],
                'weaknesses': ['深度一般'],
                'update_frequency': 'hourly',
                'recommended_for': ['行业动态', '财经新闻', '政策解读']
            }
        ]

        return sources

    def _init_search_strategies(self) -> Dict:
        """
        初始化不同平台的搜索策略

        Returns:
            strategies: 搜索策略字典
        """
        return {
            'wechat': {
                'keyword_templates': [
                    '{industry}行业分析',
                    '{industry}发展趋势',
                    '{industry}政策解读',
                    '{industry}商业模式'
                ],
                'time_range': 'recent_year',
                'sort_by': 'relevance'
            },
            'zhihu': {
                'keyword_templates': [
                    '{industry}行业怎么样',
                    '{industry}发展前景',
                    '{industry}痛点',
                    '如何进入{industry}行业'
                ],
                'time_range': 'all',
                'sort_by': 'hot'
            },
            'xiaohongshu': {
                'keyword_templates': [
                    '{industry}体验',
                    '{industry}推荐',
                    '{industry}避坑'
                ],
                'time_range': 'recent_6months',
                'sort_by': 'hot'
            },
            'bilibili': {
                'keyword_templates': [
                    '{industry}科普',
                    '{industry}测评',
                    '{industry}行业分析'
                ],
                'time_range': 'all',
                'sort_by': 'view_count'
            },
            'weibo': {
                'keyword_templates': [
                    '{industry}',
                    '{industry}话题'
                ],
                'time_range': 'recent_month',
                'sort_by': 'hot'
            }
        }

    def get_sources_by_tier(self, tier: int) -> List[Dict]:
        """按Tier筛选数据源"""
        return [s for s in self.sources if s.get('tier') == tier]

    def get_sources_by_platform_type(self, platform_type: str) -> List[Dict]:
        """
        按平台类型筛选数据源

        Args:
            platform_type: article/qa/ugc/video/short_video/microblog/news

        Returns:
            sources: 符合条件的数据源列表
        """
        return [s for s in self.sources if s.get('platform_type') == platform_type]

    def recommend_sources(self,
                         research_purpose: str,
                         include_hard_scraping: bool = False) -> List[Dict]:
        """
        根据研究目的推荐数据源

        Args:
            research_purpose: 研究目的（如"用户需求"、"竞品分析"）
            include_hard_scraping: 是否包含难爬取的源

        Returns:
            recommended: 推荐的数据源列表
        """
        recommended = []

        for source in self.sources:
            # 检查是否符合研究目的
            recommended_for = source.get('recommended_for', [])
            if any(research_purpose in r for r in recommended_for):
                # 检查爬取难度
                difficulty = source.get('scraping_difficulty', 'easy')
                if include_hard_scraping or difficulty in ['easy', 'medium']:
                    recommended.append(source)

        # 按Tier排序
        recommended.sort(key=lambda x: x.get('tier', 99))

        return recommended

    def generate_search_queries(self,
                               industry: str,
                               platform_id: str) -> List[str]:
        """
        为指定平台生成搜索关键词

        Args:
            industry: 行业名称
            platform_id: 平台ID

        Returns:
            queries: 搜索关键词列表
        """
        strategy = self.search_strategies.get(platform_id, {})
        templates = strategy.get('keyword_templates', [])

        queries = []
        for template in templates:
            query = template.replace('{industry}', industry)
            queries.append(query)

        return queries

    def get_scraping_config(self, platform_id: str) -> Optional[Dict]:
        """
        获取平台的爬取配置

        Args:
            platform_id: 平台ID

        Returns:
            config: 爬取配置
        """
        for source in self.sources:
            if source['id'] == platform_id:
                return {
                    'platform': source['name'],
                    'methods': source.get('methods', []),
                    'difficulty': source.get('scraping_difficulty'),
                    'api_available': source.get('api_available', False),
                    'requires_login': any(
                        m.get('requires_login', False)
                        for m in source.get('methods', [])
                    )
                }

        return None


def main():
    """测试流媒体数据源聚合器"""
    aggregator = SocialMediaSourceAggregator()

    print("="*60)
    print("测试1: 列出所有Tier 1数据源")
    print("="*60)
    tier1 = aggregator.get_sources_by_tier(1)
    for source in tier1:
        print(f"  - {source['name']} ({source['platform_type']})")
        print(f"    优势: {', '.join(source['strengths'])}")
        print(f"    适合: {', '.join(source['recommended_for'])}\n")

    print("="*60)
    print("测试2: 医疗陪护行业 - 用户需求研究")
    print("="*60)
    recommended = aggregator.recommend_sources(
        research_purpose='用户需求',
        include_hard_scraping=False
    )
    for source in recommended:
        print(f"  - {source['name']} (爬取难度: {source['scraping_difficulty']})")

    print("\n" + "="*60)
    print("测试3: 生成搜索关键词")
    print("="*60)
    platforms = ['wechat', 'zhihu', 'xiaohongshu']
    for platform in platforms:
        queries = aggregator.generate_search_queries('医疗陪护', platform)
        source_name = next(s['name'] for s in aggregator.sources if s['id'] == platform)
        print(f"\n{source_name}:")
        for q in queries:
            print(f"  - {q}")


if __name__ == '__main__':
    main()
