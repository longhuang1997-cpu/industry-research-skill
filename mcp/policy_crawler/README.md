# 政策文件爬虫MCP服务器

> 爬取政府部门政策文件，为行业研究提供Tier 1政策数据

---

## 🎯 功能

### 提供的MCP工具

1. **policy_search** - 搜索行业相关政策
   - 按行业、关键词、时间范围搜索
   - 自动识别相关政府部门
   - 返回政策列表

2. **policy_get_by_id** - 获取政策全文
   - 根据政策ID获取完整内容
   - 支持HTML、PDF、Word格式

3. **policy_get_latest** - 获取最新政策
   - 获取某行业最新N条政策
   - 按发布时间倒序

4. **policy_analyze_support** - 分析政策支持力度
   - 统计政策数量
   - 分析政策类型分布（规划/补贴/监管/标准）
   - 计算政策支持度评分（0-10分）

---

## 🏛️ 支持的政府部门

### 当前已配置

| 部门代码 | 部门名称 | 网站 |
|---------|---------|------|
| `ndrc` | 国家发改委 | https://www.ndrc.gov.cn |
| `miit` | 工信部 | https://www.miit.gov.cn |
| `nhc` | 国家卫健委 | http://www.nhc.gov.cn |
| `mca` | 民政部 | https://www.mca.gov.cn |
| `moe` | 教育部 | http://www.moe.gov.cn |
| `pbc` | 中国人民银行 | http://www.pbc.gov.cn |

### 行业-部门映射

| 行业 | 主管部门 |
|------|---------|
| 医疗陪护 | 卫健委、民政部 |
| 养老服务 | 民政部、卫健委 |
| 在线教育 | 教育部 |
| 金融科技 | 人民银行 |
| 新能源汽车 | 工信部、发改委 |
| 人工智能 | 工信部、发改委 |

---

## 📦 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 如果需要PDF解析
pip install PyPDF2 pdfplumber

# 如果需要Word解析
pip install python-docx
```

---

## 🚀 启动服务器

```bash
# 直接运行
python server.py

