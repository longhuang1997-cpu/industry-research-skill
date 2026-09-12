# MCP数据源扩展指南

> **架构决策（2026-09-12）**：不预建空壳MCP，按需引导用户自建真实数据源

---

## 🎯 架构原则

**Skill内置能力 vs 用户自建MCP**

### ✅ Skill内置（开箱即用）
- Claude对话中的Web搜索
- 公开信息检索和分析
- 基于搜索结果的AI推理

### ⚠️ 用户自建（按需扩展）
- 付费数据订阅（Wind、Choice、艾瑞）
- 企业内部系统（CRM、ERP、BI）
- 特定行业数据库（医疗、汽车、金融）

**判断标准**：如果用户没有相关账号/权限，MCP就是空壳，不如直接用Web搜索。

---

## 🔌 何时需要自建MCP？

### 场景1：有付费数据订阅

### 场景1：有付费数据订阅

```bash
# 示例：Wind金融终端
mcp/wind_api/
  ├── server.py          # MCP服务器
  ├── wind_client.py     # Wind API封装
  └── config.yaml        # API key配置
```

**价值**：自动化查询，无需手动登录Wind终端。

### 场景2：长期研究特定行业

```bash
# 示例：医疗行业专属数据源
mcp/healthcare_industry/
  ├── server.py
  ├── sources/
  │   ├── nhc_crawler.py     # 卫健委爬虫
  │   ├── yaozhi_api.py      # 药智网API
  │   └── dingxiang_api.py   # 丁香园API
  └── config.yaml
```

**价值**：一次配置，多次复用，积累行业数据资产。

### 场景3：接入公司内部系统

```bash
# 示例：内部BI系统
mcp/company_bi/
  ├── server.py
  └── bi_connector.py    # 连接内部数据仓库
```

**价值**：将内部数据和外部研究结合，生成定制化洞察。

---

## 🚀 快速自建MCP（5分钟）

### 模板结构

```python
# server.py
from mcp.server import Server

class MyDataSourceMCP(Server):
    def __init__(self):
        super().__init__("my-data-source")
        
        self.add_tool(
            name="get_industry_data",
            description="获取行业数据",
            input_schema={
                "type": "object",
                "properties": {
                    "industry": {"type": "string"}
                }
            },
            handler=self.get_data
        )
    
    async def get_data(self, industry):
        # 调用你的API或爬虫
        data = fetch_from_your_source(industry)
        return data

if __name__ == "__main__":
    server = MyDataSourceMCP()
    server.run()
```

### 集成到Skill

```bash
# 1. 启动MCP服务器
python mcp/my-data-source/server.py

# 2. 在skill中调用（自动发现）
# Skill会自动识别可用的MCP工具
```

---

## 💡 推荐数据源

### Tier 1（官方权威）
- 国家统计局：http://data.stats.gov.cn
- 政府部门网站：发改委、工信部、卫健委
- 行业协会官网

### Tier 2（专业机构）
- 企查查API：https://www.qcc.com/api
- 天眼查API：https://www.tianyancha.com/open
- Wind金融终端（需付费）
- Choice数据（需付费）

### Tier 3（媒体资讯）
- 36氪、虎嗅、钛媒体
- 知乎、微信公众号搜索

---

## 🎯 总结

**不要预建空壳MCP，按需引导用户自建真实数据源。**

- ✅ Skill提供框架和方法论
- ✅ 用户补充专属数据源
- ✅ 形成可扩展的数据生态

---

参考Claude Code MCP文档：https://github.com/anthropics/anthropic-cookbook/tree/main/mcp
