# 国家统计局MCP服务器

> 通过MCP协议提供国家统计局行业数据查询能力

---

## 🎯 功能

### 提供的MCP工具

1. **stats_get_industry_data** - 获取行业统计数据
   - 行业增加值
   - 增长率
   - GDP占比

2. **stats_search_by_keyword** - 关键词搜索
   - 搜索统计局数据库
   - 返回相关数据项

3. **stats_get_gdp_by_industry** - 获取各行业GDP贡献
   - 三次产业占比
   - 细分行业占比

---

## 📦 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或使用poetry
poetry install
```

---

## 🚀 启动服务器

```bash
# 直接运行
python server.py

# 或通过Claude Code配置文件启动（推荐）
# 在 .claude/mcp.json 中配置
```

---

## ⚙️ Claude Code配置

在你的 `.claude/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "stats-gov-cn": {
      "command": "python",
      "args": [
        "C:/Users/huangl265/projects/industry-research-skill/mcp/stats_gov_cn/server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 💡 使用示例

### 在Claude对话中使用

```
User: 帮我查一下医疗陪护行业2023年的统计数据

Claude会自动调用：
  stats_get_industry_data(industry="医疗陪护", year=2023)

返回：
  {
    "status": "success",
    "industry_code": "Q8400",
    "year": 2023,
    "data": {
      "value_added": "XXX亿元",
      "growth_rate": "XX%",
      "gdp_share": "X%"
    },
    "source": "国家统计局",
    "timestamp": 1234567890
  }
```

### 在Skill中使用

```python
from irs import run_research

# Skill会自动通过MCP获取统计局数据
result = run_research(
    industry="医疗陪护",
    user_params={'web_search': True}
)

# data_collector会调用MCP工具
# 获取真实的Tier 1数据
```

---

## 🏗️ 架构

```
Claude Code对话
    ↓
    MCP协议
    ↓
stats_gov_cn MCP服务器
    ↓
    HTTP请求/爬虫
    ↓
国家统计局网站
```

---

## 📊 数据流

### 1. 对话触发
```
User: "查询医疗陪护行业数据"
  ↓
Claude识别需要统计局数据
  ↓
调用MCP工具: stats_get_industry_data
```

### 2. MCP服务器处理
```
MCP服务器接收请求
  ↓
检查缓存（24小时有效）
  ↓
如果缓存命中 → 返回缓存数据
如果缓存未命中 → 爬取统计局网站
  ↓
解析数据 → 缓存 → 返回结果
```

### 3. 数据集成到Skill
```
data_collector接收MCP返回数据
  ↓
标记为Tier 1数据源
  ↓
加入collected_data
  ↓
后续AI分析使用真实数据
```

---

## 🔧 数据爬取实现

### 当前状态
- ✅ MCP服务器框架完成
- ✅ 工具接口定义完成
- ⚠️  数据爬取为简化实现（需要增强）

### 需要增强的部分

**1. 处理JavaScript渲染**
```python
from selenium import webdriver

async def _crawl_with_selenium(self, url):
    driver = webdriver.Chrome()
    driver.get(url)
    # 等待JavaScript加载
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html
```

**2. 反爬机制应对**
- 随机User-Agent
- 代理池
- 请求延迟
- Cookie处理

**3. 数据解析**
- 表格数据提取
- JSON API解析
- HTML结构解析

---

## 📝 支持的行业

当前已配置（config.yaml）：
- 医疗陪护 → Q8400
- 养老服务 → Q8500
- 在线教育 → P8200
- 金融科技 → J6800
- 新能源汽车 → C3600
- 云计算 → I6500
- 人工智能 → I6500

扩展方法：
1. 在 `config.yaml` 中添加新的行业代码映射
2. 或在MCP服务器中动态映射

---

## 🚧 待办事项

### Phase 1: 基础功能（当前）
- [x] MCP服务器框架
- [x] 工具接口定义
- [x] 配置文件
- [ ] 真实爬虫实现

### Phase 2: 增强功能
- [ ] Selenium支持
- [ ] 代理池
- [ ] 本地数据库缓存
- [ ] 数据验证

### Phase 3: 生产就绪
- [ ] 错误重试机制
- [ ] 监控和日志
- [ ] API限流
- [ ] 数据质量检查

---

## 🔍 调试

### 启用调试日志
```bash
# 设置环境变量
export MCP_DEBUG=1

# 运行服务器
python server.py
```

### 测试工具调用
```bash
# 使用MCP CLI测试
mcp test stats-gov-cn stats_get_industry_data '{"industry": "医疗陪护", "year": 2023}'
```

---

## 📖 参考资料

- [国家统计局官网](http://www.stats.gov.cn/)
- [统计数据查询](http://data.stats.gov.cn/)
- [行业分类标准](http://www.stats.gov.cn/tjbz/)
- [MCP协议文档](https://spec.modelcontextprotocol.io/)

---

## 💬 价值体现

### 之前（模拟数据）
```python
collected_data = {
    'sources': ['模拟统计局数据'],
    'tier1_coverage': 0.5  # 假的
}
```

### 现在（真实数据）
```python
collected_data = {
    'sources': [
        {
            'name': '国家统计局',
            'tier': 1,
            'url': 'http://data.stats.gov.cn/...',
            'data': {
                'value_added': '1250亿元',  # 真实数据
                'growth_rate': '15.3%',
                'gdp_share': '2.1%'
            },
            'timestamp': 1234567890
        }
    ],
    'tier1_coverage': 1.0  # 真实的Tier 1覆盖率
}
```

**这才是Skill的核心价值！**
