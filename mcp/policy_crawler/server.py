#!/usr/bin/env python3
"""
政策文件MCP服务器

爬取政府部门政策文件：
- 国家发改委（NDRC）
- 工信部（MIIT）
- 卫健委（NHC）
- 民政部（MCA）
- 各部委行业政策

提供政策检索、全文获取、政策解读
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import re

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("请安装MCP SDK: pip install mcp")
    exit(1)

# 爬虫工具
import requests
from bs4 import BeautifulSoup
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("policy-crawler-mcp")


class PolicyCrawlerMCPServer:
    """政策文件MCP服务器"""

    def __init__(self):
        self.name = "policy-crawler"
        self.version = "0.1.0"

        # 政府部门网站配置
        self.departments = {
            'ndrc': {
                'name': '国家发改委',
                'url': 'https://www.ndrc.gov.cn',
                'policy_list': 'https://www.ndrc.gov.cn/fggz/',
                'search': 'https://sousuo.ndrc.gov.cn/search/fullsearch'
            },
            'miit': {
                'name': '工信部',
                'url': 'https://www.miit.gov.cn',
                'policy_list': 'https://www.miit.gov.cn/zwgk/zcwj/',
                'search': 'https://www.miit.gov.cn/search'
            },
            'nhc': {
                'name': '国家卫健委',
                'url': 'http://www.nhc.gov.cn',
                'policy_list': 'http://www.nhc.gov.cn/wjw/gfxwj/list.shtml',
                'search': 'http://www.nhc.gov.cn/search'
            },
            'mca': {
                'name': '民政部',
                'url': 'https://www.mca.gov.cn',
                'policy_list': 'https://www.mca.gov.cn/article/zcwj/',
                'search': 'https://www.mca.gov.cn/searchPage.do'
            }
        }

        # 行业到部门的映射
        self.industry_department_map = {
            '医疗陪护': ['nhc', 'mca'],
            '养老服务': ['mca', 'nhc'],
            '在线教育': ['moe'],  # 教育部
            '金融科技': ['pbc', 'cbirc'],  # 人民银行、银保监会
            '新能源汽车': ['miit', 'ndrc'],
            '云计算': ['miit'],
            '人工智能': ['miit', 'ndrc'],
        }

        # 缓存
        self.cache = {}
        self.cache_ttl = 604800  # 7天（政策更新不频繁）

    def get_tools(self) -> List[Tool]:
        """返回MCP工具"""
        return [
            Tool(
                name="policy_search",
                description="搜索行业相关政策文件",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {
                            "type": "string",
                            "description": "行业名称"
                        },
                        "keyword": {
                            "type": "string",
                            "description": "搜索关键词（可选）"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "开始日期 YYYY-MM-DD（可选）"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "结束日期 YYYY-MM-DD（可选）"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回数量",
                            "default": 10
                        }
                    },
                    "required": ["industry"]
                }
            ),
            Tool(
                name="policy_get_by_id",
                description="获取政策文件全文",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "policy_id": {
                            "type": "string",
                            "description": "政策文件ID"
                        }
                    },
                    "required": ["policy_id"]
                }
            ),
            Tool(
                name="policy_get_latest",
                description="获取行业最新政策",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {
                            "type": "string",
                            "description": "行业名称"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回数量",
                            "default": 5
                        }
                    },
                    "required": ["industry"]
                }
            ),
            Tool(
                name="policy_analyze_support",
                description="分析政策支持力度",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {
                            "type": "string",
                            "description": "行业名称"
                        },
                        "year": {
                            "type": "integer",
                            "description": "年份"
                        }
                    },
                    "required": ["industry", "year"]
                }
            )
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """处理工具调用"""
        logger.info(f"调用工具: {tool_name}, 参数: {arguments}")

        try:
            if tool_name == "policy_search":
                result = await self.search_policies(
                    arguments["industry"],
                    arguments.get("keyword"),
                    arguments.get("start_date"),
                    arguments.get("end_date"),
                    arguments.get("limit", 10)
                )
            elif tool_name == "policy_get_by_id":
                result = await self.get_policy_by_id(arguments["policy_id"])
            elif tool_name == "policy_get_latest":
                result = await self.get_latest_policies(
                    arguments["industry"],
                    arguments.get("limit", 5)
                )
            elif tool_name == "policy_analyze_support":
                result = await self.analyze_policy_support(
                    arguments["industry"],
                    arguments["year"]
                )
            else:
                result = {"error": f"未知工具: {tool_name}"}

            return [TextContent(
                type="text",
                text=json.dumps(result, ensure_ascii=False, indent=2)
            )]

        except Exception as e:
            logger.error(f"工具调用失败: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, ensure_ascii=False)
            )]

    async def search_policies(
        self,
        industry: str,
        keyword: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        limit: int
    ) -> Dict[str, Any]:
        """
        搜索政策文件

        Args:
            industry: 行业名称
            keyword: 搜索关键词
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量

        Returns:
            政策列表
        """
        # 获取相关部门
        departments = self.industry_department_map.get(industry, ['ndrc', 'miit'])

        # 构建搜索关键词
        search_keywords = [industry]
        if keyword:
            search_keywords.append(keyword)

        policies = []

        # 遍历相关部门搜索
        for dept_code in departments:
            if dept_code not in self.departments:
                continue

            dept = self.departments[dept_code]
            logger.info(f"搜索 {dept['name']} 的政策...")

            try:
                dept_policies = await self._crawl_department_policies(
                    dept_code,
                    search_keywords,
                    start_date,
                    end_date,
                    limit
                )
                policies.extend(dept_policies)
            except Exception as e:
                logger.error(f"{dept['name']} 爬取失败: {e}")
                continue

        # 按时间排序
        policies.sort(key=lambda x: x.get('date', ''), reverse=True)

        # 限制数量
        policies = policies[:limit]

        return {
            "status": "success",
            "industry": industry,
            "keyword": keyword,
            "count": len(policies),
            "policies": policies
        }

    async def _crawl_department_policies(
        self,
        dept_code: str,
        keywords: List[str],
        start_date: Optional[str],
        end_date: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        爬取某个部门的政策

        这是简化实现，实际需要：
        1. 处理每个部门网站的特殊结构
        2. 处理JavaScript渲染
        3. 处理分页
        """
        dept = self.departments[dept_code]
        policies = []

        try:
            # 访问政策列表页
            response = requests.get(
                dept['policy_list'],
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=10
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')

            # 解析政策列表（需要根据实际网站结构调整）
            policy_items = soup.find_all('li', class_='policy-item')[:limit]

            for item in policy_items:
                try:
                    title_elem = item.find('a')
                    date_elem = item.find('span', class_='date')

                    if not title_elem:
                        continue

                    policy = {
                        'id': f"{dept_code}_{hash(title_elem.get('href', ''))}",
                        'title': title_elem.text.strip(),
                        'url': dept['url'] + title_elem.get('href', ''),
                        'date': date_elem.text.strip() if date_elem else 'N/A',
                        'department': dept['name'],
                        'department_code': dept_code
                    }

                    # 关键词过滤
                    if any(kw in policy['title'] for kw in keywords):
                        policies.append(policy)

                except Exception as e:
                    logger.warning(f"解析政策项失败: {e}")
                    continue

        except Exception as e:
            logger.error(f"爬取 {dept['name']} 失败: {e}")

        return policies

    async def get_policy_by_id(self, policy_id: str) -> Dict[str, Any]:
        """获取政策全文"""
        # 简化实现
        return {
            "status": "success",
            "policy_id": policy_id,
            "content": "政策全文内容（实际需要爬取）",
            "note": "实际实现需要根据policy_id爬取具体政策页面"
        }

    async def get_latest_policies(self, industry: str, limit: int) -> Dict[str, Any]:
        """获取最新政策"""
        # 使用search_policies实现
        return await self.search_policies(
            industry,
            keyword=None,
            start_date=None,
            end_date=None,
            limit=limit
        )

    async def analyze_policy_support(self, industry: str, year: int) -> Dict[str, Any]:
        """
        分析政策支持力度

        统计:
        - 政策数量
        - 政策类型分布
        - 支持措施
        """
        # 搜索该年的政策
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        policies_result = await self.search_policies(
            industry,
            keyword=None,
            start_date=start_date,
            end_date=end_date,
            limit=100
        )

        policies = policies_result.get('policies', [])

        # 分析政策类型
        policy_types = {
            '规划类': 0,
            '补贴类': 0,
            '监管类': 0,
            '标准类': 0,
            '其他': 0
        }

        support_keywords = ['支持', '鼓励', '补贴', '扶持', '优惠', '奖励']
        regulation_keywords = ['监管', '规范', '整治', '限制', '禁止']

        support_count = 0
        regulation_count = 0

        for policy in policies:
            title = policy.get('title', '')

            # 分类
            if '规划' in title or '计划' in title:
                policy_types['规划类'] += 1
            elif '补贴' in title or '资金' in title:
                policy_types['补贴类'] += 1
            elif '监管' in title or '管理' in title:
                policy_types['监管类'] += 1
            elif '标准' in title or '规范' in title:
                policy_types['标准类'] += 1
            else:
                policy_types['其他'] += 1

            # 支持/监管倾向
            if any(kw in title for kw in support_keywords):
                support_count += 1
            if any(kw in title for kw in regulation_keywords):
                regulation_count += 1

        # 计算支持力度评分
        total_policies = len(policies)
        if total_policies == 0:
            support_score = 0
        else:
            support_score = (support_count * 2 - regulation_count) / total_policies
            support_score = max(0, min(10, support_score * 5))  # 归一化到0-10

        return {
            "status": "success",
            "industry": industry,
            "year": year,
            "total_policies": total_policies,
            "policy_types": policy_types,
            "support_count": support_count,
            "regulation_count": regulation_count,
            "support_score": round(support_score, 2),
            "support_level": self._get_support_level(support_score),
            "policies": policies[:10]  # 返回前10条
        }

    def _get_support_level(self, score: float) -> str:
        """根据分数判断支持力度"""
        if score >= 8:
            return "强力支持"
        elif score >= 6:
            return "积极支持"
        elif score >= 4:
            return "中性"
        elif score >= 2:
            return "审慎监管"
        else:
            return "严格监管"


async def main():
    """启动MCP服务器"""
    logger.info("启动政策文件MCP服务器...")

    server_instance = PolicyCrawlerMCPServer()

    server = Server(server_instance.name)

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return server_instance.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        return await server_instance.call_tool(name, arguments)

    async with stdio_server() as (read_stream, write_stream):
        logger.info("政策文件MCP服务器已启动")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
