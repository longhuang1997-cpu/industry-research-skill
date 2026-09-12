# 自定义数据源指南

> **核心理念**：每个行业都有专属的信息源，研究者应该建立自己的MCP数据源库

---

## 🎯 为什么要自建数据源MCP？

### Skill提供的是框架，你需要补充内容

**Skill已提供**：
- ✅ 统计局MCP（通用统计数据）
- ✅ 政策文件MCP（政府政策）
- ✅ 企业信息MCP（工商数据）

**但是**：
- ❌ 医疗行业的专业数据库（如：丁香园数据）
- ❌ 金融行业的数据终端（如：Wind、Bloomberg）
- ❌ 你公司的付费账号（如：艾瑞、Frost & Sullivan）
- ❌ 你关注的行业协会（如：中国汽车工业协会）
- ❌ 你的专业数据源（如：企业内部系统、专有API）

**这些才是你行业研究的核心竞争力！**

---

## 💡 什么情况应该自建MCP？

### 1. 长期研究某个行业

如果你长期研究某个行业（如医疗），你应该建立：

**医疗行业专用MCP服务器**：
- 国家卫健委疾病监测数据
- 医院协会数据
- 医药招标平台
- 医保局数据
- 丁香园/春雨医生等平台数据

**建议文件名**：`mcp/healthcare_industry/server.py`

---

### 2. 有付费数据账号

如果你或你公司有这些账号：

| 数据源 | 用途 | 建议MCP名称 |
|--------|------|-------------|
| **Wind资讯** | 金融/宏观数据 | `mcp/wind_api/` |
| **Choice数据** | 行业/公司数据 | `mcp/choice_api/` |
| **艾瑞咨询** | 互联网行业报告 | `mcp/iresearch/` |
| **Frost & Sullivan** | 全球行业研究 | `mcp/frost_sullivan/` |
| **IT桔子** | 创投融资数据 | `mcp/itjuzi/` |
| **36氪Pro** | 新经济数据 | `mcp/36kr_pro/` |
| **企查查VIP** | 企业深度数据 | `mcp/qichacha_vip/` |
| **天眼查API** | 企业关系图谱 | `mcp/tianyancha_api/` |

**不要浪费付费账号！把它们变成MCP，让AI直接调用！**

---

### 3. 公司内部数据系统

如果你在企业工作，公司有：
- CRM系统（客户数据）
- ERP系统（供应链数据）
- 销售数据仪表板
- 市场调研数据库
- 行业监测系统

**建议**：为每个内部系统创建MCP接口

---

### 4. 行业协会/专业网站

每个行业都有权威信息源：

| 行业 | 推荐信息源 | MCP服务器 |
|------|-----------|-----------|
| **汽车** | 中国汽车工业协会 | `mcp/caam_data/` |
| **钢铁** | 中国钢铁工业协会 | `mcp/cisa_data/` |
| **电子** | 中国电子元件协会 | `mcp/ceca_data/` |
| **医药** | 中国医药工业信息中心 | `mcp/cphidata/` |
| **地产** | 中国房地产业协会 | `mcp/realestate_data/` |

**每个行业研究者都应该建立自己行业的MCP库！**

---

## 🛠️ 如何创建自定义MCP？

### Step 1: 复制模板

我们提供了3个模板供参考：

```bash
# 选择最接近的模板复制
cp -r mcp/stats_gov_cn mcp/my_custom_source
cd mcp/my_custom_source
```

### Step 2: 修改server.py

```python
class MyCustomMCPServer:
    """你的自定义数据源MCP服务器"""
    
    def __init__(self):
        self.name = "my-custom-source"
        self.version = "0.1.0"
        
        # 你的API配置
        self.api_key = os.getenv('MY_API_KEY')  # 从环境变量读取
        self.base_url = "https://your-data-source.com/api"
    
    def get_tools(self) -> List[Tool]:
        """定义你的MCP工具"""
        return [
            Tool(
                name="my_get_industry_report",
                description="获取行业报告（来自你的付费账号）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "industry": {"type": "string"},
                        "year": {"type": "integer"}
                    },
                    "required": ["industry", "year"]
                }
            )
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> List[TextContent]:
        """处理工具调用"""
        if tool_name == "my_get_industry_report":
            # 调用你的API
            response = requests.get(
                f"{self.base_url}/report",
                headers={'Authorization': f'Bearer {self.api_key}'},
                params={'industry': arguments['industry'], 'year': arguments['year']}
            )
            
            data = response.json()
            
            return [TextContent(
                type="text",
                text=json.dumps(data, ensure_ascii=False, indent=2)
            )]
```

