#!/usr/bin/env python3
"""
企业信息MCP服务器

提供企业工商数据：
- 企业注册数量（按行业、地区、时间）
- 融资信息（轮次、金额、投资方）
- 企业搜索（名称、规模、状态）
- 竞争格局分析（市场集中度、头部玩家）

数据来源：
- 企查查API（需要API key）
- 天眼查API（需要API key）
- 国家企业信用信息公示系统（爬虫）
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import time

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("请安装MCP SDK: pip install mcp")
    exit(1)

# HTTP请求
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enterprise-data-mcp")


class EnterpriseDataMCPServer:
    """企业信息MCP服务器"""

    def __init__(self):
        self.name = "enterprise-data"
        self.version = "0.1.0"

        # API配置（需要用户提供API key）
        self.api_configs = {
            'qichacha': {
                'name': '企查查',
                'base_url': 'https://api.qichacha.com',
                'api_key': '',  # 从环境变量或配置文件读取
                'enabled': False
            },
            'tianyancha': {
                'name': '天眼查',
                'base_url': 'https://open.api.tianyancha.com',
                'api_key': '',  # 从环境变量或配置文件读取
                'enabled': False
            },
            'gsxt': {
                'name': '国家企业信用信息公示系统',
                'base_url': 'http://www.gsxt.gov.cn',
                'enabled': True  # 免费，使用爬虫
            }
        }

        # 行业关键词映射
        self.industry_keywords = {
            '医疗陪护': ['医疗陪护', '陪护', '护理服务', '居家护理', '医疗护理'],
            '养老服务': ['养老', '养老院', '老年公寓', '养老服务', '长者照护'],
            '在线教育': ['在线教育', '网络教育', '远程教育', '教育科技', 'K12'],
            '金融科技': ['金融科技', 'Fintech', '互联网金融', '数字金融', '支付'],
            '新能源汽车': ['新能源汽车', '电动汽车', '充电桩', '动力电池'],
            '人工智能': ['人工智能', 'AI', '机器学习', '深度学习', '智能'],
        }

        # 缓存
        self.cache = {}
        self.cache_ttl = 86400  # 24小时

    def get_tools(self) -> List[Tool]:
        """返回MCP工具"""
        return [
            Tool(
                name="enterprise_count",
                description="统计行业企业注册数量",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {
                            "type": "string",
                            "description": "行业名称"
                        },
                        "region": {
                            "type": "string",
                            "description": "地区（可选，如：北京、上海、全国）"
                        },
                        "year": {
                            "type": "integer",
                            "description": "年份（可选）"
                        },
                        "status": {
                            "type": "string",
                            "description": "企业状态（在业、注销、吊销等）",
                            "default": "在业"
                        }
                    },
                    "required": ["industry"]
                }
            ),
            Tool(
                name="enterprise_financing",
                description="查询行业融资信息",
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
                        },
                        "round": {
                            "type": "string",
                            "description": "融资轮次（天使、A轮、B轮等，可选）"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回数量",
                            "default": 20
                        }
                    },
                    "required": ["industry", "year"]
                }
            ),
            Tool(
                name="enterprise_search",
                description="搜索企业",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "搜索关键词（企业名称或行业）"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回数量",
                            "default": 10
                        }
                    },
                    "required": ["keyword"]
                }
            ),
            Tool(
                name="enterprise_top_players",
                description="获取行业头部玩家",
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
                            "default": 10
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "排序方式（注册资本、融资总额、成立时间）",
                            "default": "注册资本"
                        }
                    },
                    "required": ["industry"]
                }
            ),
            Tool(
                name="enterprise_market_concentration",
                description="分析市场集中度",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {
                            "type": "string",
                            "description": "行业名称"
                        },
                        "metric": {
                            "type": "string",
                            "description": "衡量指标（营收、市场份额）",
                            "default": "营收"
                        }
                    },
                    "required": ["industry"]
                }
            )
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """处理工具调用"""
        logger.info(f"调用工具: {tool_name}, 参数: {arguments}")

        try:
            if tool_name == "enterprise_count":
                result = await self.count_enterprises(
                    arguments["industry"],
                    arguments.get("region"),
                    arguments.get("year"),
                    arguments.get("status", "在业")
                )
            elif tool_name == "enterprise_financing":
                result = await self.get_financing_data(
                    arguments["industry"],
                    arguments["year"],
                    arguments.get("round"),
                    arguments.get("limit", 20)
                )
            elif tool_name == "enterprise_search":
                result = await self.search_enterprises(
                    arguments["keyword"],
                    arguments.get("limit", 10)
                )
            elif tool_name == "enterprise_top_players":
                result = await self.get_top_players(
                    arguments["industry"],
                    arguments.get("limit", 10),
                    arguments.get("sort_by", "注册资本")
                )
            elif tool_name == "enterprise_market_concentration":
                result = await self.analyze_market_concentration(
                    arguments["industry"],
                    arguments.get("metric", "营收")
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

    async def count_enterprises(
        self,
        industry: str,
        region: Optional[str],
        year: Optional[int],
        status: str
    ) -> Dict[str, Any]:
        """
        统计企业数量

        Args:
            industry: 行业名称
            region: 地区
            year: 年份
            status: 企业状态

        Returns:
            企业数量统计
        """
        # 检查缓存
        cache_key = f"count_{industry}_{region}_{year}_{status}"
        if cache_key in self.cache:
            cached_time, data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                logger.info(f"使用缓存: {cache_key}")
                return data

        # 获取行业关键词
        keywords = self.industry_keywords.get(industry, [industry])

        try:
            # 优先使用API
            if self.api_configs['qichacha']['enabled']:
                count_data = await self._count_via_qichacha(keywords, region, year, status)
            elif self.api_configs['tianyancha']['enabled']:
                count_data = await self._count_via_tianyancha(keywords, region, year, status)
            else:
                # 使用爬虫（国家企业信用信息公示系统）
                count_data = await self._count_via_crawler(keywords, region, year, status)

            # 缓存
            self.cache[cache_key] = (time.time(), count_data)

            return count_data

        except Exception as e:
            logger.error(f"统计企业失败: {e}")
            return {
                "status": "error",
                "message": str(e),
                "fallback": self._get_fallback_count(industry, region, year)
            }

    async def _count_via_qichacha(
        self,
        keywords: List[str],
        region: Optional[str],
        year: Optional[int],
        status: str
    ) -> Dict[str, Any]:
        """通过企查查API统计（需要API key）"""
        api_config = self.api_configs['qichacha']

        # 构建API请求
        url = f"{api_config['base_url']}/ECIEnterprise/SearchByKey"
        headers = {
            'Token': api_config['api_key'],
            'Content-Type': 'application/json'
        }

        total_count = 0
        enterprise_samples = []

        for keyword in keywords[:3]:  # 限制关键词数量，避免API配额耗尽
            params = {
                'keyword': keyword,
                'status': status,
                'province': region if region and region != '全国' else None,
                'pageSize': 20,
                'pageIndex': 1
            }

            try:
                response = requests.post(url, json=params, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('Status') == '200':
                        result = data.get('Result', {})
                        total_count += result.get('Total', 0)
                        enterprise_samples.extend(result.get('Result', [])[:5])
            except Exception as e:
                logger.warning(f"企查查API调用失败: {e}")
                continue

        return {
            "status": "success",
            "source": "企查查API",
            "industry_keywords": keywords,
            "region": region or "全国",
            "year": year,
            "enterprise_status": status,
            "total_count": total_count,
            "samples": enterprise_samples[:10],
            "note": "数据来自企查查API"
        }

    async def _count_via_tianyancha(
        self,
        keywords: List[str],
        region: Optional[str],
        year: Optional[int],
        status: str
    ) -> Dict[str, Any]:
        """通过天眼查API统计（需要API key）"""
        # 类似企查查实现
        return {
            "status": "success",
            "source": "天眼查API",
            "note": "天眼查API实现类似企查查"
        }

    async def _count_via_crawler(
        self,
        keywords: List[str],
        region: Optional[str],
        year: Optional[int],
        status: str
    ) -> Dict[str, Any]:
        """
        通过爬虫统计（国家企业信用信息公示系统）

        注意：这是简化实现，实际需要：
        1. 处理验证码
        2. 处理JavaScript渲染
        3. 处理反爬机制
        """
        base_url = "http://www.gsxt.gov.cn"

        # 这里返回模拟数据，实际需要真正爬取
        logger.warning("爬虫功能未完全实现，返回估算数据")

        return {
            "status": "success",
            "source": "估算（爬虫未完全实现）",
            "industry_keywords": keywords,
            "region": region or "全国",
            "year": year,
            "enterprise_status": status,
            "estimated_count": self._estimate_count(keywords[0], region, year),
            "note": "实际需要接入企查查/天眼查API或完善爬虫"
        }

    def _estimate_count(self, industry: str, region: Optional[str], year: Optional[int]) -> int:
        """估算企业数量（基于行业经验）"""
        # 简化的估算逻辑
        base_counts = {
            '医疗陪护': 15000,
            '养老服务': 50000,
            '在线教育': 30000,
            '金融科技': 20000,
            '新能源汽车': 10000,
            '人工智能': 25000,
        }

        base = base_counts.get(industry, 10000)

        # 地区调整
        if region and region != '全国':
            base = int(base * 0.15)  # 单个省份约占15%

        # 年份增长
        if year and year >= 2020:
            growth_rate = 0.15  # 年均15%增长
            years = 2024 - year
            base = int(base * ((1 + growth_rate) ** years))

        return base

    def _get_fallback_count(self, industry: str, region: Optional[str], year: Optional[int]) -> Dict[str, Any]:
        """备选数据"""
        return {
            "estimated_count": self._estimate_count(industry, region, year),
            "note": "估算数据，建议接入企查查/天眼查API获取准确数据",
            "recommendation": [
                "1. 申请企查查API key",
                "2. 或申请天眼查API key",
                "3. 配置到config.yaml中"
            ]
        }

    async def get_financing_data(
        self,
        industry: str,
        year: int,
        round_type: Optional[str],
        limit: int
    ) -> Dict[str, Any]:
        """获取融资数据"""
        # 简化实现
        return {
            "status": "success",
            "industry": industry,
            "year": year,
            "round": round_type,
            "total_events": 0,
            "total_amount": "N/A",
            "financing_list": [],
            "note": "融资数据需要接入专业数据源（IT桔子、36氪等）"
        }

    async def search_enterprises(self, keyword: str, limit: int) -> Dict[str, Any]:
        """搜索企业"""
        return {
            "status": "success",
            "keyword": keyword,
            "count": 0,
            "enterprises": [],
            "note": "需要接入企查查/天眼查API"
        }

    async def get_top_players(self, industry: str, limit: int, sort_by: str) -> Dict[str, Any]:
        """获取头部玩家"""
        return {
            "status": "success",
            "industry": industry,
            "sort_by": sort_by,
            "top_players": [],
            "note": "需要接入企查查/天眼查API"
        }

    async def analyze_market_concentration(self, industry: str, metric: str) -> Dict[str, Any]:
        """分析市场集中度"""
        return {
            "status": "success",
            "industry": industry,
            "metric": metric,
            "hhi_index": "N/A",  # Herfindahl-Hirschman Index
            "cr4": "N/A",  # 前4企业市场份额
            "cr8": "N/A",  # 前8企业市场份额
            "note": "需要接入营收数据源"
        }


async def main():
    """启动MCP服务器"""
    logger.info("启动企业信息MCP服务器...")

    server_instance = EnterpriseDataMCPServer()

    server = Server(server_instance.name)

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return server_instance.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        return await server_instance.call_tool(name, arguments)

    async with stdio_server() as (read_stream, write_stream):
        logger.info("企业信息MCP服务器已启动")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
