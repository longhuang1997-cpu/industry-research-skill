#!/usr/bin/env python3
"""
自定义数据源MCP服务器模板

复制这个模板，修改以下部分：
1. 类名：YourDataSourceMCPServer
2. self.name：你的服务器名称
3. get_tools()：定义你的工具
4. call_tool()：实现工具逻辑
5. API配置：你的API key和base_url
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import os

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
logger = logging.getLogger("your-data-source-mcp")  # 修改这里


class YourDataSourceMCPServer:  # 修改类名
    """
    你的数据源MCP服务器

    功能描述：
    - ...
    - ...
    """

    def __init__(self):
        # ============ 修改以下配置 ============
        self.name = "your-data-source"  # MCP服务器名称
        self.version = "0.1.0"

        # API配置（从环境变量读取，保护API key）
        self.api_key = os.getenv('YOUR_API_KEY', '')
        self.api_secret = os.getenv('YOUR_API_SECRET', '')
        self.base_url = "https://your-api-endpoint.com"  # 你的API地址

        # 如果需要其他配置
        self.config = {
            'timeout': 10,
            'retry': 3,
            'cache_ttl': 86400  # 24小时缓存
        }
        # ====================================

        # 缓存
        self.cache = {}
        self.cache_ttl = self.config['cache_ttl']

    def get_tools(self) -> List[Tool]:
        """
        定义MCP工具

        每个工具都是一个可以被Claude调用的函数
        """
        return [
            # ============ 工具1：示例 ============
            Tool(
                name="your_tool_name",  # 工具名称（小写，下划线分隔）
                description="工具功能描述（Claude会根据这个描述决定是否调用）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "参数1的描述"
                        },
                        "param2": {
                            "type": "integer",
                            "description": "参数2的描述"
                        },
                        "optional_param": {
                            "type": "string",
                            "description": "可选参数",
                            "default": "默认值"
                        }
                    },
                    "required": ["param1", "param2"]  # 必需参数
                }
            ),
            # ============ 工具2：再加一个 ============
            Tool(
                name="your_second_tool",
                description="第二个工具的功能描述",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "查询关键词"
                        }
                    },
                    "required": ["query"]
                }
            )
            # 可以继续添加更多工具...
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        处理工具调用

        Claude调用工具时会触发这个函数
        """
        logger.info(f"调用工具: {tool_name}, 参数: {arguments}")

        try:
            # ============ 路由到具体的工具实现 ============
            if tool_name == "your_tool_name":
                result = await self.your_tool_implementation(
                    arguments["param1"],
                    arguments["param2"],
                    arguments.get("optional_param", "默认值")
                )
            elif tool_name == "your_second_tool":
                result = await self.your_second_tool_implementation(
                    arguments["query"]
                )
            else:
                result = {"error": f"未知工具: {tool_name}"}

            # 返回结果
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

    # ============ 工具实现区域 ============

    async def your_tool_implementation(
        self,
        param1: str,
        param2: int,
        optional_param: str
    ) -> Dict[str, Any]:
        """
        工具1的实现

        Args:
            param1: 参数1
            param2: 参数2
            optional_param: 可选参数

        Returns:
            结果字典
        """
        # 检查缓存
        cache_key = f"{param1}_{param2}"
        if cache_key in self.cache:
            logger.info(f"使用缓存: {cache_key}")
            return self.cache[cache_key]

        try:
            # ============ 方式1：调用API ============
            if self.api_key:
                result = await self._call_api(param1, param2)

            # ============ 方式2：爬虫 ============
            else:
                result = await self._crawl_data(param1, param2)

            # 缓存结果
            self.cache[cache_key] = result

            return result

        except Exception as e:
            logger.error(f"工具实现失败: {e}")
            return {
                "status": "error",
                "message": str(e),
                "fallback": "如果API失败，可以返回一些备选数据"
            }

    async def _call_api(self, param1: str, param2: int) -> Dict[str, Any]:
        """
        调用外部API获取数据

        适用于：有API key的付费数据源
        """
        url = f"{self.base_url}/your-endpoint"

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        params = {
            'param1': param1,
            'param2': param2
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.config['timeout']
            )

            if response.status_code == 200:
                data = response.json()

                return {
                    "status": "success",
                    "source": "你的数据源名称",
                    "data": data,
                    "timestamp": "2024-01-01"
                }
            else:
                raise Exception(f"API返回错误: {response.status_code}")

        except Exception as e:
            logger.error(f"API调用失败: {e}")
            raise

    async def _crawl_data(self, param1: str, param2: int) -> Dict[str, Any]:
        """
        爬虫获取数据

        适用于：没有API，需要爬取网页
        """
        url = f"https://your-website.com/data?q={param1}"

        try:
            response = requests.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=self.config['timeout']
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 解析HTML
                data = []
                items = soup.find_all('div', class_='data-item')

                for item in items:
                    data.append({
                        'title': item.find('h3').text.strip(),
                        'value': item.find('span', class_='value').text.strip()
                    })

                return {
                    "status": "success",
                    "source": "爬虫",
                    "data": data,
                    "count": len(data)
                }
            else:
                raise Exception(f"爬虫失败: {response.status_code}")

        except Exception as e:
            logger.error(f"爬虫失败: {e}")
            raise

    async def your_second_tool_implementation(self, query: str) -> Dict[str, Any]:
        """工具2的实现"""
        return {
            "status": "success",
            "query": query,
            "results": []
        }


async def main():
    """启动MCP服务器"""
    logger.info("启动自定义数据源MCP服务器...")

    server_instance = YourDataSourceMCPServer()  # 修改类名

    server = Server(server_instance.name)

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return server_instance.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        return await server_instance.call_tool(name, arguments)

    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP服务器已启动")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
