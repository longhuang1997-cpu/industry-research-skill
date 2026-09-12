# 5分钟创建你的第一个MCP

> 从零到能用，只需要5分钟

---

## 🎯 目标

创建一个最简单的MCP服务器，让Claude能调用你的数据源。

---

## 📋 准备

你需要：
1. ✅ 一个数据源（API、网站、或者数据库）
2. ✅ Python 3.8+
3. ✅ 5分钟时间

---

## 🚀 Step 1: 复制模板（30秒）

```bash
# 复制模板到新目录
cd industry-research-skill/mcp
cp -r _template my_data_source

cd my_data_source
```

---

## ✏️ Step 2: 修改server.py（2分钟）

打开 `server.py`，修改3个地方：

### 2.1 修改类名和服务器名称

```python
# 第33行左右
class MyDataSourceMCPServer:  # 改成你的名字
    def __init__(self):
        self.name = "my-data-source"  # 改成你的服务器名称
```

### 2.2 定义你的第一个工具

```python
# 第48行左右
def get_tools(self) -> List[Tool]:
    return [
        Tool(
            name="my_get_data",  # 你的工具名称
            description="获取我的数据源的数据",  # 描述功能
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "查询关键词"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]
```

### 2.3 实现工具逻辑

```python
# 第85行左右
async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
    if tool_name == "my_get_data":
        # 最简单的实现：返回固定数据
        result = {
            "status": "success",
            "keyword": arguments["keyword"],
            "data": {
                "value1": "数据1",
                "value2": "数据2"
            }
        }
    
    return [TextContent(
        type="text",
        text=json.dumps(result, ensure_ascii=False, indent=2)
    )]
```

**完成！你的MCP服务器已经可以运行了！**

---

## ⚙️ Step 3: 配置到Claude Code（1分钟）

在 `.claude/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "my-data-source": {
      "command": "python",
      "args": [
        "C:/Users/你的路径/industry-research-skill/mcp/my_data_source/server.py"
      ]
    }
  }
}
```

---

## ✅ Step 4: 测试（1分钟）

### 4.1 重启Claude Code

配置改变后需要重启。

### 4.2 在对话中测试

```
User: 使用my_get_data工具查询"医疗陪护"

Claude会自动调用你的MCP工具！

返回:
{
  "status": "success",
  "keyword": "医疗陪护",
  "data": {
    "value1": "数据1",
    "value2": "数据2"
  }
}
```

---

## 🎉 成功！

你已经创建了第一个MCP服务器！

---

## 📈 Step 5: 进阶（10分钟）

现在让它真正调用你的数据源：

### 5.1 如果你有API

```python
async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
    if tool_name == "my_get_data":
        # 调用你的API
        response = requests.get(
            "https://your-api.com/data",
            params={"keyword": arguments["keyword"]},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        data = response.json()
        
        return [TextContent(
            type="text",
            text=json.dumps(data, ensure_ascii=False, indent=2)
        )]
```

### 5.2 如果你要爬虫

```python
async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
    if tool_name == "my_get_data":
        # 爬取网页
        response = requests.get(f"https://your-site.com/search?q={arguments['keyword']}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析数据
        items = soup.find_all('div', class_='item')
        data = [{"title": item.text} for item in items]
        
        result = {
            "status": "success",
            "data": data
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
```

### 5.3 如果你有数据库

```python
import sqlite3

async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
    if tool_name == "my_get_data":
        # 查询数据库
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM your_table WHERE keyword LIKE ?",
            (f"%{arguments['keyword']}%",)
        )
        
        rows = cursor.fetchall()
        data = [{"id": row[0], "value": row[1]} for row in rows]
        
        conn.close()
        
        result = {
            "status": "success",
            "data": data
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
```

---

## 🔒 保护API Key

### 方法1：环境变量

```bash
# 在终端设置
export YOUR_API_KEY="your_api_key_here"

# 在server.py中读取
self.api_key = os.getenv('YOUR_API_KEY', '')
```

### 方法2：.env文件

创建 `mcp/my_data_source/.env`：

```bash
YOUR_API_KEY=your_api_key_here
YOUR_API_SECRET=your_secret_here
```

在server.py中：

```python
from dotenv import load_dotenv
load_dotenv()

self.api_key = os.getenv('YOUR_API_KEY')
```

在.claude/mcp.json中：

```json
{
  "mcpServers": {
    "my-data-source": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "YOUR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

## 🐛 常见问题

### Q1: MCP服务器没有启动

**检查**：
- Python版本是否 >= 3.8
- 是否安装了MCP SDK: `pip install mcp`
- .claude/mcp.json 路径是否正确

### Q2: Claude没有调用我的工具

**检查**：
- 工具的description是否清晰描述了功能
- 参数的description是否明确
- 尝试明确告诉Claude："使用my_get_data工具"

### Q3: API调用失败

**检查**：
- API key是否正确
- 网络是否可访问API
- API是否有速率限制

---

## 📚 下一步

1. ✅ **添加更多工具**：在get_tools()中添加更多Tool
2. ✅ **添加缓存**：避免重复请求，参考模板中的cache实现
3. ✅ **错误处理**：捕获异常，返回友好的错误信息
4. ✅ **阅读完整指南**：查看 CUSTOM_DATA_SOURCE_GUIDE.md

---

## 💡 实际案例

### 案例：IT桔子融资数据（5分钟）

```python
class ITJuziMCPServer:
    def __init__(self):
        self.name = "itjuzi"
        self.api_key = os.getenv('ITJUZI_API_KEY')
    
    def get_tools(self):
        return [
            Tool(
                name="itjuzi_get_financing",
                description="获取行业融资数据（来自IT桔子）",
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
    
    async def call_tool(self, tool_name, arguments):
        if tool_name == "itjuzi_get_financing":
            response = requests.get(
                "https://api.itjuzi.com/financing",
                params={
                    "industry": arguments["industry"],
                    "year": arguments["year"]
                },
                headers={"Token": self.api_key}
            )
            
            data = response.json()
            
            return [TextContent(
                type="text",
                text=json.dumps(data, ensure_ascii=False, indent=2)
            )]
```

**使用**：

```
User: 查询医疗陪护行业2023年的融资情况

Claude: [自动调用 itjuzi_get_financing(industry='医疗陪护', year=2023)]

返回真实的IT桔子数据！
```

---

## 🎯 核心要点

1. **从最简单开始**：先返回固定数据，确保MCP能运行
2. **逐步增强**：再接入真实API
3. **保护密钥**：使用环境变量或.env文件
4. **清晰描述**：工具的description决定Claude是否调用

**5分钟创建，终身受益！**

---

现在开始创建你的第一个MCP吧！