### Step 3: 配置API Key

在 `mcp/my_custom_source/.env` 中：

```bash
MY_API_KEY=your_api_key_here
MY_API_SECRET=your_secret_here
```

### Step 4: 配置到Claude Code

在 `.claude/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "my-custom-source": {
      "command": "python",
      "args": ["path/to/my_custom_source/server.py"],
      "env": {
        "MY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Step 5: 测试

```bash
# 启动MCP服务器
python mcp/my_custom_source/server.py

# 在Claude对话中测试
User: 使用我的自定义数据源查询医疗陪护行业报告

Claude会自动调用你的MCP工具！
```

---

## 📚 典型案例

### 案例1：Wind金融终端MCP

**场景**：你公司有Wind账号，每月花费几千元

**问题**：数据只能手动查询，无法自动化

**解决方案**：创建Wind MCP服务器

```python
# mcp/wind_api/server.py

class WindMCPServer:
    def __init__(self):
        from WindPy import w
        w.start()  # 启动Wind API
        self.w = w
    
    def get_tools(self):
        return [
            Tool(
                name="wind_get_industry_pe",
                description="获取行业PE数据（来自Wind）",
                ...
            ),
            Tool(
                name="wind_get_financial_data",
                description="获取公司财务数据（来自Wind）",
                ...
            )
        ]
    
    async def call_tool(self, tool_name, arguments):
        if tool_name == "wind_get_industry_pe":
            # 调用Wind API
            data = self.w.wss(
                "801780.SI",  # 医药生物指数
                "pe_ttm",
                f"tradeDate={arguments['date']}"
            )
            return format_wind_data(data)
```

**价值**：
- ✅ Wind账号费用不再浪费
- ✅ AI可以直接调用Wind数据
- ✅ 自动化行业分析

---

### 案例2：IT桔子创投数据MCP

**场景**：你订阅了IT桔子Pro账号

**创建MCP**：

```python
# mcp/itjuzi/server.py

class ITJuziMCPServer:
    def get_tools(self):
        return [
            Tool(
                name="itjuzi_get_financing",
                description="获取融资事件（来自IT桔子）",
                ...
            ),
            Tool(
                name="itjuzi_get_investors",
                description="获取投资机构（来自IT桔子）",
                ...
            )
        ]
```

**使用**：

```
User: 查询医疗陪护行业2023年的融资情况

Claude调用:
  itjuzi_get_financing(industry='医疗陪护', year=2023)

返回:
  {
    "total_events": 45,
    "total_amount": "23.5亿元",
    "top_deals": [
      {"company": "XX护理", "round": "B轮", "amount": "5000万美元"},
      ...
    ]
  }
```

---

### 案例3：公司内部CRM系统MCP

**场景**：你在做市场分析，公司CRM有客户数据

**创建MCP**：

```python
# mcp/company_crm/server.py

class CompanyCRMMCPServer:
    def __init__(self):
        # 连接公司内部数据库
        self.db = connect_to_internal_db()
    
    def get_tools(self):
        return [
            Tool(
                name="crm_get_customer_industry_distribution",
                description="获取客户行业分布",
                ...
            ),
            Tool(
                name="crm_get_sales_by_region",
                description="获取各地区销售数据",
                ...
            )
        ]
