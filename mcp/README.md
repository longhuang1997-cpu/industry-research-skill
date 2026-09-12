# MCP数据源服务器

> 通过MCP协议接入专业行业研究数据源

---

## 🎯 核心价值

**不是硬编码数据，而是实时接入真实数据源**

### 当前问题
- ❌ data_collector.py只是模拟搜索
- ❌ 没有真正连接统计局、政府网站
- ❌ Tier 1数据源是假的

### MCP解决方案
- ✅ 通过MCP连接真实数据源
- ✅ 统一的数据接口
- ✅ 可扩展的数据源体系

---

## 🏗️ 架构设计

### Tier 1数据源（官方权威）

**1. 国家统计局API**
- 行业增加值
- GDP占比
- 从业人数
- 固定资产投资

**2. 政府部门网站**
- 政策文件（发改委、工信部、卫健委）
- 行业规划
- 监管政策

**3. 行业协会**
- 行业白皮书
- 年度报告
- 会员企业名单

### Tier 2数据源（专业机构）

**4. 券商研报API**
- 行业研究报告
- 市场规模预测
- 竞争格局分析

**5. 企业信息API**
- 企查查/天眼查
- 企业注册数量
- 融资信息
- 经营数据

**6. 咨询公司报告**
- 艾瑞咨询
- 易观分析
- Frost & Sullivan

### Tier 3数据源（媒体资讯）

**7. 新闻资讯**
- 36氪、虎嗅
- 行业动态
- 政策解读

**8. 社交媒体**
- 知乎、微信公众号
- 行业讨论
- 用户反馈

---

## 📡 MCP服务器设计

### 1. 统计局MCP服务器

```
mcp-stats-gov-cn/
  ├── server.py          # MCP服务器主程序
  ├── api/
  │   ├── industry.py    # 行业数据API
  │   ├── gdp.py         # GDP数据API
  │   └── employment.py  # 就业数据API
  ├── cache/             # 数据缓存
  └── config.yaml        # 配置文件
```

**提供的MCP工具**：
- `stats_get_industry_data(industry_code, year)`
- `stats_get_gdp_composition(year)`
- `stats_get_employment_data(industry_code, year)`

### 2. 政策文件MCP服务器

```
mcp-policy-crawler/
  ├── server.py
  ├── crawlers/
  │   ├── ndrc.py        # 发改委
  │   ├── miit.py        # 工信部
  │   └── nhc.py         # 卫健委
  ├── parser/
  │   └── policy_parser.py  # 政策文档解析
  └── database/
      └── policies.db    # 本地政策库
```

**提供的MCP工具**：
- `policy_search(industry, keyword, start_date, end_date)`
- `policy_get_by_id(policy_id)`
- `policy_get_latest(industry, limit)`

### 3. 企业信息MCP服务器

```
mcp-enterprise-data/
  ├── server.py
  ├── apis/
  │   ├── qichacha.py    # 企查查API
  │   └── tianyancha.py  # 天眼查API
  └── aggregator.py      # 数据聚合
```

**提供的MCP工具**：
- `enterprise_count(industry, region, year)`
- `enterprise_financing(industry, year)`
- `enterprise_search(keyword, limit)`

---

## 🔌 集成到Skill

### 修改data_collector.py

```python
class DataCollector:
    def __init__(self, mcp_client=None):
        self.mcp_client = mcp_client  # 注入MCP客户端
    
    def collect_tier1_data(self, industry, year):
        """使用MCP收集Tier 1数据"""
        results = {}
        
        # 1. 统计局数据
        if self.mcp_client:
            stats_data = self.mcp_client.call_tool(
                'stats_get_industry_data',
                industry_code=self._map_industry_code(industry),
                year=year
            )
            results['stats_gov'] = stats_data
        
        # 2. 政策文件
        if self.mcp_client:
            policies = self.mcp_client.call_tool(
                'policy_search',
                industry=industry,
                start_date=f'{year-2}-01-01',
                end_date=f'{year}-12-31'
            )
            results['policies'] = policies
        
        # 3. 企业数据
        if self.mcp_client:
            enterprises = self.mcp_client.call_tool(
                'enterprise_count',
                industry=industry,
                year=year
            )
            results['enterprises'] = enterprises
        
        return results
```