# 或通过Claude Code配置
# 在 .claude/mcp.json 中配置
```

---

## ⚙️ Claude Code配置

在 `.claude/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "policy-crawler": {
      "command": "python",
      "args": [
        "C:/Users/huangl265/projects/industry-research-skill/mcp/policy_crawler/server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 💡 使用示例

### 示例1：搜索政策

```
User: 查一下2023年医疗陪护行业的政策

Claude调用:
  policy_search(
    industry="医疗陪护",
    start_date="2023-01-01",
    end_date="2023-12-31",
    limit=10
  )

返回:
  {
    "status": "success",
    "industry": "医疗陪护",
    "count": 8,
    "policies": [
      {
        "id": "nhc_12345",
        "title": "关于促进医疗陪护服务发展的指导意见",
        "url": "http://www.nhc.gov.cn/...",
        "date": "2023-06-15",
        "department": "国家卫健委"
      },
      ...
    ]
  }
```

### 示例2：分析政策支持力度

```
User: 政府对医疗陪护支持力度大吗？

Claude调用:
  policy_analyze_support(
    industry="医疗陪护",
    year=2023
  )

返回:
  {
    "status": "success",
    "industry": "医疗陪护",
    "year": 2023,
    "total_policies": 15,
    "policy_types": {
      "规划类": 5,
      "补贴类": 3,
      "监管类": 4,
      "标准类": 3
    },
    "support_count": 8,
    "regulation_count": 4,
    "support_score": 7.2,
    "support_level": "积极支持"
  }
```

### 示例3：在Skill中使用

```python
from irs import run_research

# Skill会通过MCP获取政策数据
result = run_research(
    industry="医疗陪护",
    user_params={'web_search': True}
)

# data_collector调用MCP工具
# collected_data['policies'] = [真实的政策数据]
```

---

## 📊 政策分析逻辑

### 1. 政策分类

根据标题关键词自动分类：

| 类型 | 关键词 |
|-----|--------|
| 规划类 | 规划、计划、方案、纲要 |
| 补贴类 | 补贴、资金、奖励、扶持 |
|监管类 | 监管、管理、办法、条例 |
| 标准类 | 标准、规范、指南、准则 |

### 2. 政策倾向分析

**支持性关键词**：支持、鼓励、补贴、扶持、优惠、奖励、推动、促进

**监管性关键词**：监管、规范、整治、限制、禁止、严格、管控

### 3. 支持力度评分

```
支持度 = (支持性政策数 × 2 - 监管性政策数) / 总政策数
归一化到 0-10 分

评级标准：
- 8-10分：强力支持
- 6-8分：积极支持
- 4-6分：中性
- 2-4分：审慎监管
- 0-2分：严格监管
```

---

## 🔧 爬虫实现

### 当前状态

- ✅ MCP服务器框架完成
- ✅ 6个政府部门配置
- ✅ 行业-部门映射
- ✅ 政策分类和倾向分析
- ⚠️  爬虫实现为简化版（需要增强）

### 需要增强的部分

**1. 处理各部门网站差异**

每个政府网站结构不同，需要针对性解析：

```python
async def _crawl_ndrc_policies(self):
    """发改委网站特殊处理"""
    # 发改委的HTML结构
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='policy-item-ndrc')
    ...

async def _crawl_miit_policies(self):
    """工信部网站特殊处理"""
    # 工信部的HTML结构
    ...
```

**2. 处理PDF政策文件**

很多政策以PDF形式发布：

```python
import PyPDF2

def extract_pdf_text(pdf_url):
    response = requests.get(pdf_url)
    pdf = PyPDF2.PdfReader(io.BytesIO(response.content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text
```

**3. 本地政策库**

建立SQLite数据库缓存政策：

```python
import sqlite3

def save_to_database(policy):
    conn = sqlite3.connect('policies.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO policies (id, title, url, department, date, content)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (policy['id'], policy['title'], ...))
    conn.commit()
```

**4. 定期更新**

设置定时任务自动更新政策库：

```python
# 每天凌晨更新
import schedule

def update_policies():
    # 爬取最新政策
    ...

schedule.every().day.at("02:00").do(update_policies)
```

---

## 🚧 待办事项

### Phase 1: 基础功能（当前）
- [x] MCP服务器框架
- [x] 6个部门配置
- [x] 政策搜索工具
- [x] 政策分析工具
- [ ] 真实爬虫实现

### Phase 2: 增强功能
- [ ] 针对每个部门的专用爬虫
- [ ] PDF文件解析
- [ ] Word文件解析
- [ ] 本地SQLite数据库
- [ ] 政策全文缓存

### Phase 3: 高级功能
- [ ] 政策变化追踪
- [ ] 政策影响分析
- [ ] 政策关联分析
- [ ] 定期自动更新

---

## 📖 数据流

```
Claude对话
    ↓
MCP: policy_search
    ↓
policy_crawler服务器
    ↓
1. 识别行业相关部门（医疗陪护 → 卫健委+民政部）
2. 并发爬取多个部门网站
3. 解析政策列表（标题、日期、URL）
4. 下载政策全文（HTML/PDF/Word）
5. 分类和倾向分析
6. 缓存到本地数据库
    ↓
返回结构化政策数据
    ↓
data_collector集成到collected_data
    ↓
后续AI分析使用真实政策数据
```

---

## 💬 价值体现

### 之前（模拟政策）

```python
collected_data = {
    'policies': [
        {'title': '模拟政策1', 'support': '假的'}
    ],
    'policy_support': '中等'  # 猜的
}
```

### 现在（真实政策）

```python
collected_data = {
    'policies': [
        {
            'id': 'nhc_12345',
            'title': '关于促进医疗陪护服务发展的指导意见',
            'url': 'http://www.nhc.gov.cn/...',
            'date': '2023-06-15',
            'department': '国家卫健委',
            'category': '规划类',
            'sentiment': 'support',
            'content': '（政策全文）'
        },
        ...
    ],
    'policy_support': {
        'score': 7.2,
        'level': '积极支持',
        'evidence': '15条政策，8条支持性，4条监管性'
    }
}
```

**这是真实的Tier 1政策数据！**

---

## 🔍 调试

```bash
# 启用调试日志
export MCP_DEBUG=1
python server.py

# 测试工具调用
mcp test policy-crawler policy_search '{"industry": "医疗陪护", "limit": 5}'
```

---

## 📚 参考资料

- [国家发改委](https://www.ndrc.gov.cn)
- [工信部](https://www.miit.gov.cn)
- [国家卫健委](http://www.nhc.gov.cn)
- [民政部](https://www.mca.gov.cn)
- [MCP协议文档](https://spec.modelcontextprotocol.io/)