```

**价值**：
- ✅ 将公司内部数据纳入行业研究
- ✅ AI可以结合外部数据和内部数据
- ✅ 生成更有针对性的报告

---

## 🎯 推荐自建的MCP（按行业）

### 医疗健康行业

| 数据源 | 类型 | 价值 |
|--------|------|------|
| 丁香园数据 | 医生/患者社区 | 疾病数据、医生画像 |
| 医渡云 | 医疗大数据 | 诊疗数据、用药数据 |
| 国家药监局 | 官方数据 | 药品审批、医疗器械 |
| 医保局平台 | 支付数据 | 医保覆盖、支付趋势 |

### 金融科技行业

| 数据源 | 类型 | 价值 |
|--------|------|------|
| Wind资讯 | 金融终端 | 宏观数据、行业PE |
| Choice数据 | 金融数据 | 公司财务、估值 |
| 零壹财经 | 行业研究 | 金融科技报告 |
| 央行统计 | 官方数据 | 货币、信贷数据 |

### 新能源汽车行业

| 数据源 | 类型 | 价值 |
|--------|------|------|
| 中汽协 | 行业协会 | 产销数据、市场份额 |
| 电车汇 | 专业媒体 | 新能源汽车数据 |
| 充电桩监测 | 基础设施 | 充电桩分布、使用率 |
| 工信部公告 | 官方数据 | 新车公告、准入 |

### 在线教育行业

| 数据源 | 类型 | 价值 |
|--------|------|------|
| 教育部统计 | 官方数据 | 学生人数、教育支出 |
| 艾瑞咨询 | 行业报告 | 在线教育市场规模 |
| 七麦数据 | APP数据 | 教育APP下载量、排名 |
| 多知网 | 专业媒体 | 教育行业动态 |

---

## 📋 自建MCP检查清单

在创建自定义MCP之前，问自己：

- [ ] 这个数据源我会长期使用吗？（如果是，值得建MCP）
- [ ] 这个数据源是付费的吗？（如果是，更应该建MCP充分利用）
- [ ] 这个数据源有API吗？（有API最容易，爬虫次之）
- [ ] 这个数据源对我的行业研究关键吗？（如果是，优先建MCP）
- [ ] 我的团队其他人也会用这个数据源吗？（如果是，建MCP可以复用）

---

## 🚀 从简单开始

### 不要一开始就追求完美

**Phase 1: 最小可用版本（1小时）**
- ✅ 复制模板
- ✅ 实现1个核心工具
- ✅ 返回最基本的数据
- ✅ 能在Claude对话中调用

**Phase 2: 增加功能（1周）**
- ✅ 增加2-3个工具
- ✅ 增加缓存机制
- ✅ 增加错误处理
- ✅ 添加配置文件

**Phase 3: 生产就绪（1个月）**
- ✅ 完善所有API调用
- ✅ 增加数据验证
- ✅ 增加监控和日志
- ✅ 编写文档

**先让它能用，再让它好用！**

---

## 💬 获取帮助

### 如果你不知道如何开始

1. **在GitHub Discussions提问**：
   - 说明你的行业
   - 说明你有哪些数据源
   - 我们帮你设计MCP架构

2. **分享你的MCP**：
   - 如果你创建了有价值的MCP
   - 欢迎贡献到 `mcp/community/` 目录
   - 帮助其他人节省时间

3. **付费数据源API对接**：
   - 如果你有Wind/Choice/艾瑞等账号
   - 但不知道如何对接API
   - 可以请专业开发者帮忙（值得投入！）

---

## ✅ 核心理念总结

**Skill ≠ 全能工具**

Skill提供：
- ✅ 分析框架（方法论）
- ✅ 通用数据源（统计局、政策、企业信息）
- ✅ 质量保证（Tier分级、验证）
- ✅ MCP模板（让你快速创建自己的数据源）

**你需要补充**：
- ✅ 你行业的专业数据源
- ✅ 你公司的付费账号
- ✅ 你的内部系统
- ✅ 你关注的信息源

**这才是完整的行业研究工具链！**

---

## 📖 下一步

1. 识别你最常用的3个数据源
2. 选择1个创建MCP（从最简单的开始）
3. 在实际研究中使用
4. 逐步完善和扩展

**开始建立你自己的数据源库！**