---

## 🚀 实施计划

### Phase 1: 基础MCP服务器（优先）

**1.1 统计局MCP服务器**
- [ ] 解析统计局网站结构
- [ ] 实现数据爬取
- [ ] 创建MCP服务器
- [ ] 集成到data_collector

**1.2 政策文件MCP服务器**
- [ ] 爬取发改委政策文件
- [ ] 爬取工信部政策文件
- [ ] 实现关键词搜索
- [ ] 创建MCP服务器

### Phase 2: 增强数据源

**2.1 企业信息MCP**
- [ ] 接入企查查API（需要API key）
- [ ] 或自建企业信息爬虫
- [ ] 创建MCP服务器

**2.2 行业协会MCP**
- [ ] 识别主要行业协会
- [ ] 爬取协会网站
- [ ] 创建MCP服务器

### Phase 3: 高级数据源

**3.1 券商研报API**
- [ ] 接入Wind/Choice（需要付费账号）
- [ ] 或爬取公开研报
- [ ] 创建MCP服务器

---

## 💡 关键技术点

### 1. 网站爬取
- 使用Selenium处理JavaScript渲染
- 处理反爬机制（代理、请求头、延迟）
- 数据清洗和结构化

### 2. MCP协议
- 实现标准MCP服务器
- 提供清晰的工具接口
- 错误处理和重试机制

### 3. 数据缓存
- 本地数据库（SQLite）
- 避免频繁请求
- 数据更新策略

### 4. 数据质量
- 数据验证
- 异常处理
- 数据来源追溯

---

## 🎯 价值体现

### 之前（模拟数据）
```python
def auto_collect(industry):
    return {
        'sources': ['模拟数据源1', '模拟数据源2'],
        'tier1_coverage': 0.5  # 假的
    }
```

### 之后（真实数据）
```python
def auto_collect(industry):
    # 通过MCP获取真实数据
    stats_data = mcp.call('stats_get_industry_data', ...)
    policies = mcp.call('policy_search', ...)
    enterprises = mcp.call('enterprise_count', ...)
    
    return {
        'sources': [
            {'name': '国家统计局', 'url': '...', 'data': stats_data},
            {'name': '发改委政策', 'url': '...', 'data': policies},
            {'name': '企业数量', 'url': '...', 'data': enterprises}
        ],
        'tier1_coverage': 1.0  # 真实的Tier 1数据
    }
```

---

## 📝 示例：统计局MCP服务器

### server.py（伪代码）

```python
from mcp.server import Server
import requests
from bs4 import BeautifulSoup

class StatsGovMCPServer(Server):
    def __init__(self):
        super().__init__("stats-gov-cn")
        
        # 注册工具
        self.add_tool(
            name="stats_get_industry_data",
            description="获取国家统计局行业数据",
            input_schema={
                "type": "object",
                "properties": {
                    "industry_code": {"type": "string"},
                    "year": {"type": "integer"}
                }
            },
            handler=self.get_industry_data
        )
    
    async def get_industry_data(self, industry_code, year):
        """从统计局网站爬取行业数据"""
        url = f"https://data.stats.gov.cn/easyquery.htm?cn={industry_code}&zb=A0201&sj={year}"
        
        # 爬取数据
        response = requests.get(url)
        data = self._parse_stats_data(response.text)
        
        return {
            'industry_code': industry_code,
            'year': year,
            'gdp_value': data.get('gdp_value'),
            'growth_rate': data.get('growth_rate'),
            'source': url
        }
    
    def _parse_stats_data(self, html):
        """解析统计局数据"""
        soup = BeautifulSoup(html, 'html.parser')
        # 实际解析逻辑...
        return {}
```

---

## 🔍 下一步

1. **先实现统计局MCP服务器**（最基础、最权威）
2. **集成到data_collector.py**
3. **验证真实数据流**
4. **逐步扩展其他数据源**

---

这才是Skill真正的价值所在！
